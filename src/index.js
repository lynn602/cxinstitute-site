// CX Institute SA website Worker.
// Serves the static site from ./public and handles one endpoint:
//   POST /api/enquiry  →  emails the enquiry to TO_EMAIL via Resend, with Reply-To set to the visitor.
//
// Required settings (Cloudflare → Workers & Pages → cxinstitute-site → Settings → Variables and Secrets):
//   RESEND_API_KEY  (secret)  – API key from resend.com
//   FROM_EMAIL      (secret)  – a sender address on a domain verified in Resend
// TO_EMAIL is set in wrangler.jsonc.

const MAX_BODY = 8192;
const MIN_FILL_MS = 3000;

export const INTERESTS = {
  keynote: 'Keynote (01 Inspire)',
  game: 'The Customer Journey Game© (02 Experience)',
  touchpoints: 'TOUCHPOINTS programme (03 Embed)',
  unsure: 'Not sure yet – advise me'
};

const validEmail = (v) =>
  typeof v === 'string' && v.length <= 254 &&
  /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)*\.[a-zA-Z]{2,}$/.test(v);

const clean = (v, max) =>
  typeof v === 'string'
    ? v.replace(/[\u0000-\u0008\u000B\u000C\u000E-\u001F\u007F]/g, '').trim().slice(0, max)
    : '';

const oneLine = (v) => v.replace(/[\r\n]+/g, ' ');

const esc = (s) =>
  s.replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));

const json = (body, status = 200) =>
  Response.json(body, { status, headers: { 'Cache-Control': 'no-store' } });

export function validate(data) {
  const f = {
    name: oneLine(clean(data.name, 100)),
    email: clean(data.email, 254),
    company: oneLine(clean(data.company, 150)),
    role: oneLine(clean(data.role, 100)),
    phone: oneLine(clean(data.phone, 40)),
    interest: clean(data.interest, 20),
    timing: oneLine(clean(data.timing, 120)),
    audience: oneLine(clean(data.audience, 60)),
    message: clean(data.message, 3000)
  };
  const errors = [];
  if (f.name.length < 2) errors.push('name');
  if (!validEmail(f.email)) errors.push('email');
  if (f.company.length < 2) errors.push('company');
  if (!INTERESTS[f.interest]) errors.push('interest');
  if (f.message.length < 10) errors.push('message');
  return { fields: f, errors };
}

export function buildEmail(f) {
  const label = INTERESTS[f.interest];
  const rows = [
    ['Interested in', label],
    ['Name', f.name],
    ['Email', f.email],
    ['Company', f.company],
    ['Role', f.role],
    ['Phone', f.phone],
    ['Event date / timing', f.timing],
    ['Group size', f.audience]
  ].filter(([, v]) => v);

  const subject = `Website enquiry: ${label.split(' (')[0]} – ${f.name}, ${f.company}`;
  const text =
    `New enquiry from cxinstitute.co.za\n\n` +
    rows.map(([k, v]) => `${k}: ${v}`).join('\n') +
    `\n\nMessage:\n${f.message}\n\nReply to this email to answer ${f.name} directly.`;
  const html =
    `<!doctype html><html lang="en"><body style="margin:0;background:#f4f7fa;font-family:Arial,sans-serif;color:#1d2a3a">` +
    `<table role="presentation" style="width:100%;border-collapse:collapse"><tr><td style="padding:24px 12px">` +
    `<table role="presentation" style="width:100%;max-width:600px;margin:auto;background:#fff;border-collapse:collapse">` +
    `<tr><td style="background:#173C68;color:#fff;padding:20px 24px;border-bottom:4px solid #3EA69D">` +
    `<div style="font-size:12px;letter-spacing:2px;text-transform:uppercase;color:#6cc3bb">New website enquiry</div>` +
    `<div style="font-size:20px;font-weight:bold;margin-top:6px">${esc(label)}</div></td></tr>` +
    `<tr><td style="padding:20px 24px"><table role="presentation" style="width:100%;border-collapse:collapse;font-size:14px">` +
    rows
      .map(
        ([k, v]) =>
          `<tr><td style="padding:7px 0;color:#5b6878;width:150px;vertical-align:top">${esc(k)}</td>` +
          `<td style="padding:7px 0;font-weight:bold;color:#173C68">${esc(v)}</td></tr>`
      )
      .join('') +
    `</table><div style="margin-top:18px;padding:16px;background:#e8f4f3;border-left:4px solid #3EA69D;white-space:pre-wrap;line-height:1.55;font-size:14px">${esc(f.message)}</div>` +
    `<p style="font-size:13px;color:#5b6878;margin-top:18px">Reply to this email to answer ${esc(f.name)} directly.</p></td></tr>` +
    `</table></td></tr></table></body></html>`;
  return { subject, text, html };
}

export function createHandler(send = fetch) {
  return {
    async fetch(request, env) {
      const url = new URL(request.url);
      if (url.pathname !== '/api/enquiry') {
        return env.ASSETS ? env.ASSETS.fetch(request) : new Response('Not found', { status: 404 });
      }
      if (request.method !== 'POST') return json({ ok: false, error: 'method' }, 405);

      const origin = request.headers.get('origin');
      if (origin) {
        try {
          if (new URL(origin).host !== url.host) return json({ ok: false, error: 'origin' }, 403);
        } catch {
          return json({ ok: false, error: 'origin' }, 403);
        }
      }
      if (!(request.headers.get('content-type') || '').startsWith('application/json')) {
        return json({ ok: false, error: 'type' }, 415);
      }
      const raw = await request.text();
      if (raw.length > MAX_BODY) return json({ ok: false, error: 'size' }, 413);

      let data;
      try {
        data = JSON.parse(raw);
      } catch {
        return json({ ok: false, error: 'json' }, 400);
      }
      if (!data || typeof data !== 'object') return json({ ok: false, error: 'json' }, 400);

      // Spam traps: a hidden field people never fill, and forms submitted impossibly fast.
      // Bots get a normal-looking success so they don't adapt.
      if (clean(data.website, 200)) return json({ ok: true });
      if (typeof data.elapsed === 'number' && data.elapsed < MIN_FILL_MS) return json({ ok: true });

      const { fields, errors } = validate(data);
      if (errors.length) return json({ ok: false, error: 'invalid', fields: errors }, 400);

      if (!env.RESEND_API_KEY || !validEmail(env.FROM_EMAIL) || !validEmail(env.TO_EMAIL)) {
        return json({ ok: false, error: 'not_configured' }, 503);
      }

      const { subject, text, html } = buildEmail(fields);
      try {
        const res = await send('https://api.resend.com/emails', {
          method: 'POST',
          headers: {
            Authorization: `Bearer ${env.RESEND_API_KEY}`,
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            from: `CX Institute SA website <${env.FROM_EMAIL}>`,
            to: [env.TO_EMAIL],
            reply_to: fields.email,
            subject,
            text,
            html
          }),
          signal: AbortSignal.timeout(15000)
        });
        if (!res.ok) return json({ ok: false, error: 'send' }, 502);
        return json({ ok: true });
      } catch {
        return json({ ok: false, error: 'send' }, 502);
      }
    }
  };
}

export default createHandler();

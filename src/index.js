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


// Dedicated keynote enquiry validation and two-recipient email delivery.
const KEYNOTES = {
  'welcome-to-the-age-of-experience': 'Welcome to the Age of Experience',
  'customer-experience-blueprint': 'Customer Experience Blueprinting',
  'b2b-customer-experience-cpx': 'B2B Proof of Value',
  'ai-and-humanization-cx': 'Welcome to the World of Humanization',
  'customer-journey-game': 'CX Keynote + The Customer Journey Simulation Game'
};
const AUDIENCES = ['Board Level','Executives & Senior Leaders','Management','Supervisors','Sales','Frontline Staff','A Combination of All'];
export function validateKeynote(data) {
  const f = {
    keynote: clean(data.keynote, 80),
    keynote_format: clean(data.keynote_format, 40),
    company: oneLine(clean(data.company, 150)),
    name: oneLine(clean(data.name, 100)),
    role: oneLine(clean(data.role, 100)),
    email: clean(data.email, 254),
    phone: oneLine(clean(data.phone, 40)),
    event_name: oneLine(clean(data.event_name, 160)),
    event_date: clean(data.event_date, 10),
    event_venue: oneLine(clean(data.event_venue, 160)),
    event_city: oneLine(clean(data.event_city, 100)),
    event_country: oneLine(clean(data.event_country, 100)),
    delegates: Number(data.delegates),
    delegate_types: Array.isArray(data.delegate_types) ? [...new Set(data.delegate_types.filter(x => typeof x === 'string' && AUDIENCES.includes(x)))] : [],
    message: clean(data.message, 4000)
  };
  const errors=[];
  if (!KEYNOTES[f.keynote]) errors.push('keynote');
  if (!['In-person keynote','Virtual Keynote'].includes(f.keynote_format)) errors.push('keynote_format');
  for (const k of ['company','name','phone','event_name','event_venue','event_city','event_country']) if (f[k].length < 2) errors.push(k);
  if (!validEmail(f.email)) errors.push('email');
  if (!/^\d{4}-\d{2}-\d{2}$/.test(f.event_date) || Number.isNaN(Date.parse(f.event_date))) errors.push('event_date');
  if (!Number.isInteger(f.delegates) || f.delegates < 1 || f.delegates > 100000) errors.push('delegates');
  if (!f.delegate_types.length) errors.push('delegate_types');
  if (f.message.length < 10) errors.push('message');
  return {fields:f,errors};
}
export function buildKeynoteEmail(f) {
  const rows=[
    ['Keynote',KEYNOTES[f.keynote]],['Keynote format',f.keynote_format],['Contact name',f.name],['Company',f.company],['Role',f.role],
    ['Email',f.email],['Telephone',f.phone],['Event name',f.event_name],['Event date',f.event_date],
    ['Event venue',f.event_venue],['Event city',f.event_city],['Event country',f.event_country],
    ['Number of delegates',String(f.delegates)],['Types of delegates',f.delegate_types.join(', ')],
    ['Tell us more about your event',f.message]
  ];
  const text=rows.map(([k,v])=>k+': '+v).join('\n\n');
  const html='<div style="font-family:Arial,sans-serif;max-width:680px;color:#002d57"><h1 style="background:#002d57;color:white;padding:20px">Customer Experience Keynote Enquiry</h1>'+rows.map(([k,v])=>'<p style="border-bottom:1px solid #dce6ea;padding:9px"><strong>'+esc(k)+':</strong> '+esc(v).replace(/\n/g,'<br>')+'</p>').join('')+'</div>';
  return {subject:'Customer Experience Keynote Enquiry',text,html};
}

export function createHandler(send = fetch) {
  return {
    async fetch(request, env) {
      const url = new URL(request.url);
      if (url.pathname !== '/api/enquiry' && url.pathname !== '/api/keynote-enquiry') {
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

      if (url.pathname === '/api/keynote-enquiry') {
        const {fields,errors}=validateKeynote(data);
        if (errors.length) return json({ok:false,error:'invalid',fields:errors},400);
        if (!env.RESEND_API_KEY || !validEmail(env.FROM_EMAIL) || !validEmail(env.TO_EMAIL)) return json({ok:false,error:'not_configured'},503);
        const {subject,text,html}=buildKeynoteEmail(fields);
        try {
          // Resend supports sending the same message to the organiser and CXISA.
          // Both recipients must be accepted before the page shows success.
          const res=await send('https://api.resend.com/emails',{
            method:'POST',
            headers:{Authorization:`Bearer ${env.RESEND_API_KEY}`,'Content-Type':'application/json'},
            body:JSON.stringify({from:`CX Institute SA <${env.FROM_EMAIL}>`,to:[env.TO_EMAIL,fields.email],reply_to:fields.email,subject,text,html}),
            signal:AbortSignal.timeout(15000)
          });
          if (!res.ok) return json({ok:false,error:'send'},502);
          return json({ok:true});
        } catch { return json({ok:false,error:'send'},502); }
      }

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

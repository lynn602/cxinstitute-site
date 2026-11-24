// CX Institute SA website Worker.
// Serves the static site from ./public and handles one endpoint:
//   POST /api/enquiry  →  emails the enquiry to TO_EMAIL via Resend, with Reply-To set to the visitor.
//
// Required settings (Cloudflare → Workers & Pages → cxinstitute-site → Settings → Variables and Secrets):
//   RESEND_API_KEY  (secret)  – API key from resend.com
//   FROM_EMAIL      (secret)  – a sender address on a domain verified in Resend
// TO_EMAIL is set in wrangler.jsonc.

const MAX_BODY = 16384;
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
    `<tr><td style="background:#002D57;color:#fff;padding:20px 24px;border-bottom:4px solid #0A8FB0">` +
    `<div style="font-size:12px;letter-spacing:2px;text-transform:uppercase;color:#6cc3bb">New website enquiry</div>` +
    `<div style="font-size:20px;font-weight:bold;margin-top:6px">${esc(label)}</div></td></tr>` +
    `<tr><td style="padding:20px 24px"><table role="presentation" style="width:100%;border-collapse:collapse;font-size:14px">` +
    rows
      .map(
        ([k, v]) =>
          `<tr><td style="padding:7px 0;color:#5b6878;width:150px;vertical-align:top">${esc(k)}</td>` +
          `<td style="padding:7px 0;font-weight:bold;color:#002D57">${esc(v)}</td></tr>`
      )
      .join('') +
    `</table><div style="margin-top:18px;padding:16px;background:#e8f4f3;border-left:4px solid #0A8FB0;white-space:pre-wrap;line-height:1.55;font-size:14px">${esc(f.message)}</div>` +
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


const BOOKING_ROOMS=['Standard Conference Room','Auditorium','Boardroom','Training Room','Not applicable – virtual event'];
const BOOKING_TECH=['Wifi access','Smart Screen','Data Projector + Screen','Audio + Speakers','Lapel Microphone','Handheld Microphone','Technician on site'];
export function validateBooking(data){
 const {fields:f,errors}=validateKeynote(data);
 for(const [k,max] of Object.entries({onsite_contact:100,onsite_mobile:40,room_type:80,event_timezone:80,setup_from:5,setup_to:5,presentation_from:5,presentation_to:5,technical_notes:1000})) f[k]=clean(data[k],max);
 for(const k of ['onsite_contact','onsite_mobile','event_timezone']) if(f[k].length<2) errors.push(k);
 if(!BOOKING_ROOMS.includes(f.room_type)) errors.push('room_type');
 f.technical=Array.isArray(data.technical)?[...new Set(data.technical.filter(x=>BOOKING_TECH.includes(x)))]:[];
 for(const k of ['setup_from','setup_to','presentation_from','presentation_to']) if(!/^([01]\d|2[0-3]):[0-5]\d$/.test(f[k])) errors.push(k);
 if(f.setup_from>=f.setup_to||f.presentation_from>=f.presentation_to||f.setup_to>f.presentation_from) errors.push('time_ranges');
 return {fields:f,errors};
}
export function buildBookingEmail(f){
 const base=buildKeynoteEmail(f);
 const rows=[['On-site conference contact',f.onsite_contact],['On-site mobile',f.onsite_mobile],['Room type',f.room_type],['Time zone',f.event_timezone],['Technical equipment available',f.technical.join(', ')||'None selected'],['Set-up and technical dry run',f.setup_from+' – '+f.setup_to],['Presentation time',f.presentation_from+' – '+f.presentation_to],['Technical notes',f.technical_notes]];
 return {subject:'Keynote Booking Confirmation – '+oneLine(f.event_name),text:'Keynote Booking Confirmation\n\n'+base.text+'\n\n'+rows.map(([k,v])=>k+': '+v).join('\n'),html:'<!doctype html><html lang="en"><body style="margin:0;background:#f2f6f8;font-family:Inter,Arial,sans-serif"><table role="presentation" width="100%" cellspacing="0" cellpadding="0"><tr><td style="padding:24px 12px"><table role="presentation" width="100%" style="max-width:680px;margin:auto;background:white;border-collapse:collapse;color:#002D57"><tr><td style="background:#002D57;border-bottom:5px solid #0A8FB0;padding:28px;color:white"><img src="https://cxinstitute-site.lynn-1fa.workers.dev/assets/img/cxisa-logo-white.png" alt="CX Institute SA" width="127" style="display:block;margin-bottom:20px"><h1 style="font-family:Montserrat,Arial,sans-serif;font-size:25px;color:white;margin:0">Keynote Booking Confirmation</h1><p style="color:#48B3C5;margin-bottom:0">Lynn Baker · Customer Experience Keynotes</p></td></tr><tr><td style="padding:24px"><p>Dear '+esc(f.name)+',</p><p>Thank you for confirming your keynote booking. Please retain this summary of your submitted event and technical arrangements for your records.</p>'+base.html.replace(/<h1[^>]*>.*?<\/h1>/,'')+'<h2 style="color:#007F98;font-size:19px;border-bottom:2px solid #0A8FB0;padding-bottom:8px">On-site and technical arrangements</h2>'+rows.map(([k,v])=>'<p style="border-bottom:1px solid #dce6ea;padding:9px;overflow-wrap:anywhere"><strong>'+esc(k)+':</strong> '+esc(v).replace(/\n/g,'<br>')+'</p>').join('')+'<p>Please contact <a href="mailto:lynn@cx-company.com">lynn@cx-company.com</a> if any arrangements change.</p><p>Kind regards,<br><strong>Lynn Baker</strong><br>CX Institute SA</p></td></tr><tr><td style="background:#002D57;color:white;padding:20px;text-align:center;border-top:4px solid #0A8FB0">CX Institute SA · <a style="color:#fff" href="https://www.cxinstitute.co.za">www.cxinstitute.co.za</a></td></tr></table></td></tr></table></body></html>'};
}

const EMAIL_BASE='https://cxinstitute-site.lynn-1fa.workers.dev';
const EMAIL_CONTACT='<div style="padding:20px 0;border-top:2px solid #0A8FB0;margin-top:24px;color:#002D57"><strong>Lynn Baker</strong><br>CEO · Customer Experience Institute SA<br>CX University USA – South Africa<br><a href="mailto:lynn@cx-company.com">lynn@cx-company.com</a> · <a href="mailto:lynn@cxisa.co.za">lynn@cxisa.co.za</a><br><a href="tel:+27824575752">+27 82 457 5752</a><br><a href="https://www.cxinstitute.co.za">www.cxinstitute.co.za</a></div>';
const EMAIL_LOGO='<div style="background:#fff;padding:18px 24px;border-bottom:4px solid #0A8FB0"><img src="'+EMAIL_BASE+'/assets/email/cxisa-logo-2026.png" width="200" alt="CX Institute SA" style="display:block;max-width:100%;height:auto"></div>';
const PRESS_KIT=EMAIL_BASE+'/lynnbakerspeaker/organiser-press-kit/';
function brandEmail(html,booking=false){
 const kit=booking?'<div style="background:#f2f6f8;padding:20px;border-left:4px solid #0A8FB0;margin-top:20px"><h2 style="font-size:19px;color:#002D57">Lynn Baker – Event Organiser Press Kit</h2><p>Access my biography, speaker introduction and photographs for your event communications.</p><a style="display:inline-block;background:#007F98;color:white;padding:12px 18px;text-decoration:none" href="'+PRESS_KIT+'">Access the Event Organiser Press Kit</a></div>':'';
 const content=html.replace(/<!doctype html>.*?<body[^>]*>/i,'').replace(/<\/body><\/html>$/i,'').replace(/<img src="https:\/\/cxinstitute-site\.lynn-1fa\.workers\.dev\/assets\/img\/cxisa-logo-white\.png"[^>]*>/,'').replace('<p>Kind regards,<br><strong>Lynn Baker</strong><br>CX Institute SA</p>','');
 return '<!doctype html><html lang="en"><body style="margin:0;background:#f2f6f8;font-family:Inter,Arial,sans-serif;color:#002D57"><table role="presentation" width="100%"><tr><td><table role="presentation" width="100%" style="max-width:680px;margin:auto;background:white"><tr><td>'+EMAIL_LOGO+content+'</td></tr><tr><td style="padding:0 24px 24px">'+kit+EMAIL_CONTACT+'<div style="margin:24px 0"><a href="https://www.lynnbakerspeaker.com/" style="display:inline-block;background:#007F98;color:#ffffff;padding:14px 22px;text-decoration:none;font-weight:bold;border-radius:5px">Visit Lynn Baker Speaker Website</a><p style="font-size:12px"><a href="https://www.lynnbakerspeaker.com/" style="color:#002D57">www.lynnbakerspeaker.com</a></p></div>'+'</td></tr></table></td></tr></table></body></html>';
}

export function createHandler(send = fetch) {
  return {
    async fetch(request, env) {
      const url = new URL(request.url);
      if (url.pathname !== '/api/enquiry' && url.pathname !== '/api/keynote-enquiry' && url.pathname !== '/api/keynote-booking') {
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

      if (url.pathname === '/api/keynote-enquiry' || url.pathname === '/api/keynote-booking') {
        const booking=url.pathname === '/api/keynote-booking';
        const {fields,errors}=booking?validateBooking(data):validateKeynote(data);
        if (errors.length) return json({ok:false,error:'invalid',fields:errors},400);
        if (!env.RESEND_API_KEY || !validEmail(env.FROM_EMAIL) || !validEmail(env.TO_EMAIL)) return json({ok:false,error:'not_configured'},503);
        const {subject,text,html}=booking?buildBookingEmail(fields):buildKeynoteEmail(fields);
        try {
          // Resend supports sending the same message to the organiser and CXISA.
          // Both recipients must be accepted before the page shows success.
          const res=await send('https://api.resend.com/emails',{
            method:'POST',
            headers:{Authorization:`Bearer ${env.RESEND_API_KEY}`,'Content-Type':'application/json'},
            body:JSON.stringify({from:`CX Institute SA <${env.FROM_EMAIL}>`,to:booking?[...new Set([fields.email,'lynn@cx-company.com'])]:[env.TO_EMAIL,fields.email],reply_to:booking?'lynn@cx-company.com':fields.email,subject,text:text+(booking?'\n\nEvent Organiser Press Kit: '+PRESS_KIT:'')+'\n\nLynn Baker | +27 82 457 5752 | lynn@cx-company.com | www.cxinstitute.co.za',html:brandEmail(html,booking)}),
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
            html: brandEmail(html)
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

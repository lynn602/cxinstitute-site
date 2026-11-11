# cxinstitute.co.za

Public website for CX Institute SA, served by Cloudflare Workers (worker `cxinstitute-site`).

- `public/` – the site (plain HTML/CSS, no build step). Homepage: 01 Inspire · 02 Experience · 03 Embed.
- `src/index.js` – the Worker: serves `public/` and handles `POST /api/enquiry`, which emails the enquiry form to `TO_EMAIL` via Resend (Reply-To = the visitor).
- `tests/` – `npm test` checks the enquiry endpoint (validation, escaping, spam traps, failures).

## Enquiry form settings
In Cloudflare → Workers & Pages → cxinstitute-site → Settings → Variables and Secrets, add as **Secret**:
- `RESEND_API_KEY` – API key from resend.com
- `FROM_EMAIL` – a sender on a domain verified in Resend (e.g. the one touchpoints-mailer uses)

`TO_EMAIL` (lynn@cx-company.com) is set in `wrangler.jsonc`. Until the secrets exist, the form shows visitors Lynn's email and phone instead.

Brand: navy #173C68, teal #3EA69D, game blue #1990B2 (game sections only). Montserrat headings, Inter body.

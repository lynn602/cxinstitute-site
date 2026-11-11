# cxinstitute.co.za

Public website for CX Institute SA. Plain HTML/CSS (no build step), served by Cloudflare Workers static assets.

- `public/index.html` – homepage (01 Inspire · 02 Experience · 03 Embed)
- `public/assets/` – styles, self-hosted Montserrat + Inter, images from the brochures

Brand: navy #173C68, teal #3EA69D, game blue #1990B2 (game sections only). Montserrat headings, Inter body.

Deploy: connect this repo in Cloudflare → Workers & Pages → Create → Import a repository. No build command; deploy command `npx wrangler deploy`.

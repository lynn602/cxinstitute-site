#!/usr/bin/env python3
"""Builds the CX Keynotes pages (public/keynotes/...) from tools/keynotes_content.py.

The menu icons, enquiry form and footer are copied from public/index.html so every
page stays in step with the homepage. Run after editing content or the homepage:
    python3 tools/build_keynotes.py
"""
import html
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
from keynotes_content import (CAL_URL, CREDENTIALS, FAQS, FORMATS, KEYNOTES, LINKEDIN_URL,  # noqa: E402
                              LOGOS, PAGES, TESTIMONIALS, WHATSAPP_URL, YOUTUBE_ID)

PUBLIC = os.path.join(ROOT, "public")
HOME = open(os.path.join(PUBLIC, "index.html"), encoding="utf-8").read()
SITE = "https://www.cxinstitute.co.za"


def e(text):
    return html.escape(text, quote=True)


def absolutise(fragment):
    fragment = fragment.replace('src="assets/', 'src="/assets/').replace('href="assets/', 'href="/assets/')
    fragment = re.sub(r'href="#(inspire|experience|embed|about|offerings)"', r'href="/#\1"', fragment)
    return fragment.replace('href="keynotes/"', 'href="/keynotes/"')


SPRITE = HOME[HOME.index('<svg width="0" height="0"'):HOME.index("</svg>", HOME.index('<svg width="0" height="0"')) + 6]
FORM = HOME[HOME.index('<div class="enquire" id="enquire">'):HOME.index('\n      <div class="contact-card">')]
FOOTER = absolutise(HOME[HOME.index('<footer class="site-footer">'):HOME.index("</footer>") + 9])


def heading(pair, tag="h2", cls=""):
    plain, hl = pair
    c = f' class="{cls}"' if cls else ""
    return f'<{tag}{c}>{e(plain)} <span class="hl">{e(hl)}</span></{tag}>'


def header(active_home=False):
    return f'''<header class="site-header">
  <div class="wrap">
    <a class="brand" href="/" aria-label="CX Institute SA home">
      <img src="/assets/img/cxisa-logo-white.png" alt="CXiSA – Customer Experience Institute" width="107" height="44">
    </a>
    <button class="nav-toggle" aria-label="Open menu" aria-expanded="false" aria-controls="nav">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M4 7h16M4 12h16M4 17h16"/></svg>
    </button>
    <nav class="nav" id="nav" aria-label="Main">
      <a href="/#inspire"><span class="num">01</span>Inspire</a>
      <a href="/#experience"><span class="num">02</span>Experience</a>
      <a href="/#embed"><span class="num">03</span>Embed</a>
      <a href="/keynotes/"{' aria-current="page"' if active_home else ''}>CX Keynotes</a>
      <a href="/#about">About</a>
      <a class="btn btn-teal" href="#enquire">Let's talk</a>
    </nav>
  </div>
</header>'''


def page(title, desc, path, body, interest="keynote", og_image="/assets/img/keynotes/b2b-card.jpg", active_home=False):
    form = FORM.replace('<form class="enquire-form" id="enquire-form" novalidate>',
                        f'<form class="enquire-form" id="enquire-form" data-default-interest="{interest}" novalidate>')
    body = body.replace("{{FORM}}", form)
    return f'''<!DOCTYPE html>
<html lang="en-ZA">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{e(title)}</title>
  <meta name="description" content="{e(desc)}">
  <link rel="canonical" href="{SITE}{path}">
  <meta property="og:title" content="{e(title)}">
  <meta property="og:description" content="{e(desc)}">
  <meta property="og:type" content="website">
  <meta property="og:url" content="{SITE}{path}">
  <meta property="og:image" content="{SITE}{og_image}">
  <meta name="theme-color" content="#173C68">
  <link rel="icon" type="image/png" href="/assets/img/favicon.png">
  <link rel="preload" href="/assets/fonts/montserrat-latin-600-normal.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="preload" href="/assets/fonts/inter-latin-400-normal.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="stylesheet" href="/assets/css/site.css">
</head>
<body>

{SPRITE}

{header(active_home)}

<main>
{body}
</main>

{FOOTER}
<script src="/assets/js/site.js"></script>
</body>
</html>
'''


# ---------- shared blocks ----------

def sec_head(eyebrow, pair, intro=None, tag="h2"):
    out = f'<p class="eyebrow">{e(eyebrow)}</p>\n{heading(pair, tag)}'
    if intro:
        out += f'\n<p class="lead">{e(intro)}</p>'
    return out


def showreel(soft=False):
    return f'''<section class="section dark kn-showreel">
  <div class="wrap narrow">
    {sec_head("See Lynn in action", ("A glimpse of the", "stage experience."))}
    <div class="video" data-youtube="{YOUTUBE_ID}">
      <button type="button" class="video-play" aria-label="Play the Lynn Baker showreel">
        <img src="/assets/img/keynotes/lynn-keynote-stage.jpg" alt="Lynn Baker on stage — play the showreel" loading="lazy">
        <span class="play-icon" aria-hidden="true"><svg viewBox="0 0 24 24"><path d="M8 5v14l11-7z" fill="currentColor"/></svg></span>
        <span class="play-label">Watch the showreel</span>
      </button>
    </div>
    <p class="center"><a class="text-link" href="https://www.youtube.com/watch?v={YOUTUBE_ID}" target="_blank" rel="noopener">Watch on YouTube →</a></p>
  </div>
</section>'''


def testimonials():
    cards = "\n".join(f'''      <figure class="tcard"><blockquote>{e(q)}</blockquote><figcaption>— {e(a)}</figcaption></figure>''' for q, a in TESTIMONIALS)
    return f'''<section class="section" id="testimonials">
  <div class="wrap">
    {sec_head("What event planners & executives say", ("Booked by the people who", "know the room."))}
    <div class="tgrid">
{cards}
    </div>
  </div>
</section>'''


def logos():
    items = "\n".join(f'      <li><img src="/assets/img/logos/{f}.png" alt="{e(n)} logo" loading="lazy"></li>' for f, n in LOGOS)
    return f'''<section class="logo-band" aria-label="Trusted by leading organisations">
  <div class="wrap">
    <p class="eyebrow center-eyebrow">Trusted by leading organisations</p>
    <ul class="logo-row">
{items}
    </ul>
  </div>
</section>'''


def formats(first=None, soft=True):
    rows = list(FORMATS)
    if first:
        rows[0] = (first[0], first[1], None)
    cards = []
    for t, b, link in rows:
        l = f'<a class="text-link" href="{e(link[1])}" target="_blank" rel="noopener">{e(link[0])} →</a>' if link else ""
        cards.append(f'      <div class="fcard"><h3>{e(t)}</h3><p>{e(b)}</p>{l}</div>')
    return f'''<section class="section{' soft' if soft else ''}" id="formats">
  <div class="wrap">
    {sec_head("Formats & delivery", ("A keynote shaped for your audience, your event and", "your outcomes."))}
    <div class="fgrid">
{chr(10).join(cards)}
    </div>
  </div>
</section>'''


def contact(pair, intro=None, closing=None):
    intro = intro or "Every keynote is tailored to your industry, audience and business context. Share a few details and we'll come back with availability, formats and a proposal."
    return f'''<section class="section dark" id="contact">
  <div class="wrap">
    <p class="eyebrow">Send enquiry / book keynote</p>
    {heading(pair, "h2")}
    <p class="lead">{e(intro)}</p>
    <div class="quick-contact">
      <a class="btn btn-teal" href="{e(CAL_URL)}" target="_blank" rel="noopener">Book a Discovery Call <svg><use href="#i-arrow"/></svg></a>
      <a class="btn btn-ghost" href="mailto:lynn@cx-company.com?subject=Keynote%20Booking%20Enquiry">Email Lynn</a>
      <a class="btn btn-ghost" href="tel:+27824575752">Call +27 82 457 5752</a>
      <a class="btn btn-ghost" href="{e(WHATSAPP_URL)}" target="_blank" rel="noopener">WhatsApp Lynn</a>
      <a class="btn btn-ghost" href="{e(LINKEDIN_URL)}" target="_blank" rel="noopener">Connect on LinkedIn</a>
    </div>
    <ul class="contact-facts">
      <li><b>Response time</b>Within 1 business day</li>
      <li><b>Based in</b>Johannesburg · Available worldwide</li>
    </ul>
      {{{{FORM}}}}
    {f'<p class="closing-line">{e(closing)}</p>' if closing else ''}
  </div>
</section>'''


# ---------- detail-page sections ----------

def s_bigidea(d):
    cols = "".join('<div class="col">' + "".join(f"<p>{e(p)}</p>" for p in col) + "</div>" for col in d["cols"])
    lq = ""
    if d.get("lead_quote"):
        q, by = d["lead_quote"]
        lq = f'<blockquote class="pull">{e(q)}<cite>— {e(by)}</cite></blockquote>'
    img = ""
    if d.get("image"):
        img = f'<img class="wide-img" src="{d["image"][0]}" alt="{e(d["image"][1])}" loading="lazy">'
    strong = f'<p class="strong-line">{e(d["strong"])}</p>' if d.get("strong") else ""
    return f'''<section class="section{' soft' if d.get('soft') else ''}">
  <div class="wrap">
    {sec_head(d["eyebrow"], d["heading"])}
    {lq}
    <div class="two-col">{cols}</div>
    {strong}
    {img}
  </div>
</section>'''


def s_numbered(d):
    items = "\n".join(f'      <li><span class="n">{i}</span><p>{e(t)}</p></li>' for i, t in enumerate(d["items"], 1))
    closing = f'<p class="strong-line center">{e(d["closing"][0])} <span class="hl">{e(d["closing"][1])}</span></p>' if d.get("closing") else ""
    return f'''<section class="section soft">
  <div class="wrap">
    {sec_head(d["eyebrow"], d["heading"])}
    <ol class="numbered">
{items}
    </ol>
    {closing}
  </div>
</section>'''


def s_quote(d):
    paras = "".join(f"<p>{e(p)}</p>" for p in d["paras"])
    return f'''<section class="section">
  <div class="wrap">
    {sec_head(d["eyebrow"], d["heading"])}
    <div class="quote-card">
      <blockquote>{e(d["quote"])}</blockquote>
      {paras}
      <p class="strong-line">{e(d["strong"])}</p>
    </div>
  </div>
</section>'''


def s_idealfor(d):
    items = "\n".join(f"        <li>{e(t)}</li>" for t in d["items"])
    link = f'<a class="text-link" href="{d["link"][0]}">{e(d["link"][1])} →</a>' if d.get("link") else ""
    return f'''<section class="section">
  <div class="wrap ideal">
    <div>
      {sec_head("Ideal for", d["heading"])}
      <ul class="ticks">
{items}
      </ul>
      {link}
    </div>
    <div class="duration-card">
      <p class="eyebrow">{e(d["duration_label"])}</p>
      <p class="duration">{e(d["duration"])}</p>
      <p>{e(d["duration_text"])}</p>
      <div class="btn-row">
        <a class="btn btn-teal" href="{e(CAL_URL)}" target="_blank" rel="noopener">Book a Discovery Call</a>
        <a class="btn btn-ghost" href="#enquire">Make an Enquiry</a>
      </div>
    </div>
  </div>
</section>'''


def s_framework(d):
    cards = "\n".join(f'      <div class="fw-card"><span class="tag">{e(t)}</span><h3>{e(h)}</h3><p>{e(b)}</p></div>' for t, h, b in d["items"])
    return f'''<section class="section dark">
  <div class="wrap">
    {sec_head(d["eyebrow"], d["heading"])}
    <div class="fw-grid">
{cards}
    </div>
  </div>
</section>'''


def s_steps(d):
    cards = "\n".join(f'      <div class="step-card"><span class="tag">{e(s)}</span><h3>{e(t)}</h3><p>{e(b)}</p></div>' for s, t, b in d["items"])
    return f'''<section class="section">
  <div class="wrap">
    {sec_head(d["eyebrow"], d["heading"], d.get("intro"))}
    <div class="step-grid">
{cards}
    </div>
  </div>
</section>'''


def s_chapters(d):
    out = []
    for eyebrow, title, body, lst in d["items"]:
        li = "".join(f"<li>{e(x)}</li>" for x in lst)
        out.append(f'<div class="chapter"><p class="eyebrow">{e(eyebrow)}</p><h3>{e(title)}</h3><p>{e(body)}</p><ul class="ticks">{li}</ul></div>')
    return f'''<section class="section soft">
  <div class="wrap chapters">
    {"".join(out)}
  </div>
</section>'''


def s_audience(d):
    chips = "".join(f"<li>{e(c)}</li>" for c in d["chips"])
    return f'''<section class="section">
  <div class="wrap">
    {sec_head(d["eyebrow"], d["heading"], d["intro"])}
    <ul class="chip-row">{chips}</ul>
    <p class="strong-line">{e(d["closing"][0])} <span class="hl">{e(d["closing"][1])}</span></p>
  </div>
</section>'''


def s_callout(d):
    return f'''<section class="section soft">
  <div class="wrap">
    <div class="callout">
      {sec_head(d["eyebrow"], d["heading"])}
      <p>{e(d["text"])}</p>
      <a class="btn btn-navy" href="#enquire">{e(d["button"])}</a>
    </div>
  </div>
</section>'''


def s_perfectfor(d):
    groups = "".join(f'<div class="pf-group"><h3>{e(h)}</h3><ul class="ticks">{"".join(f"<li>{e(i)}</li>" for i in items)}</ul></div>' for h, items in d["groups"])
    return f'''<section class="section">
  <div class="wrap">
    {sec_head(d["eyebrow"], d["heading"])}
    <div class="pf-grid">{groups}</div>
  </div>
</section>'''


RENDER = {
    "bigidea": s_bigidea, "numbered": s_numbered, "quote": s_quote, "idealfor": s_idealfor,
    "framework": s_framework, "steps": s_steps, "chapters": s_chapters, "audience": s_audience,
    "callout": s_callout, "perfectfor": s_perfectfor,
    "showreel": lambda d: showreel(), "testimonials": lambda d: testimonials(),
    "formats": lambda d: formats(d.get("first")),
}


def downloads(p):
    return f'''<a class="btn btn-ghost" href="{p["pdf"]}" download>Download PDF</a>
        <a class="btn btn-ghost" href="{p["ppt"]}" download>Download PPT</a>'''


def build_detail(k):
    p = PAGES[k["slug"]]
    path = f'/keynotes/{k["slug"]}/'
    lines = "".join(f'<p class="kn-line">{e(l)}</p>' for l in p["lines"])
    quote = f'<blockquote class="kn-quote">“{e(p["quote"])}”</blockquote>' if p.get("quote") else ""
    game = ' game' if p.get("game") else ""
    hero = f'''<section class="kn-hero{game}">
  <div class="kn-hero-media"><img src="{p["hero_image"]}" alt="{e(k["alt"])}"></div>
  <div class="wrap kn-hero-text">
    <a class="back" href="/keynotes/">← All CX Keynotes</a>
    <p class="eyebrow">{e(p["eyebrow"])} · Keynote {k["num"]}</p>
    <h1>{e(k["title"])}</h1>
    <p class="kn-sub">{e(k["subtitle"])}</p>
    {lines}
    {quote}
    <p class="lead">{e(p["intro"])}</p>
    <div class="btn-row">
        <a class="btn btn-teal" href="{e(CAL_URL)}" target="_blank" rel="noopener">Book a Discovery Call <svg><use href="#i-arrow"/></svg></a>
        <a class="btn btn-ghost" href="#enquire">Make an Enquiry / Book</a>
        {downloads(p)}
    </div>
  </div>
</section>'''
    body = [hero]
    for kind, d in p["sections"]:
        body.append(RENDER[kind](d))
    body.append(contact(p["contact_heading"], p.get("contact_intro"), p.get("closing")))
    interest = "game" if p.get("game") else "keynote"
    return page(p["seo_title"], p["seo_desc"], path, "\n\n".join(body), interest, k["image"])


def build_index():
    cards = []
    for k in KEYNOTES:
        blurb = "".join(f"<p>{e(b)}</p>" for b in k["blurb"])
        kicker = f'<p class="k-kicker">{e(k["kicker"])}</p>' if k.get("kicker") else ""
        sec = f'<a class="text-link" href="{k["secondary"][0]}">{e(k["secondary"][1])} →</a>' if k.get("secondary") else ""
        cards.append(f'''    <article class="kn-card">
      <a class="kn-card-img" href="/keynotes/{k["slug"]}/"><img src="{k["image"]}" alt="{e(k["alt"])}" loading="lazy"></a>
      <div class="kn-card-body">
        <span class="k-num">{k["num"]}</span>
        <h3><a href="/keynotes/{k["slug"]}/">{e(k["title"])}</a></h3>
        <p class="k-sub">{e(k["subtitle"])}</p>
        {kicker}
        <div class="kn-blurb">{blurb}</div>
        <div class="kn-links"><a class="btn btn-navy btn-sm" href="/keynotes/{k["slug"]}/">View the keynote <svg><use href="#i-arrow"/></svg></a>{sec}</div>
      </div>
    </article>''')
    creds = "".join(f"<li>{e(c)}</li>" for c in CREDENTIALS)
    faqs = "\n".join(f'      <details><summary>{e(q)}</summary><p>{e(a)}</p></details>' for q, a in FAQS)
    body = f'''<section class="kn-hero kn-hero-home">
  <div class="kn-hero-media"><img src="/assets/img/keynotes/b2b-card.jpg" alt="Lynn Baker delivering a customer experience keynote to a large conference audience"></div>
  <div class="wrap kn-hero-text">
    <p class="eyebrow">CX Keynotes · Customer Experience Keynote Speaker</p>
    <h1>Lynn Baker <span class="hl">Customer Experience Keynote Speaker</span></h1>
    <p class="kn-line">Customer Experience Keynotes That Shift Thinking, Change Behaviour and Drive Business Growth.</p>
    <p class="lead">An international Customer Experience speaker based in Johannesburg, South Africa, and speaking across Africa, the Middle East (including Dubai), Europe and the UK. With 25+ years specialising in Customer Experience and training from the Disney Institute, Lynn Baker is renowned for delivering keynote experiences that shift thinking and change behaviour. Combining powerful storytelling, humour, live audience interaction and practical ideas, Lynn turns Customer Experience into something audiences can see, feel and act on. No death by PowerPoint. No theory for theory's sake. Just memorable moments, fresh thinking and actionable ideas audiences can put to work the very next morning.</p>
    <div class="btn-row">
      <a class="btn btn-teal" href="{e(CAL_URL)}" target="_blank" rel="noopener">Book a Discovery Call <svg><use href="#i-arrow"/></svg></a>
      <a class="btn btn-ghost" href="#enquire">Make an Enquiry / Book</a>
    </div>
  </div>
</section>

<section class="section" id="keynotes">
  <div class="wrap">
    <p class="eyebrow">The keynotes</p>
    <h2>Each keynote. One central message. <span class="hl">Every moment your customer engages with you is an experience – make every moment count!</span></h2>
    <div class="lead stack">
      <p>Whether your audience is beginning its CX journey, navigating AI or transforming B2B client relationships, there is a keynote experience designed for the conversation your organisation needs to have now.</p>
      <p>Wherever possible, keynotes are tailored to your industry, your audience and your outcomes.</p>
      <p>Explore the keynote experiences below and let Lynn know how she can help you.</p>
    </div>
    <div class="kn-grid">
{chr(10).join(cards)}
    </div>
  </div>
</section>

{showreel()}

<section class="section" id="why-lynn">
  <div class="wrap why">
    <img src="/assets/img/keynotes/humanization-stage.jpg" alt="Lynn Baker on stage delivering the Humanization keynote" loading="lazy">
    <div>
      {sec_head("Why Lynn Baker", ("A leading", "Customer Experience Strategist."))}
      <p>With more than 25 years specialising in Customer Experience, Lynn Baker is a leading keynote speaker and business strategist.</p>
      <p>A Disney Institute trained CX speaker, Lynn served as Chair of Judges for the International Customer Experience Awards for six years, and is the founder and CEO of the Customer Experience Institute South Africa (CX Institute SA) and CX University SA. She was named in the Top 50 Women in CX and speaks as much on customer service as on customer experience strategy — a genuinely non-PowerPoint keynote speaker.</p>
      <p>Her presentations combine powerful storytelling, humour, practical business examples, audience interaction and actionable insights that challenge conventional thinking and inspire immediate action. Lynn doesn't simply talk about Customer Experience — she helps audiences understand it, experience it, and most importantly, live it.</p>
      <ul class="cred-grid">{creds}</ul>
    </div>
  </div>
</section>

{formats()}

{testimonials()}

{logos()}

<section class="section soft" id="faqs">
  <div class="wrap narrow">
    {sec_head("Frequently asked", ("Booking Lynn,", "answered."))}
    <div class="faq">
{faqs}
    </div>
  </div>
</section>

{contact(("Tell us about your event.", "We'll be in touch within one business day."))}'''
    return page("CX Keynotes | Lynn Baker – Customer Experience Keynote Speaker | CX Institute SA",
                "Customer experience keynotes by Lynn Baker: Welcome to the Age of Experience, B2B Proof of Value (CPX), Welcome to the World of Humanization, and the CX Keynote + The Customer Journey Simulation Game.",
                "/keynotes/", body, "keynote", active_home=True)


def write(rel, text):
    path = os.path.join(PUBLIC, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    print("wrote", rel)


if __name__ == "__main__":
    write("keynotes/index.html", build_index())
    for k in KEYNOTES:
        write(f'keynotes/{k["slug"]}/index.html', build_detail(k))

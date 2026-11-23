#!/usr/bin/env python3
"""Build the CX University page with the shared site header and footer."""
from build_keynotes import e, page, write

ROUTE = "/cx-university-online-training-courses/"
IMAGES = "/assets/img/cx-university"
SHOP = "https://cxuniversity.com/shop-south-africa/"

COURSES = [
    (
        "cxs", "Customer Experience Specialist (CXS)™", "USD 175 · Self-paced · 3 months’ access",
        "Study five CX competencies at your own pace. Each module includes a quiz, and the certification assessment unlocks when you complete the coursework. No prerequisites.",
        "https://cxuniversity.com/product/customer-experience-specialist-cxs-program-south-africa/",
    ),
    (
        "roadmap", "90-Day Roadmap to CXS™", "USD 595 · Guided cohort · 6 months’ access",
        "Work towards the same CXS credential with a cohort, live expert sessions and independent study. The programme includes CCXP exam preparation. Check the South Africa catalogue for cohort dates.",
        SHOP,
    ),
    (
        "ccxp", "CCXP Exam Prep", "USD 139 · Self-paced · 6 months’ access",
        "Review the CXPA’s five pillars and build exam confidence with practice questions and feedback. The CCXP certification exam is administered separately by the CXPA.",
        "https://cxuniversity.com/product/ccxp-exam-prep-south-africa/",
    ),
    (
        "mapping", "Applied Customer Journey Mapping", "USD 750 · Blended learning · 6 months’ access",
        "Develop a journey map for a real challenge through six online courses, expert coaching and virtual review sessions. Use JourneyTrack™ during the programme to build and refine your map.",
        SHOP,
    ),
    (
        "patient", "Patient Experience Mastery", "USD 417 · Self-paced · 6 months’ access",
        "Study patient-centred strategy, culture, measurement, design and patient feedback. Complete the five courses and pass the assessment to earn the Patient Experience Specialist (PXS)™ credential.",
        SHOP,
    ),
    (
        "ai", "X in the Age of AI", "USD 995 · Instructor-led online",
        "Explore how to apply AI to customer journeys, personalisation and decision-making. Learn to evaluate organisational readiness and move from pilots to responsible deployment.",
        "https://cxuniversity.com/product/ai-and-cx-leadership-course-south-africa/",
    ),
]


def photo(name, eager=False):
    loading = 'fetchpriority="high"' if eager else 'loading="lazy"'
    return f'<img src="{IMAGES}/{e(name)}.webp" alt="" {loading} decoding="async">'


def course_card(image, title, facts, description, url):
    return f'''<article class="kn-card">
  <div class="kn-card-img">{photo(image)}</div>
  <div class="kn-card-body">
    <p class="k-kicker">{e(facts)}</p>
    <h3>{e(title)}</h3>
    <div class="kn-blurb"><p>{e(description)}</p></div>
    <div class="kn-links"><a class="btn btn-navy" href="{e(url)}" aria-label="{e("View enrolment options for " + title)}">View enrolment options</a></div>
  </div>
</article>'''


def build():
    cards = "\n".join(course_card(*course) for course in COURSES)
    body = f'''<section class="opener navy kn-hero" aria-labelledby="university-title">
  <div class="opener-media">{photo("hero", eager=True)}</div>
  <div class="opener-text">
    <img src="{IMAGES}/logo.webp" alt="CX University" width="175" style="height:auto;margin-bottom:18px">
    <p class="eyebrow">CX University · South Africa</p>
    <h1 id="university-title">Online customer experience courses and certification</h1>
    <p>Build practical CX skills with CX University, a training partner of CX Institute SA. Choose independent study, guided cohort learning or a specialist course for your next step.</p>
    <div class="btn-row">
      <a class="btn btn-teal" href="#courses">Explore courses</a>
      <a class="btn btn-ghost" href="#enquire">Ask about a course</a>
    </div>
  </div>
</section>
<section class="section" id="courses" aria-labelledby="courses-title">
  <div class="wrap">
    <p class="eyebrow">Study with CX University</p>
    <h2 id="courses-title">CX University courses</h2>
    <p class="lead">Courses are priced in US dollars. Enrol and pay directly through the <a href="{SHOP}">CX University South Africa catalogue</a>, where you can confirm current pricing and availability.</p>
    <div class="kn-grid">
      {cards}
    </div>
  </div>
</section>
<section class="section soft" aria-labelledby="cxs-topics">
  <div class="wrap two-col">
    <div>
      <p class="eyebrow">CXS certification</p>
      <h2 id="cxs-topics">What you’ll learn</h2>
      <p>Both CXS pathways cover five areas of CX practice. Apply the learning to turn customer insights into measurable improvements and bring colleagues into the work.</p>
      <ul>
        <li>Set a CX strategy and put it into practice.</li>
        <li>Build a customer-focused culture with clear accountability.</li>
        <li>Choose meaningful measures and analyse results.</li>
        <li>Design and improve customer experiences.</li>
        <li>Use customer feedback and evidence to guide decisions.</li>
      </ul>
    </div>
    <div class="kn-card-img">{photo("career")}</div>
  </div>
</section>
<section class="section" aria-labelledby="fit-title">
  <div class="wrap">
    <h2 id="fit-title">Choose the right course for your goals</h2>
    <p class="lead">The courses are suited to CX practitioners, marketing and customer success leaders, consultants and business owners who want to improve how their organisations serve customers.</p>
    <div class="pathway">
      <article class="path-card">{photo("learn")}<div class="body"><h3>Lead CX initiatives</h3><p>Choose a CXS pathway to build a foundation in CX strategy, measurement and improvement.</p></div></article>
      <article class="path-card">{photo("training")}<div class="body"><h3>Prepare for the CCXP exam</h3><p>Use the exam prep course to structure your study and practise applying the CXPA competencies.</p></div></article>
      <article class="path-card">{photo("enrol")}<div class="body"><h3>Develop specialist skills</h3><p>Apply what you learn to journey mapping, patient experience or AI-led CX improvement.</p></div></article>
    </div>
    <figure class="pull">
      <p>Jeff Hursey, a Cisco Systems contact centre consulting systems engineer, reported that the training helped him prepare for the CCXP exam and gave him tools he could apply in his work.</p>
      <figcaption>CX University learner feedback</figcaption>
    </figure>
    <p><a class="text-link" href="https://el281.infusionsoft.app/app/form/x-in-the-age-of-ai-course-guide">Request the X in the Age of AI course guide →</a></p>
  </div>
</section>
<section class="section dark" id="enquire" aria-labelledby="university-contact">
  <div class="wrap">
    <h2 id="university-contact">Talk to CX University South Africa</h2>
    <p class="lead">Ask Lynn Baker about course selection, certification or training for your team.</p>
    <div class="btn-row">
      <a class="btn btn-teal" href="mailto:lynn@cx-company.com?subject=CX%20University%20enquiry">Email Lynn</a>
      <a class="btn btn-ghost" href="tel:+27824575752">Call +27 82 457 5752</a>
    </div>
  </div>
</section>'''
    return page(
        "CX University Online Courses & Certification | CX Institute SA",
        "Compare CX University’s online courses for South African learners, including CXS certification, CCXP exam preparation, journey mapping, patient experience and AI.",
        ROUTE, body, og_image=IMAGES + "/hero.webp",
    )


if __name__ == "__main__":
    write(ROUTE.strip("/") + "/index.html", build())

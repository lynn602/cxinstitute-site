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


DETAILS = {
    "cxs": (
        "customer-experience-specialist",
        "CX practitioners and professionals moving into CX who want a recognised credential and the flexibility to study independently.",
        [
            "Translate customer needs and business priorities into a CX strategy.",
            "Build a customer-focused culture and define who is accountable for delivery.",
            "Choose relevant CX measures and interpret the results.",
            "Use design and improvement methods to improve customer interactions.",
            "Turn customer feedback and other evidence into decisions.",
        ],
        "Work through five online modules over three months. Quizzes reinforce the material. The CXS assessment becomes available after you complete the coursework. No prerequisites are required.",
    ),
    "roadmap": (
        "90-day-roadmap-to-cxs",
        "Professionals who want live expert guidance, a study cohort and a structured route to the CXS credential.",
        [
            "Connect CX strategy with day-to-day business decisions.",
            "Define the behaviours and responsibilities that support a customer-focused culture.",
            "Measure CX performance and identify opportunities for improvement.",
            "Apply customer research and design methods to priority journeys.",
            "Use customer insights to influence stakeholders and guide action.",
        ],
        "Combine online study with live virtual sessions. You have six months’ access to course materials. The programme includes CCXP exam preparation. Check the enrolment page for the next cohort and session dates.",
    ),
    "ccxp": (
        "ccxp-exam-prep",
        "Experienced CX practitioners who intend to sit the CXPA’s Certified Customer Experience Professional exam.",
        [
            "Review strategy, culture and accountability, and the role of customer evidence.",
            "Practise questions that cover CX measurement, analysis, improvement and design.",
            "Use practice exams and answer explanations to identify areas for further study.",
        ],
        "Study independently with online materials, interactive exercises and practice assessments for six months. The CXPA handles CCXP exam registration, eligibility and certification separately.",
    ),
    "mapping": (
        "applied-customer-journey-mapping",
        "CX practitioners, consultants and cross-functional teams who want to use a journey map to address a real service challenge.",
        [
            "Choose a journey, set its scope and gather customer evidence.",
            "Visualise customer actions, needs and pain points across touchpoints.",
            "Identify which moments need attention and bring the relevant teams into the work.",
            "Build and refine your own journey map using JourneyTrack during the course.",
        ],
        "Work through six online courses with practical resources, expert coaching and virtual review sessions. You have six months to complete the programme.",
    ),
    "patient": (
        "patient-experience-mastery",
        "Healthcare professionals and patient experience leaders who want to improve how patients experience care.",
        [
            "Develop a patient experience strategy and clarify responsibilities for delivery.",
            "Build a patient-centred culture across care and support teams.",
            "Select patient experience measures and interpret the results.",
            "Use design methods and patient feedback to improve care interactions.",
        ],
        "Study five online courses at your own pace with six months’ access. Complete the coursework and pass the assessment to earn the Patient Experience Specialist (PXS) credential. No prerequisites are listed.",
    ),
    "ai": (
        "x-in-the-age-of-ai",
        "CX leaders, consultants and teams evaluating where AI can improve service, customer journeys and operations.",
        [
            "Identify where AI can support personalisation, service decisions and automation.",
            "Assess your organisation’s readiness for AI across the customer journey.",
            "Use customer signals to design responsive journeys while preserving human support.",
            "Plan how to move from pilots to wider adoption with clear governance and accountability.",
        ],
        "Learn online with instructor guidance and apply the frameworks to your organisation. Confirm dates and access terms on the enrolment page.",
    ),
}


def photo(name, eager=False):
    loading = 'fetchpriority="high"' if eager else 'loading="lazy"'
    return f'<img src="{IMAGES}/{e(name)}.webp" alt="" {loading} decoding="async">'


def course_card(image, title, facts, description, _):
    url = ROUTE + DETAILS[image][0] + "/"
    return f'''<article class="kn-card">
  <div class="kn-card-img">{photo(image)}</div>
  <div class="kn-card-body">
    <p class="k-kicker">{e(facts)}</p>
    <h3>{e(title)}</h3>
    <div class="kn-blurb"><p>{e(description)}</p></div>
    <div class="kn-links"><a class="btn btn-navy" href="{e(url)}" aria-label="{e("View course details for " + title)}">View course details</a></div>
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
    <p class="lead">Courses are priced in US dollars. Open a course to see what you’ll learn, who it’s for and how to enrol.</p>
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


def build_detail(image, title, facts, description, enrol_url):
    slug, audience, topics, format_description = DETAILS[image]
    topics_html = "\n".join(f"      <li>{e(topic)}</li>" for topic in topics)
    guide = (
        '<p><a class="text-link" href="https://el281.infusionsoft.app/app/form/x-in-the-age-of-ai-course-guide">Request the course guide →</a></p>'
        if image == "ai" else ""
    )
    body = f'''<section class="opener navy kn-hero" aria-labelledby="course-title">
  <div class="opener-media">{photo(image, eager=True)}</div>
  <div class="opener-text">
    <a class="back" href="{ROUTE}#courses">← All CX University courses</a>
    <p class="eyebrow">{e(facts)}</p>
    <h1 id="course-title">{e(title)}</h1>
    <p>{e(description)}</p>
  </div>
</section>
<section class="section" aria-labelledby="course-topics">
  <div class="wrap narrow">
    <h2 id="course-topics">What you’ll learn</h2>
    <ul>
{topics_html}
    </ul>
    <h2>Who it’s for</h2>
    <p>{e(audience)}</p>
    <h2>How the course works</h2>
    <p>{e(format_description)}</p>
{guide}
  </div>
</section>
<section class="section dark" id="enquire" aria-labelledby="course-enrol">
  <div class="wrap narrow">
    <h2 id="course-enrol">Enrol with CX University</h2>
    <p class="lead">Confirm current pricing and availability, then enrol and pay through CX University.</p>
    <div class="btn-row">
      <a class="btn btn-teal" href="{e(enrol_url)}">ENROL NOW</a>
      <a class="btn btn-ghost" href="mailto:lynn@cx-company.com?subject=CX%20University%20course%20enquiry">Ask Lynn a question</a>
    </div>
  </div>
</section>'''
    return page(
        title + " | CX University | CX Institute SA", description,
        ROUTE + slug + "/", body, og_image=IMAGES + "/" + image + ".webp",
    )


if __name__ == "__main__":
    write(ROUTE.strip("/") + "/index.html", build())
    for course in COURSES:
        write(ROUTE.strip("/") + "/" + DETAILS[course[0]][0] + "/index.html", build_detail(*course))

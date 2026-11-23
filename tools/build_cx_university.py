#!/usr/bin/env python3
"""Build the CX University page with the shared site header and footer."""
from build_keynotes import e, page, write

ROUTE = "/cx-university-online-training-courses/"
IMAGES = "/assets/img/cx-university"
SHOP = "https://cxuniversity.com/shop-south-africa/"
HOME_BUTTON = '<p><a class="btn btn-ghost" href="/">← Back to home</a></p>'

COURSES = [
    (
        "cxs", "Customer Experience Specialist (CXS)™", "USD 175 · Self-paced · 3 months’ access",
        "Study five CX competencies at your own pace. Each module includes a quiz, and the certification assessment unlocks when you complete the coursework. No prerequisites.",
        SHOP,
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
        SHOP,
    ),
]


DETAILS = {
    "cxs": (
        "customer-experience-specialist",
        "",
        [
            "Strategy in Action – Develop and execute CX strategies that drive measurable business impact.",
            "Culture and Accountability – Build a strong, customer-first culture across your organization.",
            "Metrics and Analysis – Measure CX success with key data insights and analytics.",
            "Improvement and Design – Use design thinking to continuously refine and enhance customer experiences.",
            "Voice of the Customer & Intelligence – Leverage customer insights to shape strategic decisions",
        ],
        "This program is entirely self-contained and built for independent study, allowing you to learn and review material at your own pace and schedule. We recommend that you work through each module sequentially. This program includes five focused modules covering the most important CX best practices and applied competencies used by high-performing teams. Every module ends with a quiz to reinforce learning and track your progress.",
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
    {HOME_BUTTON}
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


def build_cxs_detail(image, description, enrol_url):
    slug, _, topics, access = DETAILS[image]
    topics_html = "\n".join(f"      <li>{e(topic)}</li>" for topic in topics)
    body = f'''<section class="opener navy kn-hero" aria-labelledby="course-title">
  <div class="opener-media">{photo(image, eager=True)}</div>
  <div class="opener-text">
    {HOME_BUTTON}
    <a class="back" href="{ROUTE}#courses">← All CX University courses</a>
    <h1 id="course-title">Customer Experience Specialist (CXS)</h1>
    <p class="kn-sub">Online Certification course</p>
    <p><strong>Price USD 175.00</strong><br>
      Self-paced online course / 3 months’ access<br>
      Enrol and pay online</p>
    <p>Earn your Customer Experience Specialist (CXS)™ certificate by completing the online program and passing the certification exam available directly inside your LMS portal once you finish the coursework. This isn’t “just another course.” It’s a practical, career-boosting program designed to help you build CX confidence, speak the language of leadership, and drive measurable results across teams, departments, and customer touchpoints.</p>
  </div>
</section>
<section class="section" aria-labelledby="course-topics">
  <div class="wrap narrow">
    <h2 id="course-topics">What You’ll Learn</h2>
    <p>The Customer Experience Specialist CXS online course is structured into five expert-developed modules, covering every critical aspect of customer experience:</p>
    <ul>
{topics_html}
    </ul>
    <p>As a certified Customer Experience Specialist (CXS)™, you’ll be equipped to:</p>
    <ul>
      <li>Turn customer insights into clear, strategic actions</li>
      <li>Improve experiences that increase loyalty, retention, and revenue</li>
      <li>Influence internal stakeholders with the right CX frameworks and metrics</li>
      <li>Lead CX initiatives at any level, without needing a fancy title</li>
    </ul>
    <h2>Course Access</h2>
    <p>{e(access)}</p>
    <p>Your purchase includes:</p>
    <ul>
      <li>3 months of access to all online modules</li>
      <li>Access to the Customer Experience Specialist (CXS)™ certification exam (unlocked after completing the courses)</li>
      <li>A complete learning path built to help you finish strong and certify with confidence</li>
    </ul>
    <h2>Pre-Requisites</h2>
    <p>No prerequisites are necessary as this course covers all CX Core Competencies.</p>
  </div>
</section>
<section class="section dark" id="enquire" aria-labelledby="course-enrol">
  <div class="wrap narrow">
    <h2 id="course-enrol">Enrol with CX University</h2>
    <div class="btn-row">
      <a class="btn btn-teal" href="{e(enrol_url)}">Enrol on CXS Course</a>
      <a class="btn btn-ghost" href="mailto:lynn@cx-company.com?subject=CX%20University%20course%20enquiry">Ask Lynn a question</a>
    </div>
  </div>
</section>'''
    return page(
        "Customer Experience Specialist (CXS)™ | CX University | CX Institute SA",
        description, ROUTE + slug + "/", body, og_image=IMAGES + "/" + image + ".webp",
    )


def build_roadmap_detail(image, title, description, enrol_url):
    slug = DETAILS[image][0]
    topics_html = "\n".join(f"      <li>{e(topic)}</li>" for topic in DETAILS["cxs"][2])
    body = f'''<section class="opener navy kn-hero" aria-labelledby="course-title">
  <div class="opener-media">{photo(image, eager=True)}</div>
  <div class="opener-text">
    {HOME_BUTTON}
    <a class="back" href="{ROUTE}#courses">← All CX University courses</a>
    <h1 id="course-title">90 Day Roadmap to<br>Customer Experience Specialist (CXS)</h1>
    <p class="kn-sub">Blended online learning and virtual instructor led sessions</p>
    <p><strong>Price U$D595.00</strong><br>
      Self-paced online course / 6 months access<br>
      Enroll and pay online</p>
  </div>
</section>
<section class="section" aria-labelledby="course-benefits">
  <div class="wrap narrow">
    <p>In today’s competitive business landscape, exceptional customer experience (CX) isn’t just a luxury—it’s a necessity. CX Professionals help build loyalty, advocacy, and repeat customers. Companies are investing more than ever in CX professionals who can design, implement, and optimize experiences that drive loyalty and revenue. Bonus access to our CCXP Exam Prep Course (a $199 value) - ready for when you choose to pursue the CXPA’s Certified Customer Experience Professional (CCXP) designation.</p>
    <p>The 90-Day Roadmap to CXS is your gateway to becoming a certified expert in customer experience. This self-paced, online course empowers you with the essential skills, strategies, and frameworks to lead CX initiatives with confidence and authority.</p>
    <h2 id="course-benefits">Course benefits</h2>
    <ul>
      <li>Gain industry-recognized certification – Earn the Customer Experience Specialist (CXS) ™ credential to enhance your credibility and set yourself apart.</li>
      <li>Master essential CX skills – Learn to create strategies, measure success, and build a customer-centric culture.</li>
      <li>Advance your career – Stand out for promotions, new job opportunities, and leadership roles in CX.</li>
      <li>Blended learning – A combination of instructor-led and self-paced learning with six months of online access to complete the course.</li>
      <li>You will have access to complete the course for 6 months from the starting date.</li>
    </ul>
    <h2>What You’ll Learn</h2>
    <p>The 90-Day Roadmap to CXS is structured into five expert-developed modules, covering every critical aspect of customer experience:</p>
    <ul>
{topics_html}
    </ul>
    <h2>Who Should Enroll?</h2>
    <p>This course is ideal for:</p>
    <ul>
      <li>CX professionals looking to gain a formal credential and advance in their careers.</li>
      <li>Marketing &amp; Customer Success leaders who want to influence revenues, profits, cost reduction, and easy customer acquisition and retention.</li>
      <li>Business owners &amp; entrepreneurs aiming to differentiate their brand through outstanding CX.</li>
      <li>Consultants &amp; strategists seeking a deeper understanding of customer behavior.</li>
    </ul>
  </div>
</section>
<section class="section dark" id="enquire" aria-labelledby="course-enrol">
  <div class="wrap narrow">
    <h2 id="course-enrol">Enrol with CX University</h2>
    <div class="btn-row">
      <a class="btn btn-teal" href="{e(enrol_url)}">Enrol in 90 Day Roadmap to CXS course</a>
      <a class="btn btn-ghost" href="mailto:lynn@cx-company.com?subject=CX%20University%20course%20enquiry">Ask Lynn a question</a>
    </div>
  </div>
</section>'''
    return page(
        title + " | CX University | CX Institute SA", description,
        ROUTE + slug + "/", body, og_image=IMAGES + "/" + image + ".webp",
    )


def build_mapping_detail(image, title, description, enrol_url):
    slug = DETAILS[image][0]
    body = f'''<section class="opener navy kn-hero" aria-labelledby="course-title">
  <div class="opener-media">{photo(image, eager=True)}</div>
  <div class="opener-text">
    {HOME_BUTTON}
    <a class="back" href="{ROUTE}#courses">← All CX University courses</a>
    <h1 id="course-title">Applied Customer Journey Mapping course</h1>
    <p><strong>Price U$D750.00</strong><br>
      Self-paced online course / 6 months access<br>
      Enrol and pay online</p>
  </div>
</section>
<section class="section" aria-labelledby="course-overview">
  <div class="wrap narrow">
    <h2 id="course-overview">Why Take the Applied Customer Journey Mapping?</h2>
    <p>Customer journey mapping is an essential methodology to build your organization’s customer-centricity. Journey maps serve as guides to help you anticipate your customers’ needs, deliver excellent experiences, and promote collaboration across silos.</p>
    <p>Customer journey maps yield deep insights into which touchpoints matter the most to your customers. With all of your stakeholders focusing on the customer experience, you can move closer to delivering on your brand promise.</p>
    <p>Visualizing the Customer Experience with journey maps is becoming ever more important in modern organizations. With this course, you will develop mastery in journey mapping methodology and direct application to your own customers’ challenges.</p>
    <h2>Course Highlights</h2>
    <ul>
      <li>Six online courses packed with practical playbooks, seminal articles, and expert videos.</li>
      <li>Free access to JourneyTrack™, a comprehensive customer journey mapping platform, to help you create, manage, and iterate on your journey maps.</li>
      <li>Six post-review virtual meet-up classes to ensure continuous learning and feedback.</li>
      <li>Guidance and coaching from CX experts to support your journey mapping journey.</li>
      <li>Build and deliver your own map, tailored to your organization’s specific needs.</li>
      <li>You will have access to complete the course for 6 months from the starting date.</li>
    </ul>
  </div>
</section>
<section class="section dark" id="enquire" aria-labelledby="course-enrol">
  <div class="wrap narrow">
    <h2 id="course-enrol">Enrol with CX University</h2>
    <div class="btn-row">
      <a class="btn btn-teal" href="{e(enrol_url)}">Enrol in Applied Customer Journey Mapping Course</a>
      <a class="btn btn-ghost" href="mailto:lynn@cx-company.com?subject=CX%20University%20course%20enquiry">Ask Lynn a question</a>
    </div>
  </div>
</section>'''
    return page(
        title + " | CX University | CX Institute SA", description,
        ROUTE + slug + "/", body, og_image=IMAGES + "/" + image + ".webp",
    )


def build_patient_detail(image, title, description, enrol_url):
    slug = DETAILS[image][0]
    body = f'''<section class="opener navy kn-hero" aria-labelledby="course-title">
  <div class="opener-media">{photo(image, eager=True)}</div>
  <div class="opener-text">
    {HOME_BUTTON}
    <a class="back" href="{ROUTE}#courses">← All CX University courses</a>
    <h1 id="course-title">Patient Experience Mastery (PX)</h1>
    <p class="kn-sub">Online Certification course</p>
    <p><strong>Price U$D417.00</strong><br>
      Self-paced online course / 6 months access<br>
      Enrol and pay online</p>
    <p>Become a master of Patient Experience and make an impact in your healthcare organization. This course leads to professional Patient Experience Specialist (PXS)™ certification. Learn at your own pace with comprehensive online courses aligned to the globally recognized domains of PX knowledge and skills.</p>
  </div>
</section>
<section class="section" aria-labelledby="course-certification">
  <div class="wrap narrow">
    <h2 id="course-certification">Patient Experience Specialist (PXS)™ Certification</h2>
    <p>Earn your Patient Experience Specialist (PXS)™ certificate by completing the online courses and passing the certification exam, which will be accessible in your LMS portal after you complete your courses. As a Patient Experience Specialist (PXS)™, you will harness the power of Patient Experience to move the needle in your work and organization. This program develops leaders and advocates for PX across all levels of a company.</p>
    <h2>Course Details</h2>
    <p>Each of the five Online Courses covers theoretical and best practice aspects of Patient Experience. Complete the Online Courses at your leisure from any online or mobile device. See below for the list of courses included in this package.</p>
    <ul>
      <li>PX 521 Patient Experience Strategy</li>
      <li>PX 522 Patient-Centric Culture and Accountability</li>
      <li>PX 523 Patient Experience Metrics and Analysis</li>
      <li>PX 524 Improvement and Design</li>
      <li>PX 525 Voice of the Customer/Patient (VOC/VOP) and Intelligence</li>
    </ul>
    <h2>Course Access</h2>
    <p>This course is available through CX University’s subsidiary, PX Academy.</p>
    <h2>Pre-Requisites</h2>
    <p>No prerequisites necessary as these courses cover all PX Core Competencies</p>
  </div>
</section>
<section class="section dark" id="enquire" aria-labelledby="course-enrol">
  <div class="wrap narrow">
    <h2 id="course-enrol">Enrol with CX University</h2>
    <div class="btn-row">
      <a class="btn btn-teal" href="{e(enrol_url)}">Enrol in Patient Experience Course</a>
      <a class="btn btn-ghost" href="mailto:lynn@cx-company.com?subject=CX%20University%20course%20enquiry">Ask Lynn a question</a>
    </div>
  </div>
</section>'''
    return page(
        title + " | CX University | CX Institute SA", description,
        ROUTE + slug + "/", body, og_image=IMAGES + "/" + image + ".webp",
    )


def build_ai_detail(image, title, description, enrol_url):
    slug = DETAILS[image][0]
    body = f'''<section class="opener navy kn-hero" aria-labelledby="course-title">
  <div class="opener-media">{photo(image, eager=True)}</div>
  <div class="opener-text">
    {HOME_BUTTON}
    <a class="back" href="{ROUTE}#courses">← All CX University courses</a>
    <h1 id="course-title">AI - CX Leadership - Online course</h1>
    <p><strong>Price U$D995.00</strong><br>
      Instructor-led online course<br>
      Enrol and pay online</p>
  </div>
</section>
<section class="section" aria-labelledby="course-overview">
  <div class="wrap narrow">
    <h2 id="course-overview">Why Take the X in the Age of AI South Africa?</h2>
    <p>In today’s AI-driven economy, the integration of Artificial Intelligence into Customer Experience (CX) is no longer a futuristic vision—it’s a present-day imperative. As customer expectations evolve rapidly, intelligent systems are redefining how brands engage, personalize, and optimize interactions across the customer journey. As AI shifts from theoretical promise to practical implementation, organizations are embracing it as a core engine of customer engagement.</p>
    <p>This course explores how AI functions—such as learning, perception, and natural language processing—combine to power emotionally intelligent, real-time, and predictive experiences. As the AI landscape matures, Customer Experience (CX) enters a new phase: intelligent journey orchestration. Moving beyond isolated touchpoints, the course also explores how organizations can harness AI to orchestrate real-time, end-to-end customer journeys that are adaptive, predictive, and deeply personalized. Finally, it explores how companies move from isolated pilots to organization-wide systems that deliver consistent, ethical, and high-impact customer experiences.</p>
    <p>The focus is on embedding AI into real business workflows, aligning technology with strategy, and establishing a foundation of trust, governance, and cross-functional collaboration.</p>
    <p>The course describes how customer experience teams can use AI to drive real-time personalization, improve decision-making, and automate at scale—without losing the human element. The course also examines how to bridge the gap between strategy and execution using models for AI adoption, leadership readiness, and responsible deployment.</p>
    <ul>
      <li>Master the art of leading in an AI-powered world</li>
      <li>Fast-track your career with cutting-edge AI-CX expertise</li>
      <li>Harness the five AI functions that transform customer engagement</li>
      <li>Drive results by reducing costs and boosting conversions with AI</li>
      <li>Deliver real-time personalization and sentiment-driven adaptation</li>
      <li>Pinpoint your organization’s position on the CX-AI maturity curve</li>
      <li>Demystify generative AI and discover how it redefines customer experiences</li>
    </ul>
    <p>Confirm the course access period with CX University before enrolling.</p>
    <p><a class="text-link" href="https://el281.infusionsoft.app/app/form/x-in-the-age-of-ai-course-guide">Download the Course Guide</a></p>
    <h2>What You’ll Learn</h2>
    <p>By the end of this program, you will be able to:</p>
    <ul>
      <li>Develop advanced CX leadership mastery in an AI-driven business environment</li>
      <li>Build career momentum through applied AI-CX knowledge</li>
      <li>Identify and apply the five foundational AI functions in customer engagement</li>
      <li>Optimize business performance by reducing costs and improving conversions with AI</li>
      <li>Implement AI principles for real-time personalization, automation, and sentiment-based adaptation</li>
    </ul>
    <p><a class="text-link" href="https://cxuniversity.com/product/ai-and-cx-leadership-course-south-africa/#eae-pupup-item-1798988385">View Full Calendar</a></p>
    <h2>Who Should Enroll?</h2>
    <p>This course is ideal for:</p>
    <ul>
      <li>CX professionals looking to gain a formal credential and advance in their careers.</li>
      <li>Marketing &amp; Customer Success leaders who want to influence revenues, profits, cost reduction, and easy customer acquisition and retention.</li>
      <li>Business owners &amp; entrepreneurs aiming to differentiate their brand through outstanding CX.</li>
      <li>Consultants &amp; strategists seeking a deeper understanding of customer behavior.</li>
      <li>Anyone looking to build practical mapping skills, drive alignment across teams, and influence experience-focused decision-making.</li>
    </ul>
  </div>
</section>
<section class="section dark" id="enquire" aria-labelledby="course-enrol">
  <div class="wrap narrow">
    <h2 id="course-enrol">Enrol with CX University</h2>
    <div class="btn-row">
      <a class="btn btn-teal" href="{e(enrol_url)}">Enrol in X in the Age of AI</a>
      <a class="btn btn-ghost" href="mailto:lynn@cx-company.com?subject=CX%20University%20course%20enquiry">Ask Lynn a question</a>
    </div>
  </div>
</section>'''
    return page(
        title + " | CX University | CX Institute SA", description,
        ROUTE + slug + "/", body, og_image=IMAGES + "/" + image + ".webp",
    )


def build_detail(image, title, facts, description, enrol_url):
    if image == "cxs":
        return build_cxs_detail(image, description, enrol_url)
    if image == "roadmap":
        return build_roadmap_detail(image, title, description, enrol_url)
    if image == "mapping":
        return build_mapping_detail(image, title, description, enrol_url)
    if image == "patient":
        return build_patient_detail(image, title, description, enrol_url)
    if image == "ai":
        return build_ai_detail(image, title, description, enrol_url)
    slug, audience, topics, format_description = DETAILS[image]
    topics_html = "\n".join(f"      <li>{e(topic)}</li>" for topic in topics)
    body = f'''<section class="opener navy kn-hero" aria-labelledby="course-title">
  <div class="opener-media">{photo(image, eager=True)}</div>
  <div class="opener-text">
    {HOME_BUTTON}
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

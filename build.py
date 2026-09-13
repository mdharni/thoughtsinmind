#!/usr/bin/env python3
"""Builds the Thoughts in Mind site. Run: python3 build.py
Writes full HTML pages into this folder and an artifact-friendly copy of index.html into ../artifact/."""
import os, re
HERE = os.path.dirname(os.path.abspath(__file__))

FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,300..700;1,9..144,300..700&family=Atkinson+Hyperlegible:ital,wght@0,400;0,700;1,400&display=swap">'

LOGO = '''<svg viewBox="0 0 40 40" aria-hidden="true"><circle cx="16" cy="18" r="11" fill="none" stroke="currentColor" stroke-width="2.2"/><circle cx="25" cy="21" r="11" fill="none" stroke="var(--marigold)" stroke-width="2.2"/><circle cx="20.5" cy="19.5" r="2.4" fill="var(--sage)"/></svg>'''

CHECK = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="10"/><path d="m8 12 3 3 5-6"/></svg>'
ARROW = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'

ICONS = {
 'palette': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3a9 9 0 1 0 0 18c1.5 0 2-1 2-2v-1.5a1.5 1.5 0 0 1 1.5-1.5H17a4 4 0 0 0 4-4c0-5-4-9-9-9Z"/><circle cx="8" cy="10" r="1.2" fill="currentColor"/><circle cx="12" cy="7.5" r="1.2" fill="currentColor"/><circle cx="16" cy="10" r="1.2" fill="currentColor"/></svg>',
 'words': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 5h16v11H9l-5 4V5Z"/><path d="M8 9h8M8 12h5"/></svg>',
 'coins': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg>',
 'map': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c3 3.5 3 14.5 0 18M12 3c-3 3.5-3 14.5 0 18"/></svg>',
 'memory': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 19V6a2 2 0 0 1 2-2h5v15H6a2 2 0 0 0-2 2Z"/><path d="M20 19V6a2 2 0 0 0-2-2h-5v15h5a2 2 0 0 1 2 2Z"/></svg>',
 'music': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M9 18V6l10-2v12"/><circle cx="6.5" cy="18" r="2.5"/><circle cx="16.5" cy="16" r="2.5"/></svg>',
 'plus': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" aria-hidden="true"><path d="M12 5v14M5 12h14"/></svg>',
 'brain': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 4a3 3 0 0 0-3 3v10a3 3 0 0 0 3 3 3 3 0 0 0 3-3V7a3 3 0 0 0-3-3Z"/><path d="M9 8H7a2.5 2.5 0 0 0 0 5h2M9 14H7.5a2 2 0 0 0 0 4H9M15 8h2a2.5 2.5 0 0 1 0 5h-2M15 14h1.5a2 2 0 0 1 0 4H15"/></svg>',
 'people': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="9" cy="8" r="3"/><circle cx="17" cy="9" r="2.5"/><path d="M3 19a6 6 0 0 1 12 0M14 19a4.5 4.5 0 0 1 7 0"/></svg>',
 'calendar': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 10h18M8 3v4M16 3v4"/></svg>',
}

TOPICS = [
 ('palette','Colors &amp; Hands','Creative Making &amp; Collaboration','Hands-on projects done side by side: painting, collage, simple crafts. Choosing colors, following steps, and building something together exercises attention and fine-motor planning while the conversation flows naturally.',['Attention','Executive function','Social interaction']),
 ('words','Words, Wit &amp; Wonder','Language Games &amp; Word Creation','Word ladders, category games, finishing familiar sayings, and inventing new words together. Playful language work keeps vocabulary retrieval quick and gives everyone an easy way in.',['Language','Semantic memory','Attention']),
 ('coins','Money, Time &amp; Decision-Making','Planning &amp; Choices','Pricing a shopping list, planning a day, weighing two options. Everyday judgment tasks stimulate executive functioning in a low-pressure, familiar frame.',['Executive function','Working memory','Semantic memory']),
 ('map','Places &amp; Journeys','Local Maps &amp; World Travel','Tracing hometowns and honeymoon trips on a map, comparing landmarks, sharing where the best bakery was. Geography becomes a doorway to stories and orientation.',['Autobiographical memory','Semantic memory','Language']),
 ('memory','From Memory Lane','Childhood Games &amp; Storytelling','Jacks, jump-rope rhymes, first jobs, school days. Structured reminiscence invites each resident to be the expert on their own life and to be heard by the group.',['Autobiographical memory','Language','Social interaction']),
 ('music','Music in Motion','Songs, Choreography &amp; Memory','Singing familiar songs, tapping rhythms, and gentle seated movement. Music reaches memory when words alone cannot, and it lifts the mood of the whole room.',['Procedural memory','Attention','Mood &amp; engagement']),
]

def nav(active):
    items = [('index.html','Home'),('about.html','About'),('workshops.html','Workshops'),('team.html','Our Team'),('facilities.html','For Facilities'),('contact.html','Contact')]
    lis = ''.join('<li><a href="%s"%s>%s</a></li>' % (h, ' aria-current="page"' if h==active else '', t) for h,t in items)
    return f'''<a class="skip" href="#main">Skip to content</a>
<header class="nav"><div class="wrap">
  <a class="brand" href="index.html">{LOGO}<span>Thoughts in Mind</span></a>
  <button class="menu-btn" aria-expanded="false" aria-controls="nav-links" aria-label="Open menu"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M4 7h16M4 12h16M4 17h16"/></svg></button>
  <nav aria-label="Primary"><ul class="nav-links" id="nav-links">{lis}<li class="nav-cta"><a class="btn btn-primary" href="contact.html">Book a session</a></li></ul></nav>
</div></header>'''

FOOTER = f'''<footer><div class="wrap">
  <div><a class="brand" href="index.html">{LOGO}<span>Thoughts in Mind</span></a>
    <p style="margin-top:14px;max-width:38ch">Evidence-based cognitive stimulation workshops for seniors in assisted living and nursing homes. Serving the Tri-Valley and East Bay.</p></div>
  <div><h4>Explore</h4><ul><li><a href="about.html">Mission &amp; research</a></li><li><a href="workshops.html">The workshops</a></li><li><a href="team.html">Facilitators &amp; training</a></li><li><a href="facilities.html">For facilities</a></li><li><a href="Thoughts-in-Mind-Brochure.pdf" download>Brochure (PDF)</a></li></ul></div>
  <div><h4>Contact</h4><ul><li><a href="mailto:thoughtsinmind2@gmail.com">thoughtsinmind2@gmail.com</a></li><li><a href="tel:+19256602773">(925) 660-2773</a></li><li><a href="contact.html">Send an inquiry</a></li></ul></div>
  <div class="foot-note"><span>&copy; <span id="year">2026</span> Thoughts in Mind. All rights reserved.</span><span>Our workshops are enrichment programs, not medical therapy or treatment.</span></div>
</div></footer>
<script src="site.js"></script>'''

def cta(title='Bring Thoughts in Mind to your community.', text='Email or call us and we will send a full breakdown of each workshop, how sessions run, and how we can build a schedule around your residents.'):
    return f'''<section class="cta"><div class="wrap">
  <div class="stack"><h2>{title}</h2><p class="lede" style="color:inherit;opacity:.9">{text}</p>
    <div class="hero-actions"><a class="btn btn-gold" href="contact.html">Send an inquiry {ARROW}</a><a class="btn btn-ghost" style="color:inherit;border-color:rgba(255,255,255,.35)" href="Thoughts-in-Mind-Brochure.pdf" download>Download brochure (PDF)</a></div></div>
  <div class="contact-lines"><a href="mailto:thoughtsinmind2@gmail.com">thoughtsinmind2@gmail.com</a><a href="tel:+19256602773">(925) 660-2773</a><span class="muted" style="color:inherit;opacity:.75;font-size:1rem">Facilitators: Yashita Vijay, Sehej Dharni, Noor Dharni</span></div>
</div></section>'''

def page(fname, title, desc, body, active):
    head = f'<title>{title}</title><meta name="description" content="{desc}">{FONTS}<link rel="stylesheet" href="styles.css">'
    full = f'<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1">\n{head}\n</head>\n<body>\n{nav(active)}\n<main id="main">\n{body}\n</main>\n{FOOTER}\n</body>\n</html>\n'
    with open(os.path.join(HERE, fname), 'w') as f: f.write(full)
    if fname == 'index.html':
        os.makedirs(os.path.join(HERE, '..', 'artifact'), exist_ok=True)
        frag = f'{head}\n{nav(active)}\n<main id="main">\n{body}\n</main>\n{FOOTER}\n'
        with open(os.path.join(HERE, '..', 'artifact', 'index.html'), 'w') as f: f.write(frag)

def topic_cards():
    out = ''
    for icon, name, sub, _, _ in TOPICS:
        out += f'<a class="topic" href="workshops.html#{icon}"><div class="icon">{ICONS[icon]}</div><h3>{name}</h3><p class="sub">{sub}</p></a>'
    out += f'<div class="topic topic-more"><div class="icon">{ICONS["plus"]}</div><h3>And more in development</h3><p class="sub">We continue to design and refine new sessions every week. Ask us what is coming next.</p></div>'
    return out

# ---------------- HOME ----------------
home = f'''
<section class="hero"><div class="wrap">
  <div class="hero-copy">
    <p class="eyebrow">Evidence-based cognitive stimulation for senior communities</p>
    <h1>Keeping minds active, together.</h1>
    <p class="lede measure">Thoughts in Mind brings structured, research-backed group workshops, informed by Cognitive Stimulation Therapy (CST), to residents of assisted living and nursing homes. Conversation, creativity, and memory work, delivered on a schedule your residents can count on.</p>
    <div class="hero-actions"><a class="btn btn-primary" href="contact.html">Bring us to your facility {ARROW}</a><a class="btn btn-ghost" href="workshops.html">Explore the workshops</a></div>
    <div class="trust"><ul>
      <li>{CHECK}<span>Grounded in peer-reviewed research</span></li>
      <li>{CHECK}<span>Facilitators certified in dementia care</span></li>
      <li>{CHECK}<span>Consistent, structured sessions</span></li>
    </ul></div>
  </div>
  <figure class="hero-photo"><img src="images/session-group.jpg" alt="Residents coloring and making greeting cards around a table while two facilitators look on" width="1200" height="1600" fetchpriority="high"><figcaption>A Colors &amp; Hands session in an assisted living community</figcaption></figure>
</div></section>

<section class="band"><div class="wrap">
  <p class="statement">"These workshops are not therapy or treatment. They are evidence-based cognitive stimulation designed for prevention and enrichment."</p>
  <p class="aside">We work to keep brains active, support mental health, and build community. Every session stimulates several cognitive domains at once, while making room for reminiscence, meaningful conversation, and laughter.</p>
</div></section>

<section><div class="wrap">
  <div class="sec-head"><div><p class="eyebrow">Our mission</p><h2>Three things we work toward in every session</h2></div><p class="lede">Our mission is to protect cognitive health, reduce isolation, and strengthen the mental sharpness and memory of older adults through engaging activities.</p></div>
  <div class="pillars">
    <div class="pillar"><h3>Protect cognitive health</h3><p>Structured activities that exercise memory, attention, language, and executive function, the domains most affected by aging and dementia.</p></div>
    <div class="pillar"><h3>Reduce isolation</h3><p>Small groups, familiar faces, and a regular rhythm. Residents come to know each other and to look forward to the next session.</p></div>
    <div class="pillar"><h3>Strengthen sharpness and memory</h3><p>Reminiscence and person-centered games that let each resident be the expert on their own life, and be heard.</p></div>
  </div>
</div></section>

<section style="padding-top:0"><div class="wrap">
  <div class="sec-head"><div><p class="eyebrow">The workshops</p><h2>Six themes, each built to stimulate several cognitive domains at once</h2></div><p class="lede">Every workshop pairs a cognitive exercise with an enjoyable, social activity. Residents rotate through the themes so no two weeks feel the same.</p></div>
  <div class="topics">{topic_cards()}</div>
</div></section>

<section style="padding-top:0"><div class="wrap">
  <div class="sec-head"><div><p class="eyebrow">From our sessions</p><h2>What a workshop looks like in the room</h2></div><p class="lede">Real sessions in Tri-Valley assisted living communities. Small groups, hands busy, and conversation flowing.</p></div>
  <div class="gallery">
    <figure class="tall"><img src="images/coloring-closeup.jpg" alt="Close-up of residents coloring detailed patterns with markers and pipe cleaners" loading="lazy"><figcaption>Colors &amp; Hands: pattern coloring and pipe-cleaner flowers</figcaption></figure>
    <figure class="wide"><img src="images/song-lyrics.jpg" alt="Residents seated in a circle writing on clipboards while a facilitator helps one of them" loading="lazy"><figcaption>Music in Motion: finishing the lyrics to familiar songs</figcaption></figure>
    <figure><img src="images/tabletop-bowling.jpg" alt="A resident rolling a ball toward tabletop bowling pins as a facilitator watches" loading="lazy"><figcaption>From Memory Lane: tabletop bowling</figcaption></figure>
    <figure><img src="images/creative-table.jpg" alt="A facilitator leaning in to help residents with scratch-art cards at a long table" loading="lazy"><figcaption>Facilitators work one to one whenever it helps</figcaption></figure>
  </div>
</div></section>

<section class="evidence"><div class="wrap">
  <div class="stack">
    <p class="eyebrow">Research foundation</p>
    <h2>Why cognitive stimulation</h2>
    <p class="lede">Medication can offer modest gains for some people with dementia, but it does not stop or reverse the disease. Clinical guidelines now recommend pairing it with evidence-based, non-pharmacological programs like structured group cognitive stimulation.</p>
    <div class="stat"><span class="big">37</span><span class="cap">randomized controlled trials reviewed by the 2023 Cochrane review of cognitive stimulation for dementia (Woods et al.)</span></div>
    <a class="btn btn-ghost" href="about.html#research">Read the research summary {ARROW}</a>
  </div>
  <ul class="points">
    <li><span class="dot">{ICONS['brain']}</span><div><h3>Improves cognition and communication</h3><p>Multiple randomized controlled trials and systematic reviews show structured group cognitive stimulation can improve cognitive functioning, communication, and quality of life.</p></div></li>
    <li><span class="dot">{ICONS['people']}</span><div><h3>Works best as a group</h3><p>Combining cognitive exercises with enjoyable, person-centered group activities improves engagement and helps maintain psychosocial functioning.</p></div></li>
    <li><span class="dot">{ICONS['calendar']}</span><div><h3>Consistency matters</h3><p>Research indicates regular, scheduled sessions produce stronger cognitive outcomes than occasional ones. Our program is designed around that finding.</p></div></li>
  </ul>
</div></section>

<section><div class="wrap">
  <div class="sec-head"><div><p class="eyebrow">Cognitive domains</p><h2>What a session exercises</h2></div><p class="lede">Each session is designed to reach several of these at once, so residents with different strengths all find a way to participate.</p></div>
  <ul class="domains"><li>Autobiographical memory</li><li>Semantic memory</li><li>Executive functioning</li><li>Attention</li><li>Language</li><li>Reminiscence</li><li>Meaningful conversation</li><li>Social interaction</li></ul>
</div></section>

<section style="padding-top:0"><div class="wrap">
  <div class="sec-head"><div><p class="eyebrow">How it works</p><h2>From first email to first session</h2></div><p class="lede">We keep it simple for activity directors and administrators. Three steps, and your residents have a program they can engage with regularly.</p></div>
  <div class="steps">
    <div class="step"><h3>Reach out</h3><p>Email or call us. We will send a full breakdown of each workshop, what a session looks like, and answer questions about your residents' needs.</p></div>
    <div class="step"><h3>Build a schedule</h3><p>Together we set a consistent cadence, group size, and room. We plan alongside care staff for residents with limited verbal communication or language barriers.</p></div>
    <div class="step"><h3>Sessions begin</h3><p>Our trained facilitators run each workshop in a consistent, structured format, and we keep you informed on how residents are engaging.</p></div>
  </div>
</div></section>

<section style="padding-top:0"><div class="wrap">
  <div class="sec-head"><div><p class="eyebrow">Our facilitators</p><h2>Trained, certified, and here for the long run</h2></div><p class="lede">Every facilitator completes caregiving and dementia care training before working with residents, so they understand not just the activities but the reasoning behind them.</p></div>
  <div class="team">
    <div class="person"><div class="avatar">N</div><h3>Noor Dharni</h3><p class="role">Certified Nursing Assistant. Senior at UC Berkeley, B.A. in Neuroscience and Public Health.</p></div>
    <div class="person"><div class="avatar gold">S</div><h3>Sehej Dharni</h3><p class="role">Facilitator. Certified in Introduction to Caregiving and Dementia Care and Management.</p></div>
    <div class="person"><div class="avatar sage">Y</div><h3>Yashita Vijay</h3><p class="role">Facilitator. Certified in Introduction to Caregiving and Dementia Care and Management.</p></div>
  </div>
  <p style="margin-top:28px"><a href="team.html">Meet the team and read about our training {ARROW.replace('<svg','<svg style="width:16px;height:16px;display:inline;vertical-align:-3px"')}</a></p>
</div></section>

{cta()}
'''
page('index.html','Thoughts in Mind','Evidence-based cognitive stimulation workshops for seniors in assisted living and nursing homes.', home, 'index.html')

# ---------------- ABOUT ----------------
about = f'''
<section class="page-head"><div class="wrap"><p class="eyebrow">About Thoughts in Mind</p><h1>Research-backed enrichment for older adults</h1><p class="lede">We deliver workshops incorporating CST-informed activities to seniors in assisted living and nursing homes. Here is what drives us and the evidence we build on.</p></div></section>

<section><div class="wrap split">
  <div class="sticky stack"><p class="eyebrow">Mission</p><h2>Protect cognitive health. Reduce isolation. Strengthen memory.</h2></div>
  <div class="prose">
    <p>Thoughts in Mind delivers research-backed workshops incorporating CST-informed activities to seniors in assisted living and nursing homes. Our mission is to protect cognitive health, reduce isolation, and strengthen the mental sharpness and memory of older adults through engaging activities.</p>
    <div class="callout"><h3>Not therapy or treatment</h3><p>These workshops are evidence-based cognitive stimulation designed for prevention and enrichment. We work to keep brains active, support mental health, and build community.</p></div>
    <p>Cognitive Stimulation Therapy (CST) is a structured, group-based program of themed activities developed for people living with mild to moderate dementia. Our workshops draw on its principles: consistent structure, multi-sensory activities, an emphasis on opinions over facts, and a warm, person-centered group setting.</p>
  </div>
</div></section>

<section id="research" style="padding-top:0"><div class="wrap split">
  <div class="sticky stack"><p class="eyebrow">Research foundation</p><h2>Why non-pharmacological care matters</h2><p class="muted">A summary of the evidence our curriculum is built on. Full references are listed below.</p></div>
  <div class="prose">
    <h3>The limits of medication</h3>
    <p>Current medications for dementia, such as cholinesterase inhibitors and memantine, may provide modest improvements in memory, attention, and daily functioning for some individuals, but they do not stop or reverse the progression of the disease. As a result, clinical guidelines increasingly recommend combining medication with evidence-based, non-pharmacological interventions that support cognitive function, communication, emotional well-being, and social engagement.</p>
    <h3>What the trials show</h3>
    <p>Evidence-based cognitive stimulation interventions are among the most extensively researched non-pharmacological approaches for individuals with mild to moderate dementia. Multiple randomized controlled trials and systematic reviews have demonstrated that structured group-based cognitive stimulation can improve cognitive functioning, communication, quality of life, and social engagement when delivered through consistent, structured programming.</p>
    <h3>How our curriculum applies it</h3>
    <p>Our workshop curriculum is built upon these evidence-based principles. Each session incorporates activities designed to stimulate multiple cognitive domains, including autobiographical memory, semantic memory, executive functioning, attention, and language, while simultaneously encouraging reminiscence, meaningful conversation, and social interaction. Research suggests that combining cognitive exercises with enjoyable, person-centered group activities contributes to improved engagement and helps maintain cognitive and psychosocial functioning in older adults with dementia.</p>
    <h3>Why we insist on a regular schedule</h3>
    <p>Research indicates that structured group cognitive stimulation delivered on a consistent schedule produces stronger cognitive outcomes than less frequent sessions. For this reason, our workshops are designed to provide regular opportunities for cognitive engagement, meaningful social interaction, and mentally stimulating activities that align with the evidence supporting non-pharmacological dementia care.</p>
  </div>
</div></section>

<section style="padding-top:0"><div class="wrap">
  <div class="sec-head"><div><p class="eyebrow">References</p><h2>Selected research</h2></div><p class="lede">Peer-reviewed sources that inform our program design.</p></div>
  <ol class="refs">
    <li><span>Aguirre, E., et al. (2013). Cognitive stimulation for dementia: A systematic review of the evidence from randomized controlled trials. <em>Ageing Research Reviews.</em></span></li>
    <li><span>Cove, J., et al. (2014). Effectiveness of weekly cognitive stimulation therapy for people with dementia. <em>Clinical Interventions in Aging.</em></span></li>
    <li><span>Holden, E., et al. (2020). Cognitive stimulation therapy for dementia: Provision in National Health Service settings. <em>International Journal of Geriatric Psychiatry.</em></span></li>
    <li><span>Woods, B., et al. (2023). Cognitive stimulation to improve cognitive functioning in people with dementia. <em>Cochrane Database of Systematic Reviews.</em></span></li>
  </ol>
</div></section>

{cta('Want the full curriculum?', 'Email us and we will send a complete breakdown of every workshop, the domains each one targets, and how a session runs from start to finish.')}
'''
page('about.html','About | Thoughts in Mind','Our mission and the research foundation behind Thoughts in Mind cognitive stimulation workshops.', about, 'about.html')

# ---------------- WORKSHOPS ----------------
ws_items = ''
for icon, name, sub, desc, doms in TOPICS:
    ws_items += f'<article class="ws" id="{icon}"><div class="icon">{ICONS[icon]}</div><div class="body"><h3>{name}</h3><p class="sub">{sub}</p><p>{desc}</p><ul class="doms">{"".join(f"<li>{d}</li>" for d in doms)}</ul></div></article>'

workshops = f'''
<section class="page-head"><div class="wrap"><p class="eyebrow">The workshops</p><h1>Six themes, and more on the way</h1><p class="lede">Each workshop pairs a cognitive exercise with an enjoyable group activity. Residents rotate through the themes, so the program stays fresh while the format stays reassuringly familiar.</p></div></section>

<section style="padding-bottom:0"><div class="wrap photo-band">
  <figure><img src="images/coloring-closeup.jpg" alt="Residents coloring detailed patterns with markers" loading="lazy"></figure>
  <figure><img src="images/song-lyrics.jpg" alt="Residents writing song lyrics on clipboards during a music workshop" loading="lazy"></figure>
</div></section>

<section><div class="wrap split">
  <div class="sticky stack"><p class="eyebrow">A typical session</p><h2>Familiar shape, new content every time</h2><p class="muted">Consistency is part of the evidence. Every session follows the same arc so residents always know what to expect.</p></div>
  <ul class="timeline">
    <li><span class="t">Welcome</span><div><h3>Orientation and warm-up</h3><p>Greetings by name, the day and date, a group song or a light question that everyone can answer. This settles the room and gently orients each resident.</p></div></li>
    <li><span class="t">Main activity</span><div><h3>The themed workshop</h3><p>The core cognitive activity for the week, run in a small group with facilitators guiding, prompting, and adapting for each person's ability.</p></div></li>
    <li><span class="t">Reflect</span><div><h3>Conversation and reminiscence</h3><p>Open discussion connected to the theme. Opinions are welcomed over right answers, so no one is put on the spot.</p></div></li>
    <li><span class="t">Close</span><div><h3>Thank-yous and a preview</h3><p>A short recap, a look ahead to next time, and a warm goodbye. Residents leave knowing when we will be back.</p></div></li>
  </ul>
</div></section>

<section style="padding-top:0"><div class="wrap">
  <div class="sec-head"><div><p class="eyebrow">Workshop themes</p><h2>The six core workshops</h2></div><p class="lede">Each theme below lists the cognitive domains it is designed to stimulate. We continue to develop new themes every day.</p></div>
  <div class="ws-list">{ws_items}
    <article class="ws" style="border-style:dashed;background:transparent"><div class="icon">{ICONS['plus']}</div><div class="body"><h3>New themes in development</h3><p>We are always designing and piloting new workshops. Email us for the current full breakdown of every theme, including materials and adaptations.</p></div></article>
  </div>
</div></section>

<section style="padding-top:0"><div class="wrap grid-2">
  <div class="callout sage"><h3>Adapted for every resident</h3><p>Facilitators often work alongside care staff for residents with limited verbal communication or language barriers. Activities are adjusted so participation never depends on speech alone.</p></div>
  <div class="callout plum"><h3>Person-centered by design</h3><p>We favor opinions over facts, choice over instruction, and encouragement without pressure. Facilitators are trained to pace a session and recognize signs of fatigue or distress.</p></div>
</div></section>

{cta('Ask for the full workshop breakdown.', 'We will send details of each workshop, the materials we bring, and how we adapt activities for different levels of ability.')}
'''
page('workshops.html','Workshops | Thoughts in Mind','The six core Thoughts in Mind cognitive stimulation workshops and what a session looks like.', workshops, 'workshops.html')

# ---------------- TEAM ----------------
team = f'''
<section class="page-head"><div class="wrap"><p class="eyebrow">Our team</p><h1>Workshop facilitators</h1><p class="lede">Every facilitator is trained before stepping into a room with residents. Here is who we are and how we prepare.</p></div></section>

<section><div class="wrap">
  <div class="team">
    <div class="person"><div class="avatar">N</div><h3>Noor Dharni</h3><p class="role">Senior at UC Berkeley, pursuing a B.A. in Neuroscience and Public Health.</p>
      <ul class="creds"><li>{CHECK}<span>Certified Nursing Assistant, California Department of Public Health (<a href="https://cvl.cdph.ca.gov/DetailPage.aspx?cert_holder_id=738672" target="_blank" rel="noopener">verify license</a>)</span></li></ul></div>
    <div class="person"><div class="avatar gold">S</div><h3>Sehej Dharni</h3><p class="role">Incoming senior at Dublin High School.</p>
      <ul class="creds"><li>{CHECK}<span>Certified: Introduction to Caregiving</span></li><li>{CHECK}<span>Certified: Introduction to Dementia Care and Management</span></li></ul></div>
    <div class="person"><div class="avatar sage">Y</div><h3>Yashita Vijay</h3><p class="role">Incoming senior at Dublin High School.</p>
      <ul class="creds"><li>{CHECK}<span>Certified: Introduction to Caregiving</span></li><li>{CHECK}<span>Certified: Introduction to Dementia Care and Management</span></li></ul></div>
  </div>
</div></section>

<section style="padding-top:0"><div class="wrap">
  <figure class="split-photo" style="aspect-ratio:16/9"><img src="images/session-group.jpg" alt="Facilitators Yashita and Noor standing with residents at a workshop table" loading="lazy"></figure>
</div></section>

<section style="padding-top:0"><div class="wrap split">
  <div class="sticky stack"><p class="eyebrow">Facilitator training</p><h2>Before we work with residents</h2><p class="muted">Our facilitators are trained using established, publicly available resources designed for caregivers and volunteers working with individuals experiencing memory loss.</p></div>
  <div class="prose">
    <div class="card"><h3>Introduction to Caregiving <span class="muted" style="font-family:inherit;font-size:.9rem;font-weight:400">(Alison)</span></h3><p>The fundamentals of caregiving, effective communication, person-centered care, and supporting older adults.</p></div>
    <div class="card"><h3>Dementia Care and Management <span class="muted" style="font-family:inherit;font-size:.9rem;font-weight:400">(Alison)</span></h3><p>Dementia types, communication strategies, behavioral support, and best practices for compassionate dementia care.</p></div>
    <h3>What that training means in the room</h3>
    <p>This training ensures every facilitator understands not just the activities themselves, but the reasoning behind them:</p>
    <ul class="check">
      <li>{CHECK}<span>How to pace a session so no one is rushed or left waiting</span></li>
      <li>{CHECK}<span>How to redirect gently when a conversation drifts or a resident becomes unsettled</span></li>
      <li>{CHECK}<span>How to encourage participation without pressure</span></li>
      <li>{CHECK}<span>How to recognize signs of fatigue or distress and respond with care</span></li>
    </ul>
  </div>
</div></section>

{cta('Meet us in person.', 'We are happy to visit your community, walk your activity team through a sample session, and answer questions before anything is scheduled.')}
'''
page('team.html','Our Team | Thoughts in Mind','Meet the Thoughts in Mind facilitators and learn how they are trained in caregiving and dementia care.', team, 'team.html')

# ---------------- FACILITIES ----------------
facilities = f'''
<section class="page-head"><div class="wrap"><p class="eyebrow">For facilities</p><h1>A reliable program your residents can count on</h1><p class="lede">Built for activity directors and administrators of assisted living and nursing homes who want structured, evidence-based engagement without adding to staff workload.</p></div></section>

<section><div class="wrap split">
  <div class="sticky stack"><p class="eyebrow">How this works with your facility</p><h2>Structured, consistent, and run by us</h2></div>
  <div class="prose">
    <p>Our facilitators work directly with residents using a consistent, structured format grounded in cognitive stimulation research, often alongside care staff for residents with limited verbal communication or language barriers. This gives facilities a reliable program their residents can engage with regularly.</p>
    <h3>What we bring</h3>
    <ul class="check">
      <li>{CHECK}<span>Trained facilitators certified in caregiving and dementia care</span></li>
      <li>{CHECK}<span>A rotating curriculum of themed workshops, with new themes in development</span></li>
      <li>{CHECK}<span>Materials for each session</span></li>
      <li>{CHECK}<span>A consistent schedule your residents and staff can plan around</span></li>
    </ul>
    <h3>What we ask of you</h3>
    <ul class="check">
      <li>{CHECK}<span>A point of contact on your activities or care team</span></li>
      <li>{CHECK}<span>A quiet room with a table and seating for a small group</span></li>
      <li>{CHECK}<span>Guidance on residents who would benefit and any adaptations they need</span></li>
    </ul>
  </div>
</div></section>

<section style="padding-top:0"><div class="wrap grid-2" style="align-items:center">
  <figure class="split-photo" style="aspect-ratio:4/3"><img src="images/tabletop-bowling.jpg" alt="A resident playing tabletop bowling with a facilitator" loading="lazy"></figure>
  <div class="card"><p class="eyebrow">Printable brochure</p><h3>Share Thoughts in Mind with your team</h3><p>A two-page PDF with our mission, the research behind the program, the six workshops, and how to get started. Forward it to your administrator or print it for your activity board.</p><a class="btn btn-primary dl" href="Thoughts-in-Mind-Brochure.pdf" download>Download the brochure <small>(PDF)</small></a></div>
</div></section>

<section style="padding-top:0"><div class="wrap">
  <div class="sec-head"><div><p class="eyebrow">Common questions</p><h2>Frequently asked</h2></div><p class="lede">If your question is not here, email us and we will answer directly.</p></div>
  <div class="faq">
    <details><summary>Is this therapy or medical treatment?</summary><p class="a">No. Our workshops are evidence-based cognitive stimulation designed for prevention and enrichment. They complement, and never replace, the medical and clinical care your residents already receive.</p></details>
    <details><summary>Which residents can take part?</summary><p class="a">Workshops are designed for older adults, including those living with mild to moderate memory loss. Residents do not need a diagnosis to participate. We adapt activities so participation does not depend on speech alone, and we often work alongside care staff for residents with limited verbal communication or language barriers.</p></details>
    <details><summary>How often do sessions run?</summary><p class="a">Research shows a consistent schedule produces stronger outcomes than occasional sessions, so we build a regular cadence with each facility rather than one-off visits. We will agree on a rhythm that fits your calendar.</p></details>
    <details><summary>How large are the groups?</summary><p class="a">Small enough that every resident is greeted by name and has a turn to speak. We will recommend a group size based on your residents' needs and the room available.</p></details>
    <details><summary>Who leads the sessions?</summary><p class="a">Our own trained facilitators lead every session. Each has completed Introduction to Caregiving and Dementia Care and Management training, and our lead facilitator is a Certified Nursing Assistant.</p></details>
    <details><summary>What does it cost?</summary><p class="a">Email us with a little about your community and we will get back to you with details and a full breakdown of the workshops.</p></details>
  </div>
</div></section>

<section style="padding-top:0"><div class="wrap grid-2">
  <div class="card"><p class="eyebrow">For families</p><h3>Looking for a program for a loved one?</h3><p>If your parent or relative lives in an assisted living or nursing community, we would be glad to speak with their activity director. Send us the community's name and we will reach out.</p><a href="contact.html">Contact us {ARROW.replace('<svg','<svg style="width:16px;height:16px;display:inline;vertical-align:-3px"')}</a></div>
  <div class="card"><p class="eyebrow">Where we work</p><h3>Tri-Valley and the East Bay</h3><p>We are based in Dublin, California, and serve assisted living and nursing communities across the Tri-Valley and surrounding East Bay. Not sure if we reach you? Ask.</p><a href="contact.html">Check your area {ARROW.replace('<svg','<svg style="width:16px;height:16px;display:inline;vertical-align:-3px"')}</a></div>
</div></section>

{cta()}
'''
page('facilities.html','For Facilities | Thoughts in Mind','How Thoughts in Mind cognitive stimulation workshops work with assisted living and nursing home communities.', facilities, 'facilities.html')

# ---------------- CONTACT ----------------
contact = f'''
<section class="page-head"><div class="wrap"><p class="eyebrow">Contact</p><h1>Let's talk about your residents</h1><p class="lede">Email us for a full breakdown of the workshops, or use the form and we will get back to you.</p></div></section>

<section><div class="wrap contact-grid">
  <div class="stack">
    <div class="contact-card">
      <div class="line"><span>Email</span><a href="mailto:thoughtsinmind2@gmail.com">thoughtsinmind2@gmail.com</a></div>
      <div class="line"><span>Phone</span><a href="tel:+19256602773">(925) 660-2773</a></div>
      <div class="line"><span>Facilitators</span><p>Yashita Vijay, Sehej Dharni, Noor Dharni</p></div>
      <div class="line"><span>Based in</span><p>Dublin, California. Serving the Tri-Valley and East Bay.</p></div>
    </div>
    <div class="callout"><h3>What to include</h3><p>Your community's name, your role, roughly how many residents might take part, and any scheduling preferences. We will reply with a full breakdown of each workshop.</p></div>
  </div>
  <form id="inquiry" novalidate>
    <div class="two">
      <div class="field"><label for="name">Your name</label><input id="name" name="name" required autocomplete="name"></div>
      <div class="field"><label for="role">Your role</label><input id="role" name="role" placeholder="Activity director, administrator, family member…"></div>
    </div>
    <div class="field"><label for="facility">Facility or community</label><input id="facility" name="facility" autocomplete="organization"></div>
    <div class="two">
      <div class="field"><label for="email">Email</label><input id="email" name="email" type="email" required autocomplete="email"></div>
      <div class="field"><label for="phone">Phone (optional)</label><input id="phone" name="phone" type="tel" autocomplete="tel"></div>
    </div>
    <div class="field"><label for="residents">Approximate number of residents who might take part</label><select id="residents" name="residents"><option value="">Not sure yet</option><option>Fewer than 6</option><option>6 to 12</option><option>13 to 20</option><option>More than 20</option></select></div>
    <div class="field"><label for="message">How can we help?</label><textarea id="message" name="message" placeholder="Tell us about your residents and what you are hoping for."></textarea></div>
    <div><button class="btn btn-primary" type="submit">Send inquiry {ARROW}</button></div>
    <p class="form-note" id="form-status">Submitting opens your email app with the message ready to send to thoughtsinmind2@gmail.com.</p>
  </form>
</div></section>
'''
page('contact.html','Contact | Thoughts in Mind','Contact Thoughts in Mind to bring cognitive stimulation workshops to your assisted living or nursing home community.', contact, 'contact.html')
print('built')

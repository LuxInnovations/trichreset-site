"""Builds the Learn pages (static HTML) from the content below.

Run:  python tools/build_learn.py   (from the repo root)
Each page: answer-first summary, tables, numbered sources, Article + FAQ +
Breadcrumb schema. Written to be quoted by search engines and AI assistants.
Add a page = add a page(...) call; the hub, footer links and sitemap follow.
"""
import html, json, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = 'https://trichreset.com'
UPDATED = '2026-10-18'
UPDATED_TEXT = '18 October 2026'
PLAY = ('https://play.google.com/store/apps/details?id=trichreset.com'
        '&amp;utm_source=trichreset.com&amp;utm_medium=web&amp;utm_campaign=learn&amp;utm_content={slug}')

# ----------------------------------------------------------------- sources
S = {
 'grant2020': ('Grant JE, Dougherty DD, Chamberlain SR. Prevalence, gender correlates, and co-morbidity of trichotillomania. <em>Psychiatry Research</em>. 2020;288:112948.',
               'https://pmc.ncbi.nlm.nih.gov/articles/PMC7212053/'),
 'tlc':       ('The TLC Foundation for Body-Focused Repetitive Behaviors. Hair pulling (trichotillomania).',
               'https://www.bfrb.org/hair-pulling'),
 'farhat2020':('Farhat LC, Olfson E, Nasir M, et al. Pharmacological and behavioral treatment for trichotillomania: an updated systematic review with meta-analysis. <em>Depression and Anxiety</em>. 2020;37(8):715-727.',
               'https://onlinelibrary.wiley.com/doi/10.1002/da.23028'),
 'mcguire2014':('McGuire JF, Ung D, Selles RR, et al. Treating trichotillomania: a meta-analysis of treatment effects and moderators for behavior therapy and serotonin reuptake inhibitors. <em>Journal of Psychiatric Research</em>. 2014;58:76-83.',
               'https://pmc.ncbi.nlm.nih.gov/articles/PMC4163503/'),
 'woods2006': ('Woods DW, Wetterneck CT, Flessner CA. A controlled evaluation of acceptance and commitment therapy plus habit reversal for trichotillomania. <em>Behaviour Research and Therapy</em>. 2006;44(5):639-656.',
               'https://doi.org/10.1016/j.brat.2005.05.006'),
 'azrin1973': ('Azrin NH, Nunn RG. Habit-reversal: a method of eliminating nervous habits and tics. <em>Behaviour Research and Therapy</em>. 1973;11(4):619-628.',
               'https://doi.org/10.1016/0005-7967(73)90119-8'),
 'mansueto1997':('Mansueto CS, Stemberger RMT, Thomas AM, Golomb RG. Trichotillomania: a comprehensive behavioral model. <em>Clinical Psychology Review</em>. 1997;17(5):567-577.',
               'https://doi.org/10.1016/S0272-7358(97)00028-7'),
 'flessner2008':('Flessner CA, Woods DW, Franklin ME, Cashin SE, Keuthen NJ. The Milwaukee Inventory for Subtypes of Trichotillomania-Adult Version (MIST-A): development of an instrument for the assessment of "focused" and "automatic" hair pulling. <em>Journal of Psychopathology and Behavioral Assessment</em>. 2008;30(1):20-30.',
               'https://doi.org/10.1007/s10862-007-9073-x'),
 'apa2013':   ('American Psychiatric Association. <em>Diagnostic and Statistical Manual of Mental Disorders</em>, 5th edition (DSM-5). 2013. Trichotillomania (hair-pulling disorder).',
               'https://www.psychiatry.org/psychiatrists/practice/dsm'),
 'icd11':     ('World Health Organization. ICD-11 for Mortality and Morbidity Statistics. 6B25.0 Trichotillomania.',
               'https://icd.who.int/browse/2024-01/mms/en'),
 'chesivoir2022': ('Chesivoir EK, Valle S, Grant JE. Comorbid trichotillomania and attention-deficit hyperactivity disorder in adults. <em>Comprehensive Psychiatry</em>. 2022;116:152317.',
               'https://doi.org/10.1016/j.comppsych.2022.152317'),
 'farhat2025': ('Farhat LC, Isomura K, Fernández de la Cruz L, et al. Sociodemographic and clinical characteristics of 1,234 individuals diagnosed with trichotillomania in the Swedish National Patient Register. <em>Scientific Reports</em>. 2025;15:10396.',
               'https://www.nature.com/articles/s41598-025-95416-w'),
 'simon2009': ('Simon V, Czobor P, Bálint S, Mészáros A, Bitter I. Prevalence and correlates of adult attention-deficit hyperactivity disorder: meta-analysis. <em>British Journal of Psychiatry</em>. 2009;194(3):204-211.',
               'https://doi.org/10.1192/bjp.bp.107.048827'),
 'skinaware': ('SkinAware. Best apps to stop hair pulling (2026 comparison). Updated 20 August 2026. Used for third-party app prices.',
               'https://www.skinawareapp.com/blog/hair-pulling-app'),
 'sa-medicare': ('Services Australia. Mental health care and Medicare.',
               'https://www.servicesaustralia.gov.au/mental-health-care-and-medicare'),
 'betteraccess': ('Australian Government Department of Health, Disability and Ageing. Better Access initiative.',
               'https://www.health.gov.au/our-work/better-access-initiative'),
 'franklin2011': ('Franklin ME, Edson AL, Ledley DA, Cahill SP. Behavior therapy for pediatric trichotillomania: a randomized controlled trial. <em>Journal of the American Academy of Child and Adolescent Psychiatry</em>. 2011;50(8):763-771.',
               'https://pmc.ncbi.nlm.nih.gov/articles/PMC3143367/'),
 'tlc2011':   ('Scientific Advisory Board of the Trichotillomania Learning Center (now the TLC Foundation for BFRBs). <em>Expert Consensus Treatment Guidelines for Trichotillomania, Skin Picking and Other Body-Focused Repetitive Behaviors</em>. 2011.',
               'https://arfamiliesfirst.com/wp-content/uploads/2016/05/Trichotillomania-ExpertGuidelines_000.pdf'),
}

ORDER = []  # the current page's source order, set in render()

FREE = '<em>Boredom and the Body</em> is a full ten-minute Trich Reset meditation, free on our homepage. No signup, no email.'

def cta(slug, label, h, body):
    return f'''<div class="cta-card dark-zone">
 <p class="label">{label}</p>
 <h2>{h}</h2>
 <p>{body}</p>
 <p class="cta-row"><a class="btn btn-accent" href="/#listen">Play it free</a> <a class="btn btn-ghost" href="{PLAY.format(slug=slug)}">Get it on Google Play</a></p>
</div>
'''

def cite(*keys):
    return ''.join(f'<sup><a href="#src-{k}">[{ORDER.index(k)+1}]</a></sup>' for k in keys)

# ------------------------------------------------------------------ pages
PAGES = []

def page(slug, title, h1, label, desc, summary, body, faqs, sources):
    PAGES.append(dict(slug=slug, title=title, h1=h1, label=label, desc=desc,
                      summary=summary, body=body, faqs=faqs, sources=sources))

# 1 ------------------------------------------------------------- what is it
page('what-is-trichotillomania',
 'What Is Trichotillomania? Hair Pulling Disorder Explained',
 'What is trichotillomania?',
 'Learn · The basics',
 'Trichotillomania is a recurring urge to pull out your own hair. Around 1.7% of adults have it. Symptoms, causes, focused vs automatic pulling and diagnosis, with research sources.',
 lambda: f'''Trichotillomania (trick-o-till-o-MAY-nee-uh), also called hair pulling disorder or "trich", is
 the repeated pulling out of your own hair, with repeated attempts to stop, that causes distress or gets in
 the way of daily life.{cite('apa2013')} It is a body-focused repetitive behaviour (BFRB), not a habit you
 lack the willpower to drop. A 2020 survey of more than 10,000 US adults found a point prevalence of
 <strong>1.7%</strong>, with similar rates in men and women.{cite('grant2020')}''',
 lambda: f'''
<h2>Key facts</h2>
<div class="table-wrap">
<table>
 <caption>Trichotillomania at a glance</caption>
 <tbody>
  <tr><th scope="row">Other names</th><td>Hair pulling disorder, trich, TTM</td></tr>
  <tr><th scope="row">Classification</th><td>Obsessive-compulsive and related disorders (DSM-5){cite('apa2013')}; body-focused repetitive behaviour disorders (ICD-11, 6B25.0){cite('icd11')}</td></tr>
  <tr><th scope="row">How common</th><td>1.7% point prevalence in US adults aged 18 to 69{cite('grant2020')}; community estimates range from 0.5% to 2%{cite('grant2020')}. About 1 to 2 in 50 people in their lifetime{cite('tlc')}</td></tr>
  <tr><th scope="row">Who</th><td>Equal in boys and girls in childhood; 80 to 90% of reported adult cases are women{cite('tlc')}. A 2020 community survey found 1.8% of men and 1.7% of women{cite('grant2020')}, which suggests men are under-represented in clinics</td></tr>
  <tr><th scope="row">Typical onset</th><td>Late childhood or early puberty{cite('tlc')}</td></tr>
  <tr><th scope="row">Common sites</th><td>Scalp, eyebrows, eyelashes, and any body hair{cite('tlc')}</td></tr>
  <tr><th scope="row">Best-evidenced treatment</th><td>Behaviour therapy with habit reversal training{cite('farhat2020','mcguire2014')}. See <a href="/trichotillomania-treatment">treatments compared</a></td></tr>
 </tbody>
</table>
</div>

<h2>How it is diagnosed</h2>
<p>A clinician uses the DSM-5 criteria.{cite('apa2013')} In plain terms, all five need to be true:</p>
<ol>
 <li>You pull out your hair again and again, and it leads to hair loss.</li>
 <li>You have tried, more than once, to cut down or stop.</li>
 <li>It causes real distress, or gets in the way of work, school, relationships or other parts of life.</li>
 <li>It isn't caused by another medical condition, such as a skin condition.</li>
 <li>Another mental health condition doesn't explain it better (for example, trying to fix a perceived flaw in appearance, as in body dysmorphic disorder).</li>
</ol>
<p>Only a doctor or psychologist can diagnose it. If this list sounds like you, that is a good reason to talk to one.</p>

<h2>Focused vs automatic pulling</h2>
<p>Researchers describe two styles of pulling, and most people have some of both.{cite('flessner2008')}</p>
<div class="table-wrap">
<table>
 <caption>The two pulling styles</caption>
 <thead><tr><th scope="col"></th><th scope="col">Focused pulling</th><th scope="col">Automatic pulling</th></tr></thead>
 <tbody>
  <tr><th scope="row">Awareness</th><td>You know you are doing it</td><td>You often notice only afterwards</td></tr>
  <tr><th scope="row">What drives it</th><td>An urge, tension, a feeling to relieve, or a "wrong" hair to remove</td><td>Sedentary moments: reading, scrolling, driving, watching TV, lying in bed</td></tr>
  <tr><th scope="row">What tends to help</th><td>Tools for the urge and the feeling: urge surfing, acceptance, competing responses</td><td>Awareness first: noticing the setup, then changing the environment</td></tr>
 </tbody>
</table>
</div>

<h2>Why it happens</h2>
<p>There isn't a single cause. The comprehensive behavioural (ComB) model describes pulling as something
 that is triggered and reinforced across five areas, often remembered as <strong>SCAMP</strong>:{cite('mansueto1997')}</p>
<div class="table-wrap">
<table>
 <caption>The five SCAMP areas, with examples</caption>
 <thead><tr><th scope="col">Area</th><th scope="col">What it means</th><th scope="col">Example trigger</th></tr></thead>
 <tbody>
  <tr><th scope="row">Sensory</th><td>The physical feel of hair, roots, texture</td><td>A coarse or kinked hair that feels "wrong"</td></tr>
  <tr><th scope="row">Cognitive</th><td>Thoughts and beliefs</td><td>"I'll just get this one and stop"</td></tr>
  <tr><th scope="row">Affective</th><td>Emotions</td><td>Stress, boredom, anxiety, sadness</td></tr>
  <tr><th scope="row">Motor</th><td>Hand position and habits</td><td>Resting your hand on your head while you read</td></tr>
  <tr><th scope="row">Place</th><td>Where and when</td><td>The bathroom mirror, bed, the car</td></tr>
 </tbody>
</table>
</div>
<p>Most people pull for reasons in more than one area. Knowing your own mix is the first step to choosing tools that fit. The
 <a href="/how-to-stop-pulling-hair">practical guide</a> walks through tools for each, and the <a href="/">Trich Reset app</a> has a
 lesson on every SCAMP area plus a short questionnaire that builds your own profile.</p>

<h2>Is trichotillomania dangerous?</h2>
<p>It is usually not physically dangerous, but it can cause patchy hair loss, skin irritation and a lot of shame. One rare but serious risk:
 people who swallow pulled hair can develop a hairball in the stomach or intestines (a trichobezoar), which may need surgery.{cite('tlc')}
 If you swallow hair and have stomach pain, nausea or vomiting, see a doctor.</p>

{cta('what-is-trichotillomania', 'Understanding is step one', 'Then you need something for the urge.',
     'Trich Reset has 21 guided meditations, hypnosis and sleep tracks made only for hair pulling. ' + FREE)}''',
 [('How common is trichotillomania?', 'A 2020 survey of more than 10,000 US adults found 1.7% currently had trichotillomania, with similar rates in men and women (Grant, Dougherty and Chamberlain, Psychiatry Research, 2020).'),
  ('Is trichotillomania a form of OCD?', 'It is grouped with obsessive-compulsive and related disorders in the DSM-5, but it is its own condition. Pulling is often driven by sensation, tension or emotion rather than obsessive thoughts, and in ICD-11 it sits among the body-focused repetitive behaviour disorders.'),
  ('Can trichotillomania go away on its own?', 'For some people it eases with time, but for many it continues into adulthood. Behaviour therapy with habit reversal training has the strongest evidence for reducing pulling.'),
  ('Will my hair grow back?', 'In most cases, yes. Hair usually regrows once pulling stops, although regrowth can take months, and repeated pulling from the same follicle over many years can sometimes damage it.')],
 ['apa2013','icd11','grant2020','tlc','flessner2008','mansueto1997','farhat2020','mcguire2014'])

# 2 ------------------------------------------------------------- treatments
page('trichotillomania-treatment',
 'Trichotillomania Treatment: What Works, Compared',
 'Trichotillomania treatments compared',
 'Learn · Treatment',
 'What actually works for hair pulling? Habit reversal training, the ComB model and acceptance-based therapy compared, with the research behind each and where an app fits.',
 lambda: f'''The treatment with the strongest evidence for trichotillomania is <strong>behaviour therapy built
 around habit reversal training (HRT)</strong>. A 2020 meta-analysis of 24 randomised trials (857 people) found a
 large benefit for HRT-based therapy.{cite('farhat2020')} The skills it teaches (noticing the urge, keeping your hands busy,
 changing your setup and riding the urge out) are things you can start practising today.''',
 lambda: f'''
<h2>Side by side</h2>
<div class="table-wrap">
<table>
 <caption>Trichotillomania treatments and what the research shows</caption>
 <thead><tr><th scope="col">Treatment</th><th scope="col">What it is</th><th scope="col">Evidence</th><th scope="col">Access</th></tr></thead>
 <tbody>
  <tr><th scope="row">Habit reversal training (HRT)</th><td>Awareness training, a competing response with the hands, and support. Developed by Azrin and Nunn{cite('azrin1973')}</td>
      <td><strong>Strongest.</strong> Large effect versus control (SMD −1.22) across randomised trials{cite('farhat2020')}; large pooled effect in an earlier meta-analysis{cite('mcguire2014')}</td><td>A psychologist, ideally one trained in BFRBs</td></tr>
  <tr><th scope="row">ComB model therapy</th><td>Maps triggers across sensory, cognitive, affective, motor and place (SCAMP) and builds a tool for each{cite('mansueto1997')}</td>
      <td>Builds on HRT; widely used by BFRB specialists. Fewer head-to-head trials than HRT</td><td>BFRB specialist therapists</td></tr>
  <tr><th scope="row">HRT plus acceptance (ACT)</th><td>Adds acceptance and commitment therapy so urges can be noticed without being obeyed</td>
      <td>Better than waitlist in a controlled trial{cite('woods2006')}. Adding emotion-focused components improved behaviour therapy results{cite('mcguire2014')}</td><td>Psychologists trained in ACT</td></tr>
  <tr><th scope="row">Medicines and supplements</th><td>Several have been studied in trials, with mixed results{cite('farhat2020')}</td>
      <td>None is approved specifically for trichotillomania. Not something to start on your own</td><td>Talk to your GP or a psychiatrist</td></tr>
 </tbody>
</table>
</div>
<p class="table-note">SMD = standardised mean difference. Bigger negative numbers mean a bigger drop in symptoms compared with control. Around 0.8 or more counts as large.</p>

<h2>Therapy vs apps vs doing it alone</h2>
<div class="table-wrap">
<table>
 <caption>Ways people get help, and the trade-offs</caption>
 <thead><tr><th scope="col"></th><th scope="col">BFRB therapist</th><th scope="col">Self-help app</th><th scope="col">On your own</th></tr></thead>
 <tbody>
  <tr><th scope="row">Evidence</th><td>Strongest (HRT, ComB, ACT)</td><td>Varies. Most apps borrow HRT principles; few have been tested in trials</td><td>Willpower alone rarely holds</td></tr>
  <tr><th scope="row">Cost</th><td>Highest. Often hundreds of dollars a month</td><td>Free to a few hundred dollars a year</td><td>Free</td></tr>
  <tr><th scope="row">There at 11pm</th><td>No</td><td>Yes</td><td>Yes</td></tr>
  <tr><th scope="row">Best for</th><td>Anyone who can access it, and anyone struggling a lot</td><td>Between sessions, waiting lists, people who can't reach a specialist</td><td>Learning the basics first</td></tr>
 </tbody>
</table>
</div>
<p>An app is not a replacement for a therapist. Where it earns its place is the moment a therapist can't be there: the urge at 11pm,
 on the couch, in the car. That is the gap <a href="/">Trich Reset</a> was built for, and its Stillness Protocol draws on habit reversal
 training, the ComB model and acceptance-based work. See how it compares in the <a href="/trichotillomania-apps">app comparison</a>.</p>

<h2>What habit reversal training involves</h2>
<ol>
 <li><strong>Awareness training.</strong> Learning exactly when, where and how you pull, including the warning signs before your hand moves.</li>
 <li><strong>Competing response.</strong> Doing something with your hands for about a minute that makes pulling impossible: making a fist, holding an object, sitting on your hands.</li>
 <li><strong>Stimulus control.</strong> Changing the setup: gloves while reading, a hat at the desk, dimmer bathroom lights.</li>
 <li><strong>Social support.</strong> Someone who gently notices and encourages you.</li>
</ol>
<p>The <a href="/how-to-stop-pulling-hair">practical guide</a> turns these into steps you can start today.</p>

{cta('trichotillomania-treatment', 'Between sessions, or before you can get one', 'Something for the urge, tonight.',
     'Trich Reset puts the research into guided audio made only for hair pulling. ' + FREE)}''',
 [('What is the most effective treatment for trichotillomania?', 'Behaviour therapy built around habit reversal training (HRT). A 2020 meta-analysis of 24 randomised trials found a large benefit for HRT-based therapy compared with control conditions (Farhat et al., Depression and Anxiety, 2020).'),
  ('Is there medication for trichotillomania?', 'Some medicines and supplements have been studied, with mixed results, and none is approved specifically for trichotillomania. A GP or psychiatrist can talk through whether anything is right for you. Behaviour therapy has the strongest evidence.'),
  ('Can an app help with trichotillomania?', 'An app is not a replacement for therapy, but it can help you practise the same skills between sessions or while you wait for one: noticing urges, riding them out and tracking your triggers. Trich Reset adds guided audio for the moment the urge arrives.'),
  ('How do I find a trichotillomania therapist?', 'The TLC Foundation for Body-Focused Repetitive Behaviors keeps a directory of clinicians trained in BFRBs at bfrb.org. Ask any therapist whether they use habit reversal training or the ComB model.')],
 ['farhat2020','mcguire2014','azrin1973','mansueto1997','woods2006'])

# 3 ------------------------------------------------------------------ apps
page('trichotillomania-apps',
 'Best Trichotillomania Apps (2026), Compared',
 'Apps for trichotillomania, compared',
 'Learn · Apps',
 'Most trich apps help you count your pulling. One is built to get you through the urge. A sourced side-by-side of Trich Reset, TrichStop, SkinAware and HabitAware Keen2.',
 lambda: f'''Most trichotillomania apps help you <strong>count</strong> your pulling. Trich Reset is built to get you
 <strong>through the urge itself</strong>: 21 guided meditations, hypnosis and sleep tracks made only for hair pulling, plus the
 SCAMP trigger map that BFRB specialists use. Here's how it stacks up against TrichStop, SkinAware and HabitAware Keen2. We make
 Trich Reset, so every claim about the other apps links to a source you can check.{cite('skinaware')}''',
 lambda: f'''
<h2>Side by side</h2>
<div class="table-wrap">
<table>
 <caption>Hair pulling apps compared (October 2026)</caption>
 <thead><tr><th scope="col"></th><th scope="col">Trich Reset</th><th scope="col">TrichStop</th><th scope="col">SkinAware</th><th scope="col">HabitAware Keen2</th></tr></thead>
 <tbody>
  <tr><th scope="row">Built for</th><td><strong>Getting through the urge.</strong> Guided audio for the moment your hand starts moving, plus a trigger map, tracking and lessons</td><td>A weekly online program with a therapist</td><td>Logging, with a habit reversal course written in general BFRB language rather than for pulling{cite('skinaware')}</td><td>A bracelet that vibrates when your hand moves to your hair</td></tr>
  <tr><th scope="row">Made only for hair pulling</th><td><strong>Yes.</strong> Every track and lesson</td><td>Yes</td><td>No. Also covers skin picking and other BFRBs{cite('skinaware')}</td><td>No. Also used for skin picking and nail biting</td></tr>
  <tr><th scope="row">Guided audio</th><td><strong>21 tracks, over six hours.</strong> Urge resets from 4 minutes, protocols, hypnosis, affirmations, sleep up to 60 minutes. New tracks monthly</td><td>Mindfulness exercises{cite('skinaware')}</td><td>Breathing and urge-surfing tools{cite('skinaware')}</td><td>Not a focus</td></tr>
  <tr><th scope="row">Hypnosis and sleep tracks</th><td><strong>Yes</strong></td><td>Not listed{cite('skinaware')}</td><td>Not listed{cite('skinaware')}</td><td>Not listed{cite('skinaware')}</td></tr>
  <tr><th scope="row">Find your triggers</th><td><strong>SCAMP profile questionnaire</strong> (ComB model) across 5 trigger areas</td><td>Worked through with your therapist</td><td>From your logs</td><td>Detects the hand movement</td></tr>
  <tr><th scope="row">Education</th><td>3 modules, 17 lessons written for hair pulling</td><td>Structured program</td><td>3-module HRT course</td><td>Course sold separately{cite('skinaware')}</td></tr>
  <tr><th scope="row">Tracking</th><td>Urge and pull logs, check-ins, recovery-aware streaks, private regrowth photos</td><td>Self-monitoring</td><td>Detailed logging, widgets</td><td>Automatic + manual</td></tr>
  <tr><th scope="row">Price</th><td><strong>A$199.99/year</strong> (early bird), A$249.99/year or A$26.99/month</td><td>US$60–90 per week{cite('skinaware')}, which is US$3,120 or more over a year</td><td>Free core; premium US$5.99/month or US$34.99/year{cite('skinaware')}</td><td>US$169 bracelet; HRT content extra{cite('skinaware')}</td></tr>
  <tr><th scope="row">Free option</th><td>One full meditation free on <a href="/#listen">trichreset.com</a></td><td>No free tier{cite('skinaware')}</td><td>Yes, core logging</td><td>App logging free</td></tr>
  <tr><th scope="row">Real therapist</th><td>No</td><td>Yes</td><td>No</td><td>No</td></tr>
  <tr><th scope="row">Detects pulling automatically</th><td>No</td><td>No</td><td>No</td><td>Yes</td></tr>
  <tr><th scope="row">Platforms</th><td>Android (iOS coming)</td><td>iOS, Android</td><td>iOS, Android, Apple Watch, web</td><td>Bracelet + iOS/Android app</td></tr>
 </tbody>
</table>
</div>
<p class="table-note">Third-party prices and features are from SkinAware's published comparison (updated 20 August 2026){cite('skinaware')} and may have changed. Check each store before you buy.</p>

<h2>Which one fits you</h2>
<div class="table-wrap">
<table>
 <caption>Match the app to the problem</caption>
 <thead><tr><th scope="col">If this sounds like you</th><th scope="col">Look at</th></tr></thead>
 <tbody>
  <tr><td>You know when the urge hits, and need something to do in that moment</td><td><strong>Trich Reset.</strong> This is exactly what it's built for</td></tr>
  <tr><td>You pull in bed, or in the hour before sleep</td><td><strong>Trich Reset.</strong> Four sleep tracks, 20 to 60 minutes</td></tr>
  <tr><td>You've never been sure why you pull</td><td><strong>Trich Reset.</strong> The SCAMP lessons and questionnaire map your triggers</td></tr>
  <tr><td>You mostly pull without noticing (automatic pulling)</td><td><strong>Trich Reset's</strong> Automatic Pulling Protocol, plus a wearable such as Keen2 if you want a buzz on your wrist</td></tr>
  <tr><td>You want weekly sessions with a specialist and can pay US$60–90 a week</td><td>TrichStop or a local BFRB therapist, with Trich Reset for the moments in between</td></tr>
  <tr><td>You're on iPhone</td><td>SkinAware for now. Trich Reset for iOS is coming</td></tr>
 </tbody>
</table>
</div>

<h2>What makes a good trich app</h2>
<ul>
 <li><strong>Built on the research.</strong> Habit reversal training has the strongest evidence, and the ComB model builds on it. See <a href="/trichotillomania-treatment">treatments compared</a>. <em>Trich Reset's Stillness Protocol draws on both, and its lessons are built on SCAMP.</em></li>
 <li><strong>Help in the moment, not only afterwards.</strong> A log tells you what happened. The urge needs something now. <em>Trich Reset's resets start at four minutes.</em></li>
 <li><strong>Fast to use.</strong> If logging takes a minute, you will stop by week two. <em>Trich Reset logs a pull in a few taps.</em></li>
 <li><strong>Doesn't punish a bad day.</strong> Shame keeps the cycle going. Streaks that reset to zero can make things worse. <em>Trich Reset's streaks count the days you show up.</em></li>
 <li><strong>Private.</strong> You should be able to delete everything yourself. <em>In Trich Reset it's one button.</em></li>
 <li><strong>Honest about what it is.</strong> No app is a medical treatment. Be wary of "cure" claims.</li>
</ul>

{cta('trichotillomania-apps', 'Try before you pay', 'Hear Trich Reset for yourself, free.', FREE)}
''',
 [('What is the best app for trichotillomania?', 'It depends on what you need. For help in the moment the urge hits, Trich Reset: it is the only app in this comparison with a full guided audio library made for hair pulling, including hypnosis and sleep tracks. TrichStop connects you with a specialist therapist (about US$60–90 a week). HabitAware Keen2 is a bracelet that detects automatic pulling. SkinAware offers detailed logging and a habit reversal course with a free tier.'),
  ('Is there a free app for hair pulling?', 'SkinAware has a free core logging tier, and the HabitAware app is free for manual logging. Trich Reset lets you hear a full ten-minute meditation free on its website, no signup. Fully featured apps generally need a subscription.'),
  ('Do trichotillomania apps work?', 'Most apps use principles from habit reversal training, which has strong evidence as a therapy. Few apps have been tested in their own clinical trials, so treat any app as support rather than treatment.'),
  ('Is Trich Reset on iPhone?', 'Not yet. Trich Reset is on Android through Google Play, with iOS planned.')],
 ['skinaware'])

# 4 ---------------------------------------------------------------- how-to
page('how-to-stop-pulling-hair',
 'How to Stop Pulling Your Hair: A Research-Based Guide',
 'How to stop pulling your hair',
 'Learn · Practical guide',
 'Practical, research-based steps to stop pulling your hair: spot your triggers, use a competing response, change your setup and ride out the urge. Includes a trigger-to-tool table.',
 lambda: f'''The approach with the most research behind it is <strong>habit reversal training</strong>:{cite('farhat2020')}
 notice the warning signs, give your hands a competing job for about a minute, change the places where pulling
 happens, and get support. Pair it with a plan for the urge itself. Urges rise, peak and pass, and you don't have
 to win or lose each one.{cite('woods2006')}''',
 lambda: f'''
<h2>1. Find your pattern first</h2>
<p>For a week, write down every pull or strong urge: the time, where you were, what you were doing, and what you felt. Most people
 find two or three situations account for most of their pulling. The ComB model sorts triggers into five areas (SCAMP),{cite('mansueto1997')}
 explained on <a href="/what-is-trichotillomania">what is trichotillomania</a>.</p>

<h2>2. Match a tool to each trigger</h2>
<div class="table-wrap">
<table>
 <caption>Trigger-to-tool table</caption>
 <thead><tr><th scope="col">If you pull when…</th><th scope="col">Area</th><th scope="col">Try</th></tr></thead>
 <tbody>
  <tr><td>A hair feels coarse, kinked or "wrong"</td><td>Sensory</td><td>A textured fidget in the same hand (a smooth stone, a hairbrush, Velcro); run your fingers through your hair without pulling</td></tr>
  <tr><td>You think "just one more"</td><td>Cognitive</td><td>Name the thought as a thought: "That's the urge talking." Delay by 10 minutes</td></tr>
  <tr><td>You're stressed, bored or anxious</td><td>Affective</td><td>A short guided reset or slow breathing until the wave passes; move your body</td></tr>
  <tr><td>Your hand rests on your head while reading or scrolling</td><td>Motor</td><td>Competing response: make a fist or hold an object for 1 minute; gloves or finger tape during high-risk activities</td></tr>
  <tr><td>You're in front of the mirror, in bed, or in the car</td><td>Place</td><td>Dim or cover the mirror, keep tweezers out of reach, a hat or bandana in high-risk places</td></tr>
 </tbody>
</table>
</div>

<h2>3. Use a competing response</h2>
<p>This is the core of habit reversal training.{cite('azrin1973')} As soon as you notice the urge or your hand moving, do something
 with your hands for about one minute that makes pulling physically impossible and isn't noticeable to others: clench your fists,
 press your palms together, sit on your hands, or hold an object. Practise it when you're calm so it is ready when you're not.</p>

<h2>4. Ride the urge out instead of fighting it</h2>
<p>Acceptance-based therapy treats an urge as something you can notice without obeying.{cite('woods2006')} Try this:</p>
<ol>
 <li>Name it: "There's the urge."</li>
 <li>Find where you feel it in your body, and rate it from 1 to 10.</li>
 <li>Breathe slowly and watch the number. Urges peak, then fall.</li>
 <li>Keep your hands busy with your competing response while it passes.</li>
</ol>
<p>When you can't think straight, a voice in your ear can carry you through it. That is exactly what
 <a href="/">Trich Reset</a> is built for: guided resets from four minutes, made only for hair pulling.
 <a href="/#listen">Hear a full one free</a>.</p>

<h2>5. Expect slips, and count the hard days</h2>
<p>Recovery is rarely a straight line. Shame after a slip often leads to more pulling. Track the days you showed up, not only the clean ones,
 so you can see the trend over weeks rather than judging yourself on one night. Trich Reset's streaks work exactly this way: a hard day
 still counts.</p>

<h2>When to get professional help</h2>
<p>If pulling is causing noticeable hair loss, affecting your work, school or relationships, or you feel low or hopeless, see a doctor or
 psychologist. A therapist trained in habit reversal training or the ComB model gives you the best-evidenced help. The TLC Foundation
 lists BFRB clinicians at <a href="https://www.bfrb.org">bfrb.org</a>. If you are in crisis in Australia, call Lifeline on 13 11 14.</p>

{cta('how-to-stop-pulling-hair', 'For the ten seconds your hand starts moving', 'Press play when the urge hits.', FREE)}''',
 [('How do I stop pulling my hair right now?', 'Give your hands a competing job for about a minute: clench your fists, hold an object or sit on your hands. Then name the urge, breathe slowly and wait for it to peak and pass.'),
  ('What can I do instead of pulling my hair?', 'Use a competing response that keeps your hands busy (a fidget, a smooth stone, a hairbrush), wear gloves or a hat during high-risk activities, and change the places where you pull, such as covering or dimming the mirror.'),
  ("Why can't I stop pulling my hair?", 'Trichotillomania is a body-focused repetitive behaviour, not a lack of willpower. Pulling is triggered and reinforced by sensations, thoughts, emotions, habits and places. Tools that target your specific triggers work better than trying to just stop.'),
  ('Does wearing gloves help with hair pulling?', 'Gloves, finger tape or a hat are a form of stimulus control used in habit reversal training. They are most useful during predictable high-risk times, like reading, watching TV or lying in bed.')],
 ['farhat2020','woods2006','mansueto1997','azrin1973'])

# 5 ------------------------------------------------------------------ ADHD
page('trichotillomania-and-adhd',
 'Trichotillomania and ADHD: Why They Overlap and What Helps',
 'Trichotillomania and ADHD',
 'Learn · ADHD',
 'Up to 3 in 10 adults with trichotillomania also report ADHD. Why hair pulling and ADHD overlap, and practical tools that suit an ADHD brain, with research sources.',
 lambda: f'''ADHD is common in people with trichotillomania. In a study of 308 adults with trich, <strong>15.3%</strong>
 met the clinical threshold for ADHD{cite('chesivoir2022')}, and in a US survey <strong>29%</strong> of people with trich
 reported ADHD{cite('grant2020','farhat2025')}, compared with about <strong>2.5%</strong> of adults overall.{cite('simon2009')}
 They are separate conditions, but impulsivity, boredom and restless hands connect them, so tools that keep your hands busy and
 your setup simple are a good place to start.''',
 lambda: f'''
<h2>How often they occur together</h2>
<div class="table-wrap">
<table>
 <caption>ADHD and trichotillomania: what the research found</caption>
 <thead><tr><th scope="col">Study</th><th scope="col">Who was studied</th><th scope="col">Finding</th></tr></thead>
 <tbody>
  <tr><th scope="row">Chesivoir, Valle and Grant, 2022</th><td>308 adults with a current trichotillomania diagnosis</td><td>15.3% met the clinical threshold for ADHD{cite('chesivoir2022')}</td></tr>
  <tr><th scope="row">Grant, Dougherty and Chamberlain, 2020</th><td>175 US adults with trichotillomania, from a survey of 10,169</td><td>29% reported ADHD; 79% had at least one other mental health condition{cite('grant2020','farhat2025')}</td></tr>
  <tr><th scope="row">Farhat and colleagues, 2025</th><td>1,234 people diagnosed with trichotillomania in Sweden</td><td>39% also had a neurodevelopmental diagnosis, the group that includes ADHD{cite('farhat2025')}</td></tr>
  <tr><th scope="row">Simon and colleagues, 2009</th><td>Adults in general (meta-analysis)</td><td>About 2.5% have ADHD{cite('simon2009')}</td></tr>
 </tbody>
</table>
</div>
<p class="table-note">The studies used different methods (clinical interviews, self-report surveys and health records), which is why the numbers vary.</p>

<h2>Is hair pulling a symptom of ADHD?</h2>
<p>No. Trichotillomania is its own condition, classed as a body-focused repetitive behaviour.{cite('apa2013')} Many people
 have one without the other. But when they show up together, each can make the other harder to manage, so it helps to understand both.</p>

<h2>Why they overlap</h2>
<ul>
 <li><strong>Impulsivity.</strong> In the 2022 study, people with both conditions scored higher on every measure of impulsivity:
  acting on the spot, attention drifting and not planning ahead.{cite('chesivoir2022')} The gap between an urge and your hand
  moving can feel shorter.</li>
 <li><strong>Restless, under-stimulated moments.</strong> Automatic pulling tends to happen while sitting still: reading, studying,
  scrolling, watching TV, lying in bed.{cite('flessner2008')} Those are the same moments an ADHD brain goes looking for stimulation.</li>
 <li><strong>Hands that want a job.</strong> Pulling gives the hands something to do and the senses something to focus on. The sensory
  and motor parts of the SCAMP model describe exactly this.{cite('mansueto1997')}</li>
 <li><strong>Plans that slip.</strong> ADHD makes it harder to remember a strategy in the moment, so tools need to be visible and
  within reach, not just in your head.</li>
</ul>
<p>One encouraging finding: in the 2022 study, people with both conditions did not have more severe pulling, or a lower quality of
 life, than people with trich alone.{cite('chesivoir2022')}</p>

<h2>Tools that suit an ADHD brain</h2>
<div class="table-wrap">
<table>
 <caption>Common ADHD pulling situations, and what to try</caption>
 <thead><tr><th scope="col">If you pull when…</th><th scope="col">Try</th></tr></thead>
 <tbody>
  <tr><td>Your hands are free while studying, working or on a screen</td><td>A fidget in the hand you pull with, kept on the desk where you can see it. Thin gloves or a beanie during long focus sessions</td></tr>
  <tr><td>You're bored or under-stimulated</td><td>Short movement breaks, background audio, or a short guided track instead of sitting with nothing to do</td></tr>
  <tr><td>You forget your plan the moment the urge hits</td><td>Put tools where pulling happens, not in a drawer. A sticky note on the mirror or laptop. One plan, not five</td></tr>
  <tr><td>You lose track of time scrolling in bed</td><td>Phone charging out of reach, hair tied up, and sleep audio instead of the feed</td></tr>
  <tr><td>"Just one" turns into twenty minutes</td><td>A competing response the second you notice: make a fist or hold an object for one minute.{cite('azrin1973')} Delay, don't negotiate</td></tr>
  <tr><td>Tracking feels like homework</td><td>Log in a few taps or not at all. A rough count you keep beats a detailed diary you drop</td></tr>
 </tbody>
</table>
</div>
<p>These come from habit reversal training, the approach with the strongest evidence for trichotillomania,{cite('farhat2020')}
 adapted to be short, visible and hands-on. The <a href="/how-to-stop-pulling-hair">practical guide</a> goes deeper on each step.</p>

<h2>Where Trich Reset fits</h2>
<p>Most self-help asks you to remember a technique when your brain is at its busiest. <a href="/">Trich Reset</a> is built the other
 way round: press play and a voice walks you through it. Resets start at four minutes, the Automatic Pulling Protocol is made for
 pulling you don't notice, sleep tracks replace the late-night scroll, and logging takes a few taps. The SCAMP questionnaire shows which
 of your triggers are sensory, emotional or habit-based, so you know where to start.</p>

<h2>When to get professional help</h2>
<p>If you think you might have ADHD, start with your GP, who can refer you for an assessment. For pulling, a therapist trained in habit
 reversal training or the ComB model gives you the best-evidenced help, and the TLC Foundation lists BFRB clinicians at
 <a href="https://www.bfrb.org">bfrb.org</a>. Tell any clinician you see about both, because a plan that works for one should fit the
 other. If you are in crisis in Australia, call Lifeline on 13 11 14.</p>

{cta('trichotillomania-and-adhd', 'Short, guided, hands-free', "Something for the urge that you don't have to remember.",
     'Trich Reset has 21 guided meditations, hypnosis and sleep tracks made only for hair pulling. ' + FREE)}''',
 [('Is trichotillomania a symptom of ADHD?', 'No. Trichotillomania is a separate condition, a body-focused repetitive behaviour. The two often occur together: in one study of 308 adults with trichotillomania, 15.3% also met the threshold for ADHD.'),
  ('How common is ADHD in people with trichotillomania?', 'Studies range from about 15% (a 2022 clinical study of 308 adults) to 29% (a 2020 US survey), compared with about 2.5% of adults in general.'),
  ('Does ADHD make hair pulling worse?', 'People with both conditions tend to be more impulsive, but a 2022 study found their pulling was not more severe, and their quality of life was no lower, than people with trichotillomania alone.'),
  ('What helps hair pulling if you have ADHD?', 'The same habit reversal skills, made short and visible: a fidget kept where you pull, gloves or a hat during long focus sessions, one simple plan, and guided audio so you do not have to remember the steps yourself.')],
 ['chesivoir2022','grant2020','farhat2025','simon2009','apa2013','flessner2008','mansueto1997','azrin1973','farhat2020'])

# 6 ------------------------------------------------------------- Australia
page('trichotillomania-help-australia',
 'Trichotillomania Help in Australia: Medicare, Psychologists and Support',
 'Trichotillomania help in Australia',
 'Learn · Australia',
 'How to get help for hair pulling in Australia: a GP mental health treatment plan, up to 10 Medicare-rebated psychology sessions a year, finding a BFRB-trained psychologist, and who to call.',
 lambda: f'''In Australia, start with your <strong>GP</strong>. They can write a <strong>mental health treatment plan</strong>
 and refer you to a psychologist, and Medicare then pays part of the cost of <strong>up to 10 individual sessions</strong>
 (and 10 group sessions) each calendar year.{cite('sa-medicare','betteraccess')} The first referral is for up to 6 sessions,
 then your GP reviews and can refer you for more.{cite('sa-medicare')} Ask for a psychologist who uses <strong>habit reversal
 training</strong>, the treatment with the strongest evidence for trichotillomania.{cite('farhat2020')}''',
 lambda: f'''
<h2>Step by step</h2>
<div class="table-wrap">
<table>
 <caption>Getting Medicare-rebated help for hair pulling in Australia</caption>
 <thead><tr><th scope="col">Step</th><th scope="col">What to do</th><th scope="col">Tip</th></tr></thead>
 <tbody>
  <tr><th scope="row">1. Book your GP</th><td>Ask for a long appointment and say it's about a mental health treatment plan</td><td>Say the words "trichotillomania" or "hair pulling disorder". Many people only ever mention hair loss, and get sent to a dermatologist</td></tr>
  <tr><th scope="row">2. Get the plan and a referral</th><td>Your GP writes the plan and refers you for up to 6 sessions{cite('sa-medicare')}</td><td>A psychiatrist or paediatrician can also refer{cite('sa-medicare')}. For children, a paediatrician is often the easier door</td></tr>
  <tr><th scope="row">3. Find the right psychologist</th><td>A clinical or registered psychologist, occupational therapist or social worker can be eligible{cite('sa-medicare')}</td><td>Ask before booking: "Do you use habit reversal training or the ComB model, and have you treated trichotillomania?"</td></tr>
  <tr><th scope="row">4. Go back for a review</th><td>After your first sessions, your GP can refer you for more, up to 10 individual sessions in the calendar year{cite('sa-medicare')}</td><td>The count resets on 1 January</td></tr>
 </tbody>
</table>
</div>

<h2>What it costs</h2>
<p>Medicare pays a rebate for each eligible session, and many psychologists charge more than the rebate, so expect a gap fee. It varies
 a lot between practices, so ask when you book. Some bulk bill, especially for students, concession card holders or children.</p>
<div class="table-wrap">
<table>
 <caption>What Medicare covers under a mental health treatment plan</caption>
 <tbody>
  <tr><th scope="row">Individual sessions</th><td>Up to 10 per calendar year{cite('sa-medicare','betteraccess')}</td></tr>
  <tr><th scope="row">Group sessions</th><td>Up to 10 per calendar year{cite('sa-medicare','betteraccess')}</td></tr>
  <tr><th scope="row">Per referral</th><td>Up to 6 sessions, then a GP review{cite('sa-medicare')}</td></tr>
  <tr><th scope="row">Video sessions</th><td>Can be claimed, which helps if you live regionally or remotely{cite('sa-medicare')}</td></tr>
  <tr><th scope="row">Carers and parents</th><td>Can join up to 2 sessions a year as part of the plan of the person they care for (these count towards the 10){cite('sa-medicare')}</td></tr>
 </tbody>
</table>
</div>

<h2>Finding a psychologist who knows trich</h2>
<p>BFRB specialists are thin on the ground in Australia, so widen the search:</p>
<ul>
 <li><strong>The TLC Foundation directory</strong> at <a href="https://www.bfrb.org">bfrb.org</a> lists clinicians trained in body-focused repetitive behaviours, including some outside the US.{cite('tlc')}</li>
 <li><strong>The Australian Psychological Society's Find a Psychologist</strong> at <a href="https://www.findapsychologist.org.au">findapsychologist.org.au</a>. Search for "habit reversal", "BFRB" or "OCD and related disorders".</li>
 <li><strong>Video sessions</strong> mean the right psychologist doesn't have to be in your city.{cite('sa-medicare')}</li>
 <li>If you can't find a trich specialist, a psychologist experienced with <strong>OCD and related disorders</strong> and habit reversal training is a sound second choice.</li>
</ul>

<h2>While you wait</h2>
<p>Waiting lists can run for months. You don't have to wait to start. The <a href="/how-to-stop-pulling-hair">practical guide</a> covers the
 habit reversal steps you can begin today, and <a href="/">Trich Reset</a> is made for the moments between sessions: guided audio for
 the urge, a SCAMP trigger map you can take to your first appointment, and logs that show your psychologist your real pattern.
 Trich Reset is made by Lux Innovations, a small Australian company.</p>

<h2>If you need to talk to someone now</h2>
<div class="table-wrap">
<table>
 <caption>Australian support lines</caption>
 <tbody>
  <tr><th scope="row">Lifeline</th><td>13 11 14, 24 hours, crisis support</td></tr>
  <tr><th scope="row">Beyond Blue</th><td>1300 22 4636, 24 hours, anxiety and low mood</td></tr>
  <tr><th scope="row">Kids Helpline</th><td>1800 55 1800, 24 hours, for ages 5 to 25</td></tr>
  <tr><th scope="row">Emergency</th><td>000</td></tr>
 </tbody>
</table>
</div>

{cta('trichotillomania-help-australia', 'Made in Australia', 'Something for the urge, tonight, before your first session.',
     'Trich Reset has 21 guided meditations, hypnosis and sleep tracks made only for hair pulling. ' + FREE)}''',
 [('Does Medicare cover a psychologist for trichotillomania?', 'Yes. With a mental health treatment plan from your GP, Medicare pays a rebate for up to 10 individual and 10 group sessions with an eligible psychologist, occupational therapist or social worker each calendar year. Many practices charge a gap on top.'),
  ('How do I get a mental health treatment plan?', 'Book a long appointment with your GP and say it is for a mental health treatment plan. Your GP assesses you, writes the plan and refers you for up to 6 sessions, then reviews you and can refer you for more.'),
  ('How do I find a trichotillomania specialist in Australia?', 'Check the TLC Foundation directory at bfrb.org and the Australian Psychological Society\'s Find a Psychologist. Ask whether they use habit reversal training or the ComB model. Video sessions are claimable, so the psychologist does not have to be local.'),
  ('Can I see a dermatologist for hair pulling?', 'A dermatologist can rule out other causes of hair loss and help with the skin, but trichotillomania is treated with behaviour therapy, so you will also need a psychologist. Tell your GP it is hair pulling, not only hair loss.')],
 ['sa-medicare','betteraccess','farhat2020','tlc'])

# 7 -------------------------------------------------------------- children
page('trichotillomania-in-children',
 'Trichotillomania in Children: A Guide for Parents',
 'Trichotillomania in children',
 'Learn · For parents',
 'Is your child pulling out their hair? What trichotillomania looks like at each age, what helps and what makes it worse, and how behaviour therapy helped 75% of children in a trial.',
 lambda: f'''Trichotillomania often starts in <strong>late childhood or early puberty</strong>,{cite('tlc')} and children respond well to
 treatment. In a randomised trial of children aged 7 to 17, <strong>75%</strong> responded to eight weeks of behaviour therapy, compared with
 <strong>0%</strong> in the comparison group, and 7 to 9-year-olds did as well as the older children.{cite('franklin2011')} The most useful
 thing a parent can be is a calm coach, not the hair police.{cite('tlc2011')}''',
 lambda: f'''
<h2>What it looks like at each age</h2>
<div class="table-wrap">
<table>
 <caption>Hair pulling by age, and the parent's role (from the TLC expert guidelines)</caption>
 <thead><tr><th scope="col">Age</th><th scope="col">What it's like</th><th scope="col">Your role</th></tr></thead>
 <tbody>
  <tr><th scope="row">0 to 5 ("baby trich")</th><td>Often pulling while falling asleep, sucking a thumb or being comforted. Very young children often respond very well to treatment{cite('tlc2011')}</td><td>You run it, with a therapist's guidance: you set the routine and the environment{cite('tlc2011')}</td></tr>
  <tr><th scope="row">6 to 9</th><td>More able to take part and talk about it{cite('tlc2011')}</td><td>A reward system for <em>using strategies</em>, not for "not pulling"{cite('tlc2011')}</td></tr>
  <tr><th scope="row">10 to 13</th><td>More independent, still needs structure{cite('tlc2011')}</td><td>Let them help design their own plan; rewards still work{cite('tlc2011')}</td></tr>
  <tr><th scope="row">14 to 18</th><td>Privacy matters a lot, and shame can be intense{cite('tlc2011')}</td><td>Step back. Support, and let the work happen between them and their therapist{cite('tlc2011')}</td></tr>
 </tbody>
</table>
</div>

<h2>What helps, and what makes it worse</h2>
<div class="table-wrap">
<table>
 <caption>For parents: do and don't</caption>
 <thead><tr><th scope="col">Instead of…</th><th scope="col">Try…</th></tr></thead>
 <tbody>
  <tr><td>"Stop it!", or pulling their hand away</td><td>A quiet signal you agreed on together, or handing them their fidget</td></tr>
  <tr><td>Punishing or taking things away after pulling</td><td>Praising the moments they used a strategy. Shame tends to feed the cycle</td></tr>
  <tr><td>Checking their head or counting hairs</td><td>Asking, once a week and calmly, how their plan is going</td></tr>
  <tr><td>Telling them to just use willpower</td><td>Changing the setup: hair tied back or a beanie at bedtime, a fidget at homework time, gloves for screen time</td></tr>
  <tr><td>Keeping it a family secret</td><td>Naming it plainly: "It's called trichotillomania. Lots of kids have it, and it can get better."</td></tr>
 </tbody>
</table>
</div>
<p>These follow habit reversal training, the best-evidenced treatment,{cite('farhat2020')} which the children's trial adapted for kids.{cite('franklin2011')}
 The <a href="/how-to-stop-pulling-hair">practical guide</a> explains each step, and the trigger table there works well as a family worksheet.</p>

<h2>One thing to watch for</h2>
<p>Some children chew or swallow the hair they pull. Over time this can form a hairball in the stomach (a trichobezoar), which may need
 surgery.{cite('tlc')} If your child eats hair and has stomach pain, nausea, vomiting or a poor appetite, see a doctor.</p>

<h2>Getting help</h2>
<p>Start with your GP or paediatrician, and say "trichotillomania". Ask for a psychologist experienced with children and habit reversal
 training. In Australia, Medicare rebates up to 10 sessions a year with a mental health treatment plan, and a paediatrician can refer.
 Parents can join sessions as part of their child's plan.{cite('sa-medicare')} See <a href="/trichotillomania-help-australia">trichotillomania
 help in Australia</a> for the steps, and the TLC Foundation directory at <a href="https://www.bfrb.org">bfrb.org</a> to find a BFRB-trained clinician.</p>

<h2>Where Trich Reset fits</h2>
<p><a href="/">Trich Reset</a> is made for teenagers and adults. For an older child, it gives them something private to press play on
 when the urge hits, without a parent watching. For a younger child, it is a good way for <em>you</em> to understand trich: the SCAMP
 lessons explain why pulling happens and which tools fit which triggers.</p>

{cta('trichotillomania-in-children', 'For you, or for your teen', 'Hear what Trich Reset sounds like.', FREE)}''',
 [('Why is my child pulling out their hair?', 'Hair pulling in children is usually linked to soothing, boredom, tiredness or stress, and often happens while falling asleep, reading or watching a screen. When it is repeated and hard to stop, it may be trichotillomania, which commonly starts in late childhood or early puberty.'),
  ('Will my child grow out of trichotillomania?', 'Some very young children ("baby trich") do, but many do not without help. The good news is that children respond well to behaviour therapy: in one trial, 75% of children aged 7 to 17 responded after eight weeks.'),
  ('Should I tell my child to stop pulling?', 'Telling them to stop, punishing or checking their hair tends to add shame, which can make pulling worse. Agree a quiet signal together, praise them for using strategies, and change the setup, such as tying hair back at bedtime.'),
  ('What kind of doctor treats trichotillomania in children?', 'Start with your GP or paediatrician. Treatment is behaviour therapy with a psychologist, ideally one experienced with children and habit reversal training. The TLC Foundation lists BFRB clinicians at bfrb.org.')],
 ['tlc','franklin2011','tlc2011','farhat2020','sa-medicare'])

# ------------------------------------------------------------- templates
NAV = '''<header class="nav dark-zone" id="nav">
  <div class="container nav-inner">
    <a class="wordmark" href="/">
      <img src="/assets/img/app-icon-64.png" width="32" height="32" alt="Trich Reset app icon">
      <span>Trich Reset</span>
    </a>
    <nav class="nav-links" aria-label="Sections">
      <a href="/#listen">Listen</a>
      <a href="/learn">Learn</a>
      <a href="/#pricing">Pricing</a>
    </nav>
    <a class="btn btn-primary nav-cta" href="{play}">Get Trich Reset on Google Play</a>
  </div>
</header>'''

FOOT = '''<footer class="learn-foot dark-zone">
  <div class="container">
    <p><strong>Learn:</strong> {links}</p>
    <p><a href="/">Trich Reset</a> · <a href="/privacy">Privacy</a> · <a href="mailto:trichreset@gmail.com">trichreset@gmail.com</a></p>
    <p class="muted">© 2026 Trich Reset, made by Lux Innovations.</p>
  </div>
</footer>'''

HEAD = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{url}">
<meta name="theme-color" content="#0D1B2A">
<meta property="og:type" content="article">
<meta property="og:site_name" content="Trich Reset">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="https://trichreset.com/assets/img/og-image.jpg">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/assets/img/app-icon-64.png" sizes="64x64">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Figtree:wght@400;500&family=Nunito+Sans:wght@400;500&display=swap">
<link rel="stylesheet" href="/brand-tokens.css">
<link rel="stylesheet" href="/styles.css">
<link rel="stylesheet" href="/learn.css">
{schema}
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
'''

AUTHOR = {'@type': 'Organization', 'name': 'Trich Reset', 'url': SITE}
PUBLISHER = {'@type': 'Organization', 'name': 'Lux Innovations', 'url': SITE,
             'logo': {'@type': 'ImageObject', 'url': SITE + '/assets/img/app-icon-180.png'}}

def schema_tags(objs):
    return '\n'.join('<script type="application/ld+json">\n' + json.dumps(o, ensure_ascii=False, indent=1) + '\n</script>' for o in objs)

def foot():
    return FOOT.format(links=' · '.join(f'<a href="/{p["slug"]}">{p["h1"]}</a>' for p in PAGES))

# One image per guide for the 50/50 header and the hub rows.
# 'art' = square trich image (assets/img/learn, made by tools/learn_art.py), 'phone' = real app screen.
IMAGES = {
    'what-is-trichotillomania': ('assets/img/learn/what-is-v2', 'Late at night in bed, scrolling a phone, one of the most common times hair pulling starts', 'art'),
    'trichotillomania-treatment': ('assets/img/learn/treatment-v2', 'An urge log notebook with tally marks, a pen, a worry stone and a cup of tea', 'art'),
    'trichotillomania-apps': ('assets/img/app/screen-4', 'Trich Reset app screen: the Listen tab with urge resets, sleep and grounding tracks', 'phone'),
    'trichotillomania-and-adhd': ('assets/img/learn/adhd', 'A study desk at night: open laptop and textbook, a cup of tea, and a hand turning a fidget cube instead of reaching for hair', 'art'),
    'how-to-stop-pulling-hair': ('assets/img/learn/how-to-stop-v2', 'A bathroom mirror covered with a towel, with a scrunchie and fidget spinner on the sink', 'art'),
    'trichotillomania-help-australia': ('assets/img/learn/australia', 'A kitchen table in morning light with a phone, a notepad of tick boxes ready for a GP appointment, and a sprig of eucalyptus', 'art'),
    'trichotillomania-in-children': ('assets/img/learn/children', "A child's hand holding a soft fidget toy on a duvet, with a parent's hand resting gently beside it", 'art'),
}
HUB_ORDER = ['what-is-trichotillomania', 'how-to-stop-pulling-hair', 'trichotillomania-in-children', 'trichotillomania-help-australia',
             'trichotillomania-apps', 'trichotillomania-and-adhd', 'trichotillomania-treatment']
HUB_IMAGE = ('assets/img/learn/hub-v2', 'A trichotillomania toolkit: fidget ring, stress ball, beanie, cotton gloves, scrunchie, worry stone, hairbrush and phone', 'art')

def figure(img, eager=False):
    src, alt, kind = img
    w, h = (540, 960) if kind == 'phone' else (720, 720)
    load = 'fetchpriority="high"' if eager else 'loading="lazy"'
    return (f'<figure class="split-media split-{kind}"><picture><source type="image/webp" srcset="/{src}.webp">'
            f'<img src="/{src}.jpg" width="{w}" height="{h}" alt="{html.escape(alt)}" {load} decoding="async"></picture></figure>')

def render(p):
    global ORDER
    ORDER = p['sources']
    url = f"{SITE}/{p['slug']}"
    summary, body = p['summary'](), p['body']()
    faq_html = ''.join(f'<details><summary>{html.escape(q)}</summary><p>{html.escape(a)}</p></details>' for q, a in p['faqs'])
    src_html = ''.join(f'<li id="src-{k}">{S[k][0]} <a href="{S[k][1]}" rel="noopener">{html.escape(S[k][1])}</a></li>' for k in ORDER)
    schema = schema_tags([
        {'@context': 'https://schema.org', '@type': 'Article', 'headline': p['h1'], 'description': p['desc'],
         'datePublished': UPDATED, 'dateModified': UPDATED, 'author': AUTHOR, 'publisher': PUBLISHER,
         'mainEntityOfPage': url, 'image': SITE + '/assets/img/og-image.jpg',
         'citation': [S[k][1] for k in ORDER]},
        {'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': [
            {'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in p['faqs']]},
        {'@context': 'https://schema.org', '@type': 'BreadcrumbList', 'itemListElement': [
            {'@type': 'ListItem', 'position': 1, 'name': 'Trich Reset', 'item': SITE + '/'},
            {'@type': 'ListItem', 'position': 2, 'name': 'Learn', 'item': SITE + '/learn'},
            {'@type': 'ListItem', 'position': 3, 'name': p['h1'], 'item': url}]},
    ])
    out = HEAD.format(title=html.escape(p['title']), desc=html.escape(p['desc']), url=url, schema=schema)
    out += NAV.format(play=PLAY.format(slug=p['slug']))
    out += f'''
<main id="main" class="learn">
 <header class="container split split-hero">
  <div class="split-copy">
   <nav class="crumbs" aria-label="Breadcrumb"><a href="/">Trich Reset</a> › <a href="/learn">Learn</a> › <span>{p['h1']}</span></nav>
   <p class="label">{p['label']}</p>
   <h1>{p['h1']}</h1>
   <p class="split-desc">{html.escape(p['desc'])}</p>
   <p class="byline">Updated <time datetime="{UPDATED}">{UPDATED_TEXT}</time> · By the Trich Reset team · Every claim links to its source below</p>
  </div>
  {figure(IMAGES[p['slug']], eager=True)}
 </header>
 <article class="container learn-article">
  <div class="answer"><p class="label">The short answer</p><p>{summary}</p></div>
{body}
  <h2>Common questions</h2>
  <div class="faq">{faq_html}</div>

  <h2 id="sources">Sources</h2>
  <ol class="sources">{src_html}</ol>

  <p class="disclaimer">This page is general information, not medical advice. Trich Reset is a self-help tool, not a medical device,
   and doesn't replace care from a doctor, psychologist or other qualified professional.</p>
 </article>
</main>
{foot()}
<script defer src="/_vercel/insights/script.js"></script>
</body>
</html>
'''
    (ROOT / f"{p['slug']}.html").write_text(out, encoding='utf-8', newline='\n')

def render_hub():
    url = SITE + '/learn'
    cards = ''.join(f'''<li class="split hub-row"><div class="split-copy"><p class="label">{p['label'].replace('Learn · ', '')}</p>
      <h2><a href="/{p['slug']}">{p['h1']}</a></h2><p>{html.escape(p['desc'])}</p>
      <p><a class="btn btn-primary" href="/{p['slug']}">{'See the comparison' if p['slug'] == 'trichotillomania-apps' else 'Read the guide'}</a></p></div>
      {figure(IMAGES[p['slug']])}</li>''' for p in sorted(PAGES, key=lambda p: HUB_ORDER.index(p['slug'])))
    schema = schema_tags([{'@context': 'https://schema.org', '@type': 'CollectionPage', 'name': 'Learn about trichotillomania',
        'url': url, 'publisher': PUBLISHER, 'hasPart': [{'@type': 'Article', 'headline': p['h1'], 'url': f"{SITE}/{p['slug']}"} for p in PAGES]}])
    desc = 'Plain-English, research-sourced guides to trichotillomania: what it is, how to stop pulling, trich in children, help in Australia, apps compared, ADHD and trich, and treatments compared.'
    out = HEAD.format(title='Learn About Trichotillomania: Research-Sourced Guides | Trich Reset', desc=desc, url=url, schema=schema)
    out += NAV.format(play=PLAY.format(slug='learn'))
    out += f'''
<main id="main" class="learn">
 <header class="container split split-hero">
  <div class="split-copy">
   <p class="label">Learn</p>
   <h1>Trichotillomania, <span class="hl">explained properly.</span></h1>
   <p class="lede">Plain-English guides to hair pulling disorder, every fact linked to the research it came from.
   And when you've finished reading, <a href="/">an app built to help you do something about it</a>.</p>
  </div>
  {figure(HUB_IMAGE, eager=True)}
 </header>
 <div class="container">
  <ul class="hub">{cards}</ul>
{cta('learn', 'Reading is step one', 'Now hear what the app sounds like.',
     'Trich Reset has 21 guided meditations, hypnosis and sleep tracks made only for hair pulling, plus the SCAMP lessons these guides draw on. ' + FREE)}
 </div>
</main>
{foot()}
<script defer src="/_vercel/insights/script.js"></script>
</body>
</html>
'''
    (ROOT / 'learn.html').write_text(out, encoding='utf-8', newline='\n')

def render_sitemap():
    urls = ['', 'learn'] + [p['slug'] for p in PAGES] + ['privacy', 'delete-account']
    body = ''.join(f'  <url><loc>{SITE}/{u}</loc><lastmod>{UPDATED}</lastmod></url>\n' for u in urls)
    (ROOT / 'sitemap.xml').write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + body + '</urlset>\n', encoding='utf-8', newline='\n')

def render_llms():
    lines = ['# Trich Reset', '',
             '> Trich Reset is an Android app for trichotillomania (hair pulling disorder): guided audio for the moment an urge arrives, urge and pull logging, recovery-aware streaks and lessons. Made by Lux Innovations, Australia.', '',
             '## Learn (research-sourced guides)', '']
    lines += [f"- [{p['h1']}]({SITE}/{p['slug']}): {p['desc']}" for p in PAGES]
    lines += ['', '## App', '', f'- [Home, with a free meditation]({SITE}/)',
              '- [Google Play](https://play.google.com/store/apps/details?id=trichreset.com)', '']
    (ROOT / 'llms.txt').write_text('\n'.join(lines), encoding='utf-8', newline='\n')

if __name__ == '__main__':
    for p in PAGES:
        render(p)
    render_hub(); render_sitemap(); render_llms()
    print('built', len(PAGES) + 1, 'pages, sitemap.xml, llms.txt')

"""Builds the Learn pages (static HTML) from the content below.

Run:  python tools/build_learn.py   (from the repo root)
Each page: answer-first summary, tables, numbered sources, Article + FAQ +
Breadcrumb schema. Written to be quoted by search engines and AI assistants.
Add a page = add a page(...) call; the hub, footer links and sitemap follow.
"""
import html, json, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = 'https://trichreset.com'
UPDATED = '2026-10-14'
UPDATED_TEXT = '14 October 2026'
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
 'grant2009': ('Grant JE, Odlaug BL, Kim SW. N-acetylcysteine, a glutamate modulator, in the treatment of trichotillomania: a double-blind, placebo-controlled study. <em>Archives of General Psychiatry</em>. 2009;66(7):756-763.',
               'https://jamanetwork.com/journals/jamapsychiatry/fullarticle/483113'),
 'bloch2013': ('Bloch MH, Panza KE, Grant JE, Pittenger C, Leckman JF. N-acetylcysteine in the treatment of pediatric trichotillomania: a randomized, double-blind, placebo-controlled add-on trial. <em>Journal of the American Academy of Child and Adolescent Psychiatry</em>. 2013;52(3):231-240.',
               'https://pmc.ncbi.nlm.nih.gov/articles/PMC3745012/'),
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
 'skinaware': ('SkinAware. Best apps to stop hair pulling (2026 comparison). Updated 20 August 2026. Used for third-party app prices.',
               'https://www.skinawareapp.com/blog/hair-pulling-app'),
}

ORDER = []  # the current page's source order, set in render()

def cite(*keys):
    return ''.join(f'<sup><a href="#src-{k}">[{ORDER.index(k)+1}]</a></sup>' for k in keys)

# ------------------------------------------------------------------ pages
PAGES = []

def page(slug, title, h1, label, desc, summary, body, faqs, sources):
    PAGES.append(dict(slug=slug, title=title, h1=h1, label=label, desc=desc,
                      summary=summary, body=body, faqs=faqs, sources=sources))

# 1 ------------------------------------------------------------- what is it
page('what-is-trichotillomania',
 'What Is Trichotillomania? Hair Pulling Disorder Explained, With Sources',
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
 <a href="/how-to-stop-pulling-hair">practical guide</a> walks through tools for each.</p>

<h2>Is trichotillomania dangerous?</h2>
<p>It is usually not physically dangerous, but it can cause patchy hair loss, skin irritation and a lot of shame. One rare but serious risk:
 people who swallow pulled hair can develop a hairball in the stomach or intestines (a trichobezoar), which may need surgery.{cite('tlc')}
 If you swallow hair and have stomach pain, nausea or vomiting, see a doctor.</p>
''',
 [('How common is trichotillomania?', 'A 2020 survey of more than 10,000 US adults found 1.7% currently had trichotillomania, with similar rates in men and women (Grant, Dougherty and Chamberlain, Psychiatry Research, 2020).'),
  ('Is trichotillomania a form of OCD?', 'It is grouped with obsessive-compulsive and related disorders in the DSM-5, but it is its own condition. Pulling is often driven by sensation, tension or emotion rather than obsessive thoughts, and in ICD-11 it sits among the body-focused repetitive behaviour disorders.'),
  ('Can trichotillomania go away on its own?', 'For some people it eases with time, but for many it continues into adulthood. Behaviour therapy with habit reversal training has the strongest evidence for reducing pulling.'),
  ('Will my hair grow back?', 'In most cases, yes. Hair usually regrows once pulling stops, although regrowth can take months, and repeated pulling from the same follicle over many years can sometimes damage it.')],
 ['apa2013','icd11','grant2020','tlc','flessner2008','mansueto1997','farhat2020','mcguire2014'])

# 2 ------------------------------------------------------------- treatments
page('trichotillomania-treatment',
 'Trichotillomania Treatment Compared: HRT, ComB, ACT, NAC and Medication',
 'Trichotillomania treatments compared',
 'Learn · Treatment',
 'What actually works for hair pulling? A side-by-side table of trichotillomania treatments (habit reversal training, ComB, ACT, NAC, clomipramine, SSRIs) with the research behind each.',
 lambda: f'''The treatment with the strongest evidence for trichotillomania is <strong>behaviour therapy built
 around habit reversal training (HRT)</strong>. A 2020 meta-analysis of 24 randomised trials (857 people) found a
 large benefit for HRT-based therapy.{cite('farhat2020')} Among medicines, clomipramine, N-acetylcysteine (NAC) and
 olanzapine showed benefits in trials, while SSRIs did not show a clear benefit.{cite('farhat2020')}''',
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
  <tr><th scope="row">N-acetylcysteine (NAC)</th><td>An amino acid supplement that affects glutamate</td>
      <td>In adults, 56% were much or very much improved vs 16% on placebo over 12 weeks{cite('grant2009')}. In children it did no better than placebo{cite('bloch2013')}</td><td>Over the counter. Talk to a doctor first</td></tr>
  <tr><th scope="row">Clomipramine</th><td>An older antidepressant (tricyclic)</td><td>Benefit over placebo (SMD −0.71){cite('farhat2020')}; side effects limit use</td><td>Prescription</td></tr>
  <tr><th scope="row">Olanzapine</th><td>An antipsychotic</td><td>Benefit over placebo (SMD −0.94){cite('farhat2020')}; significant side effects</td><td>Prescription, specialist use</td></tr>
  <tr><th scope="row">SSRIs (e.g. fluoxetine)</th><td>Common antidepressants</td><td>No clear benefit for pulling itself{cite('farhat2020')}; may help co-occurring anxiety or depression</td><td>Prescription</td></tr>
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
<p>An app is not a replacement for a therapist. Where it can help is the moment a therapist can't be there, when the urge arrives at
 night or on the couch. See the <a href="/trichotillomania-apps">app comparison</a>.</p>

<h2>What habit reversal training involves</h2>
<ol>
 <li><strong>Awareness training.</strong> Learning exactly when, where and how you pull, including the warning signs before your hand moves.</li>
 <li><strong>Competing response.</strong> Doing something with your hands for about a minute that makes pulling impossible: making a fist, holding an object, sitting on your hands.</li>
 <li><strong>Stimulus control.</strong> Changing the setup: gloves while reading, a hat at the desk, dimmer bathroom lights.</li>
 <li><strong>Social support.</strong> Someone who gently notices and encourages you.</li>
</ol>
<p>The <a href="/how-to-stop-pulling-hair">practical guide</a> turns these into steps you can start today.</p>
''',
 [('What is the most effective treatment for trichotillomania?', 'Behaviour therapy built around habit reversal training (HRT). A 2020 meta-analysis of 24 randomised trials found a large benefit for HRT-based therapy compared with control conditions (Farhat et al., Depression and Anxiety, 2020).'),
  ('Does NAC work for trichotillomania?', 'In a 12-week trial in adults, 56% taking N-acetylcysteine were much or very much improved, compared with 16% on placebo (Grant, Odlaug and Kim, 2009). A later trial in children found no benefit over placebo. Talk to a doctor before starting any supplement.'),
  ('Do antidepressants help hair pulling?', 'SSRIs have not shown a clear benefit for pulling itself in randomised trials, although they may help co-occurring anxiety or depression. Clomipramine, an older antidepressant, has shown some benefit.'),
  ('How do I find a trichotillomania therapist?', 'The TLC Foundation for Body-Focused Repetitive Behaviors keeps a directory of clinicians trained in BFRBs at bfrb.org. Ask any therapist whether they use habit reversal training or the ComB model.')],
 ['farhat2020','mcguire2014','azrin1973','mansueto1997','woods2006','grant2009','bloch2013'])

# 3 ------------------------------------------------------------------ apps
page('trichotillomania-apps',
 'Best Apps for Trichotillomania (2026): Trich Reset, TrichStop, SkinAware, Keen2 Compared',
 'Apps for trichotillomania, compared',
 'Learn · Apps',
 'An honest side-by-side of hair pulling apps in 2026: price, platforms, therapist access, guided audio and tracking for Trich Reset, TrichStop, SkinAware and HabitAware Keen2.',
 lambda: f'''There are four main types of trichotillomania app: <strong>therapist platforms</strong> (TrichStop),
 <strong>wearables</strong> that buzz when your hand moves (HabitAware Keen2), <strong>trackers with a habit
 reversal course</strong> (SkinAware), and <strong>audio-first apps for the urge itself</strong> (Trich Reset). They
 suit different people. This page is written by the team behind Trich Reset, so we have stuck to facts you can check
 and linked our source for other apps' prices.{cite('skinaware')}''',
 lambda: f'''
<h2>Side by side</h2>
<div class="table-wrap">
<table>
 <caption>Hair pulling apps compared (October 2026)</caption>
 <thead><tr><th scope="col"></th><th scope="col">Trich Reset</th><th scope="col">TrichStop</th><th scope="col">SkinAware</th><th scope="col">HabitAware Keen2</th></tr></thead>
 <tbody>
  <tr><th scope="row">Main idea</th><td>Guided audio for the moment of the urge, plus tracking and lessons</td><td>Online program with a specialist therapist</td><td>Logging plus a habit reversal course</td><td>Bracelet that vibrates when your hand moves to your hair</td></tr>
  <tr><th scope="row">Platforms</th><td>Android (iOS coming)</td><td>iOS, Android</td><td>iOS, Android, Apple Watch, web</td><td>Bracelet + iOS/Android app</td></tr>
  <tr><th scope="row">Price</th><td>A$199.99/year (early bird), A$249.99/year or A$26.99/month</td><td>US$60–90 per week{cite('skinaware')}</td><td>Free core; premium US$5.99/month or US$34.99/year{cite('skinaware')}</td><td>US$169 bracelet; HRT content extra{cite('skinaware')}</td></tr>
  <tr><th scope="row">Free option</th><td>One full meditation free on <a href="/#listen">trichreset.com</a></td><td>No free tier{cite('skinaware')}</td><td>Yes, core logging</td><td>App logging free</td></tr>
  <tr><th scope="row">Real therapist</th><td>No</td><td>Yes</td><td>No</td><td>No</td></tr>
  <tr><th scope="row">Guided audio / meditation</th><td>Yes. A growing library built for pulling urges, with new tracks monthly</td><td>Mindfulness exercises{cite('skinaware')}</td><td>Breathing and urge-surfing tools{cite('skinaware')}</td><td>Not a focus</td></tr>
  <tr><th scope="row">Detects pulling automatically</th><td>No</td><td>No</td><td>No</td><td>Yes</td></tr>
  <tr><th scope="row">Tracking</th><td>Urge and pull logs, check-ins, recovery-aware streaks, private regrowth photos</td><td>Self-monitoring</td><td>Detailed logging, widgets</td><td>Automatic + manual</td></tr>
  <tr><th scope="row">Education</th><td>3 modules, 17 lessons, SCAMP profile questionnaire</td><td>Structured program</td><td>3-module HRT course</td><td>Course sold separately</td></tr>
 </tbody>
</table>
</div>
<p class="table-note">Third-party prices are from SkinAware's published comparison (updated 20 August 2026){cite('skinaware')} and may have changed. Check each store before you buy.</p>

<h2>Which one fits you</h2>
<div class="table-wrap">
<table>
 <caption>Match the app to the problem</caption>
 <thead><tr><th scope="col">If this sounds like you</th><th scope="col">Look at</th></tr></thead>
 <tbody>
  <tr><td>You want a real specialist and can afford weekly therapy</td><td>TrichStop, or a local BFRB therapist</td></tr>
  <tr><td>You mostly pull without noticing (automatic pulling)</td><td>A wearable such as Keen2</td></tr>
  <tr><td>You want detailed logs on a small budget, or you're on iPhone</td><td>SkinAware</td></tr>
  <tr><td>You know when the urge hits, and need something to do in that moment</td><td>Trich Reset</td></tr>
 </tbody>
</table>
</div>

<h2>What makes a good trich app</h2>
<ul>
 <li><strong>Built on habit reversal training.</strong> It is the best-evidenced approach. See <a href="/trichotillomania-treatment">treatments compared</a>.</li>
 <li><strong>Fast to use.</strong> If logging takes a minute, you will stop by week two.</li>
 <li><strong>Doesn't punish a bad day.</strong> Shame keeps the cycle going. Streaks that reset to zero can make things worse.</li>
 <li><strong>Private.</strong> You should be able to delete everything yourself.</li>
 <li><strong>Honest about what it is.</strong> No app is a medical treatment. Be wary of "cure" claims.</li>
</ul>

<div class="cta-card dark-zone">
 <p class="label">Try before you pay</p>
 <h2>Hear the Trich Reset urge track, free.</h2>
 <p><em>Right now</em> is a four-minute guided reset for the moment your hand starts moving. No signup.</p>
 <p class="cta-row"><a class="btn btn-accent" href="/#listen">Play it free</a> <a class="btn btn-ghost" href="{PLAY.format(slug='trichotillomania-apps')}">Get it on Google Play</a></p>
</div>
''',
 [('What is the best app for trichotillomania?', 'It depends on how you pull. TrichStop connects you with a specialist therapist (about US$60–90 a week). HabitAware Keen2 is a bracelet that detects automatic pulling. SkinAware offers detailed logging and a habit reversal course with a free tier. Trich Reset (Android) focuses on guided audio for the moment an urge arrives, plus tracking and lessons.'),
  ('Is there a free app for hair pulling?', 'SkinAware has a free core logging tier, and the HabitAware app is free for manual logging. Trich Reset offers one full meditation free on its website. Fully featured apps generally need a subscription.'),
  ('Do trichotillomania apps work?', 'Most apps use principles from habit reversal training, which has strong evidence as a therapy. Few apps have been tested in their own clinical trials, so treat any app as support rather than treatment.'),
  ('Is Trich Reset on iPhone?', 'Not yet. Trich Reset is on Android through Google Play, with iOS planned.')],
 ['skinaware'])

# 4 ---------------------------------------------------------------- how-to
page('how-to-stop-pulling-hair',
 'How to Stop Pulling Your Hair: A Practical, Research-Based Guide',
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
<p>Guided audio can carry you through this when you can't think straight. That is what Trich Reset's
 <a href="/#listen">free urge track</a> is for.</p>

<h2>5. Expect slips, and count the hard days</h2>
<p>Recovery is rarely a straight line. Shame after a slip often leads to more pulling. Track the days you showed up, not only the clean ones,
 so you can see the trend over weeks rather than judging yourself on one night.</p>

<h2>When to get professional help</h2>
<p>If pulling is causing noticeable hair loss, affecting your work, school or relationships, or you feel low or hopeless, see a doctor or
 psychologist. A therapist trained in habit reversal training or the ComB model gives you the best-evidenced help. The TLC Foundation
 lists BFRB clinicians at <a href="https://www.bfrb.org">bfrb.org</a>. If you are in crisis in Australia, call Lifeline on 13 11 14.</p>

<div class="cta-card dark-zone">
 <p class="label">For the ten seconds your hand starts moving</p>
 <h2>Press play when the urge hits.</h2>
 <p>Hear Trich Reset's four-minute urge reset free on our homepage. No signup, no email.</p>
 <p class="cta-row"><a class="btn btn-accent" href="/#listen">Play it free</a> <a class="btn btn-ghost" href="{PLAY.format(slug='how-to-stop-pulling-hair')}">Get it on Google Play</a></p>
</div>
''',
 [('How do I stop pulling my hair right now?', 'Give your hands a competing job for about a minute: clench your fists, hold an object or sit on your hands. Then name the urge, breathe slowly and wait for it to peak and pass.'),
  ('What can I do instead of pulling my hair?', 'Use a competing response that keeps your hands busy (a fidget, a smooth stone, a hairbrush), wear gloves or a hat during high-risk activities, and change the places where you pull, such as covering or dimming the mirror.'),
  ("Why can't I stop pulling my hair?", 'Trichotillomania is a body-focused repetitive behaviour, not a lack of willpower. Pulling is triggered and reinforced by sensations, thoughts, emotions, habits and places. Tools that target your specific triggers work better than trying to just stop.'),
  ('Does wearing gloves help with hair pulling?', 'Gloves, finger tape or a hat are a form of stimulus control used in habit reversal training. They are most useful during predictable high-risk times, like reading, watching TV or lying in bed.')],
 ['farhat2020','woods2006','mansueto1997','azrin1973'])

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
    <p><a href="/">Trich Reset</a> · <a href="/privacy">Privacy</a> · <a href="mailto:info@luxinnovations.com.au">info@luxinnovations.com.au</a></p>
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
# 'art' = square meditation cover (assets/img/learn), 'phone' = real app screen.
IMAGES = {
    'what-is-trichotillomania': ('assets/img/learn/befriending_the_pull', 'Calm illustrated figure from the Trich Reset meditation Befriending the Pull', 'art'),
    'trichotillomania-treatment': ('assets/img/learn/the_trigger_window', 'Illustrated path of light from the Trich Reset meditation The Trigger Window', 'art'),
    'trichotillomania-apps': ('assets/img/app/screen-4', 'Trich Reset app screen: the Listen tab with urge resets, sleep and grounding tracks', 'phone'),
    'how-to-stop-pulling-hair': ('assets/img/learn/calm_hands_hypnosis', 'Glowing open hands from the Trich Reset meditation Calm Hands Hypnosis', 'art'),
}
HUB_IMAGE = ('assets/img/learn/calm_hands_kind_mind', 'Two glowing faces from the Trich Reset meditation Calm Hands, Kind Mind', 'art')

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
      <p><a class="btn btn-primary" href="/{p['slug']}">Read the guide</a></p></div>
      {figure(IMAGES[p['slug']])}</li>''' for p in PAGES)
    schema = schema_tags([{'@context': 'https://schema.org', '@type': 'CollectionPage', 'name': 'Learn about trichotillomania',
        'url': url, 'publisher': PUBLISHER, 'hasPart': [{'@type': 'Article', 'headline': p['h1'], 'url': f"{SITE}/{p['slug']}"} for p in PAGES]}])
    desc = 'Plain-English, research-sourced guides to trichotillomania: what it is, treatments compared, apps compared, and practical steps to stop pulling.'
    out = HEAD.format(title='Learn About Trichotillomania: Research-Sourced Guides | Trich Reset', desc=desc, url=url, schema=schema)
    out += NAV.format(play=PLAY.format(slug='learn'))
    out += f'''
<main id="main" class="learn">
 <header class="container split split-hero">
  <div class="split-copy">
   <p class="label">Learn</p>
   <h1>Trichotillomania, <span class="hl">explained properly.</span></h1>
   <p class="lede">Plain-English guides to hair pulling disorder. Every fact links to the research it came from, so you can check it yourself.</p>
  </div>
  {figure(HUB_IMAGE, eager=True)}
 </header>
 <div class="container">
  <ul class="hub">{cards}</ul>
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

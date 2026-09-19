import json, pathlib
ROOT=pathlib.Path('/Users/carolineli/Developer/MCU'); SITE='https://mcu-breakdown.vercel.app/'
BEACON=('<script type="module" src="https://static.cloudflareinsights.com/beacon.min.js" '
        'data-cf-beacon=\'{"token": "45f9aa7f5121417096f6c77fa40ea24c"}\'></script>')
FONTS='<link href="https://fonts.googleapis.com/css2?family=Bangers&family=Archivo+Black&family=Barlow+Condensed:wght@700&family=Barlow:ital,wght@0,400;0,600;1,400&display=swap" rel="stylesheet">'
OTHERS={'what-to-watch-before-doomsday.html':'What to watch before Avengers: Doomsday',
        'x-men-in-the-mcu.html':'Where the X-Men fit into the MCU',
        'marvel-shows-that-matter.html':'Which Marvel shows actually matter'}

def page(slug, title, desc, h1, lede, body, faq):
    ld=[{"@context":"https://schema.org","@type":"Article","headline":h1,"description":desc,
         "inLanguage":"en","mainEntityOfPage":SITE+slug,
         "isPartOf":{"@type":"WebSite","name":"The MCU, In Order","url":SITE}}]
    if faq:
        ld.append({"@context":"https://schema.org","@type":"FAQPage","mainEntity":[
            {"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in faq]})
    more="".join(f'\n        <a href="{u}">{t} &rarr;</a>' for u,t in OTHERS.items() if u!=slug)
    html=f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="color-scheme" content="light">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{SITE}{slug}">
<meta property="og:type" content="article">
<meta property="og:site_name" content="The MCU, In Order">
<meta property="og:url" content="{SITE}{slug}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="{SITE}og.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{SITE}og.png">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' rx='10' fill='%2314100D'/%3E%3Ctext x='32' y='45' font-family='Georgia,serif' font-size='40' font-weight='bold' text-anchor='middle' fill='%23D92B1C'%3EM%3C/text%3E%3C/svg%3E">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
{FONTS}
<link rel="stylesheet" href="guide.css">
<script type="application/ld+json">
{json.dumps(ld[0] if len(ld)==1 else ld, ensure_ascii=False, indent=1)}
</script>
</head>
<body>
  <main class="wrap">
    <div class="top"><a class="home" href="./">&larr; The MCU, in order</a></div>
    <h1>{h1}</h1>
    <p class="lede">{lede}</p>
{body}
    <a class="cta" href="./"><b>See the full watch order</b><span>Every film and series, in release or story order, with the ones you can skip marked &mdash; and it remembers what you have watched.</span></a>
    <h2>More guides</h2>
    <div class="more">{more}
    </div>
    <footer class="legal">
      <p>Unofficial fan guide. Marvel, MCU and all related characters and titles are the property of Marvel Characters, Inc. and The Walt Disney Company. Not affiliated with, endorsed by or connected to Marvel Studios or Disney. Runtimes and dates are approximate; later in-universe placements are the fan community&rsquo;s best reconstruction and may be wrong.</p>
    </footer>
  </main>
{BEACON}
</body>
</html>
'''
    (ROOT/slug).write_text(html, encoding='utf-8'); return slug

def table(caption, head, rows):
    rt=[i for i,c in enumerate(head) if c=="Runtime"]      # only this column refuses to wrap
    cls=lambda i: ' class="rt"' if i in rt else ''
    h="".join(f"<th{cls(i)}>{c}</th>" for i,c in enumerate(head))
    body="".join("<tr>"+"".join(f"<td{cls(i)}>{c}</td>" for i,c in enumerate(r))+"</tr>" for r in rows)
    return (f'    <table><caption>{caption}</caption><thead><tr>{h}</tr></thead>\n'
            f'      <tbody>{body}</tbody></table>\n')

# ---------------- 1. Doomsday ----------------
body1 = """    <p>Avengers: Doomsday lands on 18 December 2026, and it is the first film in years that genuinely
    asks you to have done some homework. Not eighteen years of it, though. Four titles carry almost
    everything you need, and they come to about eleven hours.</p>

    <h2>The four that matter</h2>
""" + table("Watch these", ["Title","Why","Runtime"], [
    ("The Fantastic Four: First Steps","Earth-828 and the family Doomsday is built around. Its post-credits scene is the direct on-ramp.","1h 55m"),
    ("Thunderbolts*","Where the new team assembles, and where Doomsday finds most of its roster.","2h 07m"),
    ("Deadpool &amp; Wolverine","The TVA pulls Fox&rsquo;s X-Men universe into the MCU. Doomsday is where that bill comes due.","2h 08m"),
    ("Loki &mdash; Season 2","The multiverse rules the whole film runs on. Dry in places, essential in others.","5h 00m"),
]) + """    <p class="tot">Total: about 11 hours.</p>

    <h2>If you have more time</h2>
    <p>These are not required, but they are the difference between following Doomsday and feeling it.</p>
""" + table("Worth adding", ["Title","Why","Runtime"], [
    ("Avengers: Infinity War","The last time everyone shared a screen. Doomsday is measured against it whether it likes it or not.","2h 29m"),
    ("Avengers: Endgame","Closes the Infinity Saga and explains who is missing and why.","3h 01m"),
    ("Loki &mdash; Season 1","Where the Sacred Timeline breaks and the multiverse starts.","4h 50m"),
    ("Spider-Man: No Way Home","The first crossing between universes, and the easiest to enjoy cold.","2h 28m"),
    ("Doctor Strange in the Multiverse of Madness","Earth-838, the Illuminati, and Patrick Stewart&rsquo;s Professor X.","2h 06m"),
]) + """    <h2>What about the X-Men films?</h2>
    <p>Doomsday brings back the original Fox cast &mdash; Patrick Stewart, Ian McKellen, James Marsden,
    Rebecca Romijn and Alan Cumming. You do not need thirteen X-Men films to follow that. Watching
    <strong>X-Men</strong> (2000) and <strong>X2</strong> will tell you who these people are to each other,
    which is all Doomsday is likely to lean on. There is a fuller answer in
    <a href="x-men-in-the-mcu.html">where the X-Men fit into the MCU</a>.</p>

    <h2>What you can skip</h2>
    <p>Secret Invasion, Ironheart, Echo, She-Hulk, Moon Knight and Wonder Man are all good or bad on
    their own terms, and none of them set up Doomsday. If you are working to a December deadline,
    leave them.</p>
"""
p1=page('what-to-watch-before-doomsday.html',
  'What to Watch Before Avengers: Doomsday (2026) — The Short List',
  'The four titles that actually set up Avengers: Doomsday, about eleven hours in total, plus what to add if you have more time and what you can safely skip.',
  'What to watch before Doomsday',
  'Four titles, about eleven hours. Everything else is optional.', body1,
  [("What do I need to watch before Avengers: Doomsday?",
    "Four titles carry almost everything: The Fantastic Four: First Steps, Thunderbolts*, Deadpool & Wolverine and Loki season 2. That is roughly eleven hours. Infinity War and Endgame help if you have never seen them."),
   ("Do I need to watch the X-Men films before Doomsday?",
    "No. Doomsday brings back the original Fox cast, but X-Men (2000) and X2 are enough to know who they are to each other. The other eleven films are optional.")])

# ---------------- 2. X-Men ----------------
body2 = """    <p>For twenty-four years the X-Men were not in the MCU at all. They were Fox&rsquo;s, in their own
    universe, with their own continuity and their own Wolverine. Disney buying Fox in 2019 changed who
    owned them; it did not put them on screen together. That took another five years, and it happened
    in a Deadpool film.</p>

    <h2>The short answer</h2>
    <p>Fox&rsquo;s X-Men films are <strong>Earth-10005</strong>, a separate universe. In
    <strong>Deadpool &amp; Wolverine</strong> (2024) the TVA reaches into it and pulls Deadpool and a
    Wolverine out, which is the moment the two franchises formally touch. In
    <strong>Avengers: Doomsday</strong> (December 2026) the original cast returns properly.</p>

    <h2>Every time the MCU has nodded at mutants</h2>
""" + table("The trail", ["When","What happened"], [
    ("Ms. Marvel <em>(2022)</em>","Kamala is told her powers come from a mutation, over a bar of the X-Men &rsquo;97 theme. The first time the word is used on screen."),
    ("Black Panther: Wakanda Forever <em>(2022)</em>","Namor calls himself a mutant, casually, as if it were settled."),
    ("Doctor Strange in the Multiverse of Madness <em>(2022)</em>","Patrick Stewart&rsquo;s Professor X appears &mdash; but on Earth-838, as a variant, not the one from the Fox films."),
    ("The Marvels <em>(2023)</em>","Monica wakes in a world with Kelsey Grammer&rsquo;s Beast. A different universe again, and the clearest signal yet."),
    ("Deadpool &amp; Wolverine <em>(2024)</em>","The TVA, the Void, and Fox&rsquo;s universe folded into canon. Cameos from across the Fox era."),
    ("Avengers: Doomsday <em>(2026)</em>","Stewart, McKellen, Marsden, Romijn and Cumming all return, alongside the Avengers and the Fantastic Four."),
]) + """    <h2>Which Fox films are worth watching</h2>
    <p>Thirteen films, and most of them you can skip. These six carry the parts that matter now.</p>
""" + table("The ones to watch", ["Film","Why","Runtime"], [
    ("X-Men <em>(2000)</em>","Introduces Xavier, Magneto, Cyclops and Mystique &mdash; the cast Doomsday is bringing back.","1h 44m"),
    ("X2 <em>(2003)</em>","Still the best of them, and where Nightcrawler arrives.","2h 14m"),
    ("X-Men: Days of Future Past <em>(2014)</em>","Both casts in one film. If you watch only one, make it this.","2h 12m"),
    ("Deadpool <em>(2016)</em>","Wade&rsquo;s origin. Deadpool &amp; Wolverine assumes you know him.","1h 48m"),
    ("Deadpool 2 <em>(2018)</em>","Cable, Domino, and the life Deadpool &amp; Wolverine picks up from.","1h 59m"),
    ("Logan <em>(2017)</em>","Wolverine&rsquo;s ending, and the film Deadpool &amp; Wolverine spends its runtime answering.","2h 17m"),
]) + """    <h2>A detail most guides get wrong</h2>
    <p>The Professor X in Multiverse of Madness is not the Fox one. He is an Earth-838 variant who
    happens to share an actor &mdash; one of several universes the MCU has visited, and separate from
    Earth-10005, where Deadpool and Logan come from. The films are deliberately vague about it. The
    <a href="./">multiverse map</a> on the main guide lays the universes out side by side.</p>
"""
p2=page('x-men-in-the-mcu.html',
  'Where Do the X-Men Fit Into the MCU? — Every Crossover, Explained',
  'Fox’s X-Men were a separate universe until Deadpool & Wolverine. Every mutant nod the MCU has made, which Fox films are worth watching, and what Doomsday brings back.',
  'Where the X-Men fit into the MCU',
  'A separate universe for twenty-four years, folded in by a Deadpool film, and back properly in Doomsday.', body2,
  [("Are the X-Men part of the MCU?",
    "They are now. Fox's X-Men films were their own universe, Earth-10005, until Deadpool & Wolverine (2024), where the TVA pulls Deadpool and Wolverine into the MCU. The original cast returns in Avengers: Doomsday in December 2026."),
   ("Which X-Men films should I watch?",
    "Six of the thirteen carry what matters now: X-Men (2000), X2, Days of Future Past, Deadpool, Deadpool 2 and Logan.")])

# ---------------- 3. Disney+ shows ----------------
body3 = """    <p>There are more than twenty Marvel series now, and the honest position is that most of them do
    not matter to the films. A handful genuinely do. Here is the split, and why.</p>

    <h2>The ones that feed the films</h2>
""" + table("Watch these", ["Series","Why it matters","Runtime"], [
    ("WandaVision","Wanda&rsquo;s grief and her power, without which Multiverse of Madness makes no sense.","5h 50m"),
    ("Loki &mdash; Season 1","Breaks the Sacred Timeline. Everything multiverse-shaped starts here.","4h 50m"),
    ("Loki &mdash; Season 2","The rules the whole current era runs on, and required before Doomsday.","5h 00m"),
    ("The Falcon and the Winter Soldier","How Sam becomes Captain America, and sets up Brave New World.","5h 30m"),
    ("Daredevil: Born Again","Fisk in office, and the thread running into Spider-Man: Brand New Day.","8h 00m"),
]) + """    <h2>Good, but optional</h2>
""" + table("Only if you want to", ["Series","Verdict","Runtime"], [
    ("Hawkeye","Introduces Kate Bishop and Echo. Cheerful, light stakes.","4h 30m"),
    ("Ms. Marvel","Kamala&rsquo;s origin before The Marvels, and the first &ldquo;mutant&rdquo; on screen.","4h 40m"),
    ("Moon Knight","Almost entirely self-contained, and better for it.","4h 40m"),
    ("Agatha All Along","A WandaVision spin-off that pays off if you liked her, and nothing if you did not.","5h 30m"),
    ("Echo","A tighter, grimmer story that ties into Daredevil.","3h 40m"),
]) + """    <h2>Skippable</h2>
    <p><strong>Secret Invasion</strong> has one consequence that carries into The Marvels and is
    otherwise a chore. <strong>She-Hulk</strong>, <strong>Ironheart</strong> and
    <strong>Wonder Man</strong> are worth watching if the premise appeals and are safe to miss
    entirely. No film so far asks you to have seen any of them.</p>

    <h2>The short version</h2>
    <p>If you want the smallest set that keeps the films coherent: WandaVision, both seasons of Loki,
    and The Falcon and the Winter Soldier &mdash; about twenty-one hours. Add Daredevil: Born Again if
    you are heading for Brand New Day. The
    <a href="./">full guide</a> marks every title as essential, recommended or optional, so you can
    filter the whole thing down to the path you want.</p>
"""
p3=page('marvel-shows-that-matter.html',
  'Which Marvel Disney+ Shows Actually Matter? — Required vs Skippable',
  'More than twenty Marvel series, and most of them do not affect the films. Which Disney+ shows are required, which are optional, and which you can skip entirely.',
  'Which Marvel shows actually matter',
  'Twenty-odd series. Five that the films depend on. The rest is up to you.', body3,
  [("Do I need to watch the Marvel Disney+ shows?",
    "Most of them, no. WandaVision, both seasons of Loki, The Falcon and the Winter Soldier and Daredevil: Born Again feed directly into the films. The rest are optional."),
   ("Which Marvel shows can I skip?",
    "Secret Invasion, She-Hulk, Ironheart and Wonder Man have no bearing on any film so far. Hawkeye, Ms. Marvel, Moon Knight, Echo and Agatha All Along are good but optional.")])
print('built:', p1, p2, p3)

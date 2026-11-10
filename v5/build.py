#!/usr/bin/env python3
"""Builds the static v5 pages (NL + EN) from one template.

Edit copy in COPY / SU below, then run:  python3 v5/build.py
Outputs:
  v5/index.html            (nl-NL landing, SugarDates.nl)
  v5/aanmelden/index.html  (nl-NL signup)
  v5/en/index.html         (en-US landing, SugarDates.net)
  v5/en/signup/index.html  (en-US signup)
Shared: v5/assets/site.css, v5/assets/signup.js, v5/assets/logo.svg, v5/img/*
"""
import json, os, html

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = "https://realmrhodl.github.io/sugardates-nl/v5/"
MIN_AGE = 18
CHECK = '<span class="ck" aria-hidden="true"><svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"><path d="M6 12.5l4 4 8-9"/></svg></span>'

COPY = {
"nl": {
  "lang":"nl", "locale":"nl_NL", "hreflang":"nl-NL", "path":"", "signup":"aanmelden/",
  "title":"SugarDates – sugardating in Nederland",
  "desc":"Sugardating in Nederland. Maak een profiel, zeg eerlijk wat je zoekt en spreek af op jullie voorwaarden. Meld je gratis aan.",
  "skip":"Naar de inhoud", "cta_top":"Aanmelden",
  "hero_h1":"Sugardating in Nederland",
  "hero_sub":"Voor sugardaddy's, sugarmama's en sugarbaby's die eerlijk willen zijn over wat ze zoeken. Maak een profiel, leer elkaar kennen en maak duidelijke afspraken.",
  "role_baby":"Ik ben sugarbaby", "role_daddy":"Ik ben sugardaddy / sugarmama",
  "hero_note":"Aanmelden is gratis. SugarDates is nog niet live; je komt op de wachtlijst. Alleen 18+.",
  "p_kicker":"In het kort",
  "promise":[("Profiel maken","Vertel wie je bent en wat je zoekt. Je mag een bijnaam gebruiken."),
             ("Praten","Bespreek wat jullie van elkaar verwachten, voordat je afspreekt."),
             ("Afspreken","Spreek af als het voor allebei goed voelt.")],
  "how_kicker":"Hoe het werkt", "how_h2":"In drie stappen begonnen",
  "how_lead":"Aanmelden duurt een paar minuten. De rest vul je aan wanneer het jou uitkomt.",
  "how":[("Meld je aan","Kies je rol, een gebruikersnaam en je regio. Daarna je e-mailadres en een wachtwoord."),
         ("Maak je profiel af","Schrijf een korte tekst en geef aan wat je zoekt."),
         ("Stuur berichten","Bekijk profielen in je regio en stuur berichten.")],
  "trust_kicker":"Veiligheid en privacy", "trust_h2":"Waarom SugarDates",
  "trust_lead":"",
  "trust":[("Bijnaam mag","Je hoeft je echte naam niet te gebruiken."),
           ("Jij kiest wat je deelt","Je woonplaats is een stad of provincie, nooit een adres."),
           ("E-mailadres blijft privé","Andere leden zien je e-mailadres niet.")],
  "web_kicker":"Op elk apparaat", "web_h2":"Geen app nodig",
  "web_lead":"SugarDates werkt in de browser op je telefoon, tablet en computer. Je hoeft niets te installeren.",
  "web_list":["iPhone, Android en desktop","Geen app-icoon op je telefoon","Inloggen met e-mail en wachtwoord"],
  "web_alt":"Sfeerbeeld: iemand met een telefoon in een café, geen echte leden",
  "types_kicker":"Voor wie", "types_h2":"Sugardaddy's, sugarmama's en sugarbaby's",
  "type_daddy_k":"Sugardaddy / sugarmama", "type_daddy_h":"Wat is een sugardaddy of sugarmama?",
  "type_daddy_p":"Iemand die succesvol is en graag tijd doorbrengt met een leuk en energiek gezelschap. Je bent open over wat je zoekt en wat je kunt bieden.",
  "type_daddy_list":["Gezelschap voor diners, uitjes en reizen","Iemand steunen of begeleiden","Duidelijke afspraken vooraf"],
  "type_daddy_cta":"Aanmelden als sugardaddy / sugarmama", "type_daddy_alt":"Sfeerbeeld: man in een lunchroom, geen echte leden",
  "type_baby_k":"Sugarbaby", "type_baby_h":"Wat is een sugarbaby?",
  "type_baby_p":"Iemand die zelfstandig is en weet wat hij of zij wil. Bijvoorbeeld een student, starter of ondernemer. Jij bepaalt je grenzen.",
  "type_baby_list":["Een ervaren gesprekspartner of mentor","Nieuwe plekken en ervaringen","Steun die past bij jullie afspraken"],
  "type_baby_cta":"Aanmelden als sugarbaby", "type_baby_alt":"Sfeerbeeld: vrouw loopt langs een gracht, geen echte leden",
  "cr_kicker":"Kosten", "cr_h2":"Hoe betalen werkt",
  "cr_lead":"SugarDates werkt met credits. Je betaalt alleen voor wat je gebruikt, zonder abonnement.",
  "credits":[("Gratis aanmelden","Een account en profiel aanmaken is gratis."),
             ("Credits voor contact","Voor sommige functies, zoals berichten sturen, gebruik je credits."),
             ("Prijzen vooraf bekend","Je ziet altijd eerst wat iets kost.")],
  "faq_kicker":"Vragen", "faq_h2":"Veelgestelde vragen",
  "faq":[("Wat is sugardating?","Daten waarbij je vooraf eerlijk bespreekt wat je van elkaar verwacht, zoals gezelschap, begeleiding of steun. Wat jullie afspreken, bepalen jullie samen."),
         ("Moet ik mijn echte naam gebruiken?","Nee. Je kiest zelf een gebruikersnaam. Je e-mailadres is niet zichtbaar voor andere leden."),
         ("Wat kost het?","Een account aanmaken is gratis. Voor sommige functies gebruik je credits."),
         ("Wat gebeurt er met mijn gegevens?","We maken je gegevens niet openbaar. Je kunt je aanmelding altijd laten verwijderen. Zie ons privacybeleid."),
         ("Is dit een escortsite?","Nee. SugarDates is een datingsite. Seks aanbieden of vragen tegen betaling is niet toegestaan.")],
  "close_h2":"Meld je aan voor SugarDates",
  "close_lead":"Aanmelden duurt een paar minuten.",
  "hero_alt":"Sfeerbeeld: man en vrouw op een terras aan de gracht, geen echte leden",
  "f_about":"Sugardating voor Nederland en Europa. Een site van Forest Road B.V., het bedrijf achter Paydates.nl.",
  "f_site":"SugarDates", "f_links":[("Hoe het werkt","#hoe"),("Veelgestelde vragen","#faq"),("Privacy","#"),("Voorwaarden","#"),("Contact","#")],
  "f_region":"Land", "region_here":"SugarDates.nl · Nederland/EU", "region_other":"SugarDates.net · USA", "region_soon":"binnenkort",
  "f_legal":"Forest Road B.V. · Herengracht 449A, 1017 BR Amsterdam · KvK 97957232 · BTW NL868303550B01 · © 2026",
  "su_title":"Aanmelden – SugarDates",
  "su_alt":"Sfeerbeeld: man en vrouw op een terras, geen echte leden",
},
"en": {
  "lang":"en", "locale":"en_US", "hreflang":"en-US", "path":"en/", "signup":"signup/",
  "title":"SugarDates – sugar dating",
  "desc":"Sugar dating made simple. Create a profile, be upfront about what you want and meet on your own terms. Sign up for free.",
  "skip":"Skip to content", "cta_top":"Join",
  "hero_h1":"Sugar dating, made simple",
  "hero_sub":"For sugar daddies, sugar mommies and sugar babies who want to be upfront about what they're looking for. Create a profile, get to know each other and agree on what works.",
  "role_baby":"I'm a sugar baby", "role_daddy":"I'm a sugar daddy / mommy",
  "hero_note":"Joining is free. SugarDates isn't live yet, so you'll join the waitlist. 18+ only.",
  "p_kicker":"In short",
  "promise":[("Create a profile","Say who you are and what you're looking for. A nickname is fine."),
             ("Talk","Discuss what you expect from each other before you meet."),
             ("Meet","Meet up when it feels right for both of you.")],
  "how_kicker":"How it works", "how_h2":"Get started in three steps",
  "how_lead":"Signing up takes a few minutes. Fill in the rest whenever you like.",
  "how":[("Sign up","Choose your role, a username and your state. Then your email and a password."),
         ("Finish your profile","Write a short intro and say what you're looking for."),
         ("Send messages","Browse profiles near you and send messages.")],
  "trust_kicker":"Safety and privacy", "trust_h2":"Why SugarDates",
  "trust_lead":"",
  "trust":[("Nicknames welcome","You don't have to use your real name."),
           ("You choose what to share","Your location is a city or state, never an address."),
           ("Your email stays private","Other members can't see your email address.")],
  "web_kicker":"On any device", "web_h2":"No app needed",
  "web_lead":"SugarDates works in the browser on your phone, tablet and computer. Nothing to install.",
  "web_list":["iPhone, Android and desktop","No app icon on your phone","Sign in with email and password"],
  "web_alt":"Mood image: someone using a phone in a café, not real members",
  "types_kicker":"Who it's for", "types_h2":"Sugar daddies, sugar mommies and sugar babies",
  "type_daddy_k":"Sugar daddy / mommy", "type_daddy_h":"What is a sugar daddy or sugar mommy?",
  "type_daddy_p":"Someone successful who enjoys spending time with fun, energetic company. You're open about what you're looking for and what you can offer.",
  "type_daddy_list":["Company for dinners, events and travel","Supporting or mentoring someone","Clear agreements up front"],
  "type_daddy_cta":"Join as a sugar daddy / mommy", "type_daddy_alt":"Mood image: man in a restaurant, not real members",
  "type_baby_k":"Sugar baby", "type_baby_h":"What is a sugar baby?",
  "type_baby_p":"Someone independent who knows what they want. For example a student, young professional or entrepreneur. You set your boundaries.",
  "type_baby_list":["An experienced mentor to talk to","New places and experiences","Support that fits what you agree on"],
  "type_baby_cta":"Join as a sugar baby", "type_baby_alt":"Mood image: woman walking along a canal, not real members",
  "cr_kicker":"Pricing", "cr_h2":"How payment works",
  "cr_lead":"SugarDates uses credits. You only pay for what you use, with no subscription.",
  "credits":[("Free to join","Creating an account and profile is free."),
             ("Credits for contact","Some features, like sending messages, use credits."),
             ("Prices shown up front","You'll always see the cost first.")],
  "faq_kicker":"Questions", "faq_h2":"Frequently asked questions",
  "faq":[("What is sugar dating?","Dating where you're upfront about what you expect from each other, such as companionship, mentoring or support. What you agree on is up to the two of you."),
         ("Do I have to use my real name?","No. You choose a username. Your email isn't shown to other members."),
         ("What does it cost?","Creating an account is free. Some features use credits."),
         ("What happens to my data?","We don't make your data public. You can ask us to delete your signup at any time. See our privacy policy."),
         ("Is this an escort site?","No. SugarDates is a dating site. Offering or asking for sex for money isn't allowed.")],
  "close_h2":"Join SugarDates",
  "close_lead":"Signing up takes a few minutes.",
  "hero_alt":"Mood image: a man and woman at a canal-side café, not real members",
  "f_about":"SugarDates.net is the US site of SugarDates, on the same platform as SugarDates.nl. Operated by Forest Road B.V.",
  "f_site":"SugarDates", "f_links":[("How it works","#how"),("FAQ","#faq"),("Privacy","#"),("Terms","#"),("Contact","#")],
  "f_region":"Country", "region_here":"SugarDates.net · USA", "region_other":"SugarDates.nl · Netherlands/EU", "region_soon":"",
  "f_legal":"Forest Road B.V. · Herengracht 449A, 1017 BR Amsterdam, the Netherlands · Chamber of Commerce 97957232 · VAT NL868303550B01 · © 2026",
  "su_title":"Join – SugarDates",
  "su_alt":"Mood image: a man and woman at a café, not real members",
},
}

def e(s): return html.escape(s, quote=True)

def head(c, title, desc, canon, root, alt_nl, alt_en, robots="index,follow"):
    return f'''<!DOCTYPE html>
<html lang="{c["hreflang"]}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <title>{e(title)}</title>
  <meta name="description" content="{e(desc)}">
  <meta name="robots" content="{robots}">
  <meta name="theme-color" content="#ffffff">
  <link rel="canonical" href="{canon}">
  <link rel="alternate" hreflang="nl-NL" href="{alt_nl}">
  <link rel="alternate" hreflang="en-US" href="{alt_en}">
  <link rel="alternate" hreflang="x-default" href="{alt_nl}">
  <meta property="og:type" content="website">
  <meta property="og:locale" content="{c["locale"]}">
  <meta property="og:site_name" content="SugarDates">
  <meta property="og:title" content="{e(title)}">
  <meta property="og:description" content="{e(desc)}">
  <meta property="og:url" content="{canon}">
  <meta property="og:image" content="{BASE}img/og.jpg">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="icon" href="{root}assets/logo.svg" type="image/svg+xml">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Manrope:wght@700;800&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="{root}assets/site.css?v=7">
</head>
'''

GLOBE = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c2.6 2.6 2.6 15.4 0 18M12 3c-2.6 2.6-2.6 15.4 0 18"/></svg>'
CHEV = '<svg class="chev" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M6 9l6 6 6-6"/></svg>'
TICKSVG = '<svg class="lm-tick" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12.5l4.5 4.5L19 7.5"/></svg>'
LOCALES = [("nl","nl-NL","Nederlands","SugarDates.nl"),("en","en-US","English (US)","SugarDates.net")]

def langmenu(c, hrefs):
    """hrefs: {'nl': url, 'en': url} relative to the current page."""
    cur = c["lang"]
    label = "Taal en land" if cur=="nl" else "Language and region"
    items = ""
    for code, hl, name, dom in LOCALES:
        on = code==cur
        attrs = ' aria-current="true"' if on else f' hreflang="{hl}" lang="{code}"'
        items += f'<li><a class="lm-item{" is-on" if on else ""}" href="{hrefs[code]}"{attrs}><span><span class="lm-name">{name}</span><span class="lm-dom">{dom}</span></span>{TICKSVG if on else ""}</a></li>'
    return (f'<div class="lm" data-lm><button type="button" class="lm-btn" aria-expanded="false" aria-controls="lm-list" aria-label="{label}: {dict((l[0],l[2]) for l in LOCALES)[cur]}">'
            f'{GLOBE}<span class="lm-code">{cur.upper()}</span>{CHEV}</button>'
            f'<ul class="lm-list" id="lm-list" hidden>{items}</ul></div>')

def langline(c, hrefs):
    out=[]
    for code, hl, name, dom in LOCALES:
        if code==c["lang"]: out.append(f'<span aria-current="true">{name}</span>')
        else: out.append(f'<a href="{hrefs[code]}" hreflang="{hl}" lang="{code}">{name}</a>')
    return '<p class="foot-lang">'+" / ".join(out)+'</p>'

LM_JS = """<script>(function(){document.querySelectorAll('[data-lm]').forEach(function(m){var b=m.querySelector('.lm-btn'),l=m.querySelector('.lm-list');
function set(o,f){b.setAttribute('aria-expanded',o);l.hidden=!o;if(o&&f){var a=l.querySelector('a');a&&a.focus();}}
b.addEventListener('click',function(e){set(b.getAttribute('aria-expanded')!=='true',e.detail===0);});
b.addEventListener('keydown',function(e){if(e.key==='ArrowDown'){e.preventDefault();set(true,true);}});
l.addEventListener('keydown',function(e){var a=[].slice.call(l.querySelectorAll('a')),i=a.indexOf(document.activeElement);
if(e.key==='ArrowDown'){e.preventDefault();a[(i+1)%a.length].focus();}if(e.key==='ArrowUp'){e.preventDefault();a[(i-1+a.length)%a.length].focus();}
if(e.key==='Escape'){set(false);b.focus();}});
document.addEventListener('click',function(e){if(!m.contains(e.target))set(false);});
m.addEventListener('focusout',function(e){if(e.relatedTarget&&!m.contains(e.relatedTarget))set(false);});
document.addEventListener('keydown',function(e){if(e.key==='Escape'&&!l.hidden){set(false);b.focus();}});});})();</script>"""

def pic(root, name, alt, w=1152, h=864, lazy=True):
    ld = ' loading="lazy" decoding="async"' if lazy else ' fetchpriority="high"'
    return f'<picture><source srcset="{root}img/{name}.webp" type="image/webp"><img src="{root}img/{name}.jpg" alt="{e(alt)}" width="{w}" height="{h}"{ld}></picture>'

def brand(root, href):
    return f'<a class="brand" href="{href}" aria-label="SugarDates"><img src="{root}assets/logo.svg" alt="" width="30" height="30">SugarDates</a>'

def roles(c, su, alt=False):
    a, b = ("btn-white","btn-ghost-w") if alt else ("btn-primary","btn-outline")
    return (f'<div class="roles"><a class="btn {a}" href="{su}?rol=baby">{c["role_baby"]}</a>'
            f'<a class="btn {b}" href="{su}?rol=daddy">{c["role_daddy"]}</a></div>')

def landing(c):
    nl = c["lang"]=="nl"
    root = "" if nl else "../"
    su = c["signup"]
    canon = BASE + c["path"]
    LH = {"nl":"./","en":"en/"} if nl else {"nl":"../","en":"./"}
    hdr = f'''<header class="top"><div class="wrap top-in">
    {brand(root, "./")}
    <div class="top-right">{langmenu(c, LH)}<a class="btn btn-primary btn-sm top-cta" href="{su}">{c["cta_top"]}</a></div>
  </div></header>'''
    promise = "".join(f'<li><span class="num">{i+1}</span><div><h3>{t}</h3><p>{p}</p></div></li>' for i,(t,p) in enumerate(c["promise"]))
    how = "".join(f'<li><h3>{t}</h3><p>{p}</p></li>' for t,p in c["how"])
    trust = "".join(f'<div>{CHECK}<div><h3>{t}</h3><p>{p}</p></div></div>' for t,p in c["trust"])
    weblist = "".join(f"<li>{x}</li>" for x in c["web_list"])
    def typ(k, img, alt):
        lst = "".join(f"<li>{x}</li>" for x in c[f"type_{k}_list"])
        btn = "btn-primary" if k=="baby" else "btn-outline"
        return f'''<article class="type"><div class="type-img">{pic(root,img,c[alt])}</div><div class="type-body">
        <p class="eyebrow">{c[f"type_{k}_k"]}</p><h3>{c[f"type_{k}_h"]}</h3><p>{c[f"type_{k}_p"]}</p><ul class="checks">{lst}</ul>
        <a class="btn {btn} btn-block" href="{su}?rol={k}">{c[f"type_{k}_cta"]}</a></div></article>'''
    credits = "".join(f'<div class="credit"><h3>{t}</h3><p>{p}</p></div>' for t,p in c["credits"])
    faq = "".join(f'<details><summary>{q}</summary><div class="ans">{a}</div></details>' for q,a in c["faq"])
    links = "".join(f'<li><a href="{h}">{t}</a></li>' for t,h in c["f_links"])
    hid = "hoe" if nl else "how"
    body = f'''<body>
  <a class="skip" href="#inhoud">{c["skip"]}</a>
  {hdr}
  <main id="inhoud">
  <section class="hero"><div class="wrap hero-grid">
    <div class="hero-img">{pic(root,"terrace",c["hero_alt"],1280,720,lazy=False)}</div>
    <div>
      <h1>{c["hero_h1"]}</h1>
      <p class="sub">{c["hero_sub"]}</p>
      {roles(c, su)}
    </div>
  </div></section>

  <section class="sec sec-soft"><div class="wrap">
    <div class="sec-head"><p class="eyebrow">{c["p_kicker"]}</p></div>
    <ul class="promise">{promise}</ul>
  </div></section>

  <section class="sec" id="{hid}"><div class="wrap">
    <div class="sec-head"><p class="eyebrow">{c["how_kicker"]}</p><h2>{c["how_h2"]}</h2><p class="lead">{c["how_lead"]}</p></div>
    <ol class="steps">{how}</ol>
  </div></section>

  <section class="sec sec-soft"><div class="wrap">
    <div class="sec-head"><p class="eyebrow">{c["trust_kicker"]}</p><h2>{c["trust_h2"]}</h2></div>
    <div class="trust-grid">{trust}</div>
  </div></section>

  <section class="sec"><div class="wrap">
    <div class="sec-head"><p class="eyebrow">{c["types_kicker"]}</p><h2>{c["types_h2"]}</h2></div>
    <div class="types">{typ("daddy","man","type_daddy_alt")}{typ("baby","woman","type_baby_alt")}</div>
  </div></section>

  <section class="sec sec-soft"><div class="wrap split">
    <div class="split-img">{pic(root,"phone",c["web_alt"])}</div>
    <div class="split-copy"><p class="eyebrow">{c["web_kicker"]}</p><h2>{c["web_h2"]}</h2><p class="lead">{c["web_lead"]}</p><ul class="checks">{weblist}</ul></div>
  </div></section>

  <section class="sec"><div class="wrap">
    <div class="sec-head"><p class="eyebrow">{c["cr_kicker"]}</p><h2>{c["cr_h2"]}</h2><p class="lead">{c["cr_lead"]}</p></div>
    <div class="credits">{credits}</div>
  </div></section>

  <section class="sec sec-soft" id="faq"><div class="wrap faq-wrap">
    <div class="sec-head"><p class="eyebrow">{c["faq_kicker"]}</p><h2>{c["faq_h2"]}</h2></div>
    <div class="faq">{faq}</div>
  </div></section>

  <section class="close"><div class="wrap"><div class="close-box">
    <h2>{c["close_h2"]}</h2><p>{c["close_lead"]}</p>{roles(c, su, alt=True)}
  </div></div></section>
  </main>

  <footer class="foot"><div class="wrap">
    <div class="foot-grid foot-grid-2">
      <div>{brand(root, "./")}<p style="margin-top:.8rem;max-width:26rem">{c["f_about"]}</p></div>
      <div><h4>{c["f_site"]}</h4><ul>{links}</ul></div>
    </div>
    <div class="foot-legal"><p>{c["f_legal"]}</p></div>
    {langline(c, LH)}
  </div></footer>
  {LM_JS}
</body>
</html>
'''
    return head(c, c["title"], c["desc"], canon, root, BASE, BASE+"en/") + body

SU = {
"nl": {
  "steps":{"role":"Rol","about":"Over jou","looking":"Wat zoek je","bio":"Profiel","account":"Account"},
  "stepOf":"Stap {n} van {t}","left1":"Laatste stap","done":"Klaar","back":"Terug","next":"Verder","skip":"Overslaan",
  "role_h":"Wie ben je?","role_p":"Kies wat bij je past. Je kunt dit later wijzigen.",
  "role_baby_k":"Je zoekt een sugardaddy of sugarmama","role_baby_t":"Ik ben sugarbaby","role_daddy_k":"Je zoekt een sugarbaby","role_daddy_t":"Ik ben sugardaddy / sugarmama",
  "lead_baby":"Aanmelden als sugarbaby","lead_daddy":"Aanmelden als sugardaddy / sugarmama",
  "about_h":"Over jou","about_p":"Alleen de basis. Een bijnaam mag.",
  "f_name":"Gebruikersnaam","f_loc":"Stad of provincie","f_loc_ph":"Kies een stad of provincie","f_year":"Geboortejaar","f_year_ph":"Kies je geboortejaar",
  "grp_cities":"Grote steden","grp_regions":"Provincies","other":"Ergens anders in Nederland",
  "about_micro":"We tonen alleen je stad of provincie, nooit je adres. Je moet 18 jaar of ouder zijn.",
  "looking_h":"Wat zoek je?","looking_p":"Zo weten we welke profielen we je straks laten zien.","grp_who":"Ik zoek","grp_what":"Waarvoor? (meerdere mogelijk)",
  "who":[["sugardaddy","Een sugardaddy"],["sugarmama","Een sugarmama"],["sugarbaby","Een sugarbaby"],["any","Maakt niet uit"]],
  "what":[["langdurig","Een vaste regeling"],["afentoe","Af en toe afspreken"],["mentor","Begeleiding / mentor"],["reizen","Samen reizen"],["chatten","Eerst online kennismaken"]],
  "bio_h":"Korte profieltekst","bio_p":"Eén zin over jezelf. Je kunt dit ook later doen.","f_bio":"Profieltekst (optioneel)","bio_micro":"Maximaal 120 tekens. Geen telefoonnummer of andere contactgegevens.",
  "acc_h":"Account aanmaken","acc_p":"SugarDates is nog niet live. Je komt op de wachtlijst en we mailen je bij de livegang.",
  "f_email":"E-mailadres","f_pass":"Wachtwoord (minimaal 8 tekens)","acc_micro":"Andere leden zien je e-mailadres niet. In deze testversie wordt je wachtwoord niet opgeslagen.",
  "chk_age":"Ik ben 18 jaar of ouder","chk_terms":"Ik ga akkoord met de <a href=\"#\">voorwaarden</a> en het <a href=\"#\">privacybeleid</a>","submit":"Aanmelden",
  "e_name":"Vul een gebruikersnaam in.","e_loc":"Kies een stad of provincie.","e_year":"Kies je geboortejaar. Je moet 18 jaar of ouder zijn.",
  "e_who":"Kies wie je zoekt.","e_what":"Kies minstens één optie.","e_email":"Vul een geldig e-mailadres in.","e_pass":"Je wachtwoord moet minstens 8 tekens hebben.",
  "e_age":"Bevestig dat je 18 jaar of ouder bent.","e_terms":"Ga akkoord met de voorwaarden en het privacybeleid.",
  "ok_h":"Je staat op de wachtlijst, {name}","ok_p":"Bij de livegang sturen we een e-mail naar {email}.",
  "s_role":"Rol","s_name":"Gebruikersnaam","s_loc":"Regio","s_year":"Geboortejaar","s_who":"Zoekt","s_what":"Waarvoor","s_bio":"Profieltekst","s_email":"E-mail",
  "r_baby":"Sugarbaby","r_daddy":"Sugardaddy / sugarmama",
  "ok_next":"Bij de livegang bevestig je je e-mailadres en maak je je profiel af.",
  "home":"Naar de homepage","reset":"Opnieuw beginnen",
  "trust":["Alleen 18+","Gratis aanmelden","Nog niet live: je komt op de wachtlijst"],
  "cities":["Amsterdam","Rotterdam","Den Haag","Utrecht","Eindhoven","Groningen","Almere","Tilburg","Breda","Nijmegen","Arnhem","Haarlem","Amersfoort","Enschede","Den Bosch","Zwolle","Leiden","Maastricht","Delft","Alkmaar"],
  "regions":["Drenthe","Flevoland","Friesland","Gelderland","Groningen","Limburg","Noord-Brabant","Noord-Holland","Overijssel","Utrecht","Zeeland","Zuid-Holland"],
},
"en": {
  "steps":{"role":"Role","about":"About you","looking":"Looking for","bio":"Profile","account":"Account"},
  "stepOf":"Step {n} of {t}","left1":"Last step","done":"Done","back":"Back","next":"Continue","skip":"Skip",
  "role_h":"Who are you?","role_p":"Choose what fits. You can change this later.",
  "role_baby_k":"You're looking for a sugar daddy or mommy","role_baby_t":"I'm a sugar baby","role_daddy_k":"You're looking for a sugar baby","role_daddy_t":"I'm a sugar daddy / mommy",
  "lead_baby":"Joining as a sugar baby","lead_daddy":"Joining as a sugar daddy / mommy",
  "about_h":"About you","about_p":"Just the basics. A nickname is fine.",
  "f_name":"Username","f_loc":"State","f_loc_ph":"Choose your state","f_year":"Birth year","f_year_ph":"Choose your birth year",
  "grp_cities":"States","grp_regions":"","other":"Outside the US",
  "about_micro":"We only show your state or city, never your address. You must be 18 or older.",
  "looking_h":"What are you looking for?","looking_p":"So we know which profiles to show you.","grp_who":"I'm looking for","grp_what":"For what? (choose any)",
  "who":[["sugardaddy","A sugar daddy"],["sugarmama","A sugar mommy"],["sugarbaby","A sugar baby"],["any","No preference"]],
  "what":[["langdurig","An ongoing arrangement"],["afentoe","Meeting now and then"],["mentor","Mentoring"],["reizen","Traveling together"],["chatten","Chatting online first"]],
  "bio_h":"Short profile text","bio_p":"One line about yourself. You can also do this later.","f_bio":"Profile text (optional)","bio_micro":"Up to 120 characters. No phone numbers or other contact details.",
  "acc_h":"Create your account","acc_p":"SugarDates isn't live yet. You'll join the waitlist and we'll email you at launch.",
  "f_email":"Email","f_pass":"Password (at least 8 characters)","acc_micro":"Other members can't see your email. This test version doesn't store your password.",
  "chk_age":"I'm 18 or older","chk_terms":"I agree to the <a href=\"#\">Terms</a> and <a href=\"#\">Privacy Policy</a>","submit":"Sign up",
  "e_name":"Enter a username.","e_loc":"Choose your state.","e_year":"Choose your birth year. You must be 18 or older.",
  "e_who":"Choose who you're looking for.","e_what":"Choose at least one option.","e_email":"Enter a valid email address.","e_pass":"Your password needs at least 8 characters.",
  "e_age":"Confirm that you're 18 or older.","e_terms":"Please agree to the Terms and Privacy Policy.",
  "ok_h":"You're on the waitlist, {name}","ok_p":"We'll email {email} when we launch.",
  "s_role":"Role","s_name":"Username","s_loc":"Location","s_year":"Birth year","s_who":"Looking for","s_what":"For","s_bio":"Profile text","s_email":"Email",
  "r_baby":"Sugar baby","r_daddy":"Sugar daddy / mommy",
  "ok_next":"At launch you'll confirm your email and finish your profile.",
  "home":"Back to the homepage","reset":"Start over",
  "trust":["18+ only","Free to sign up","Not live yet: you'll join the waitlist"],
  "cities":["Alabama","Alaska","Arizona","Arkansas","California","Colorado","Connecticut","Delaware","District of Columbia","Florida","Georgia","Hawaii","Idaho","Illinois","Indiana","Iowa","Kansas","Kentucky","Louisiana","Maine","Maryland","Massachusetts","Michigan","Minnesota","Mississippi","Missouri","Montana","Nebraska","Nevada","New Hampshire","New Jersey","New Mexico","New York","North Carolina","North Dakota","Ohio","Oklahoma","Oregon","Pennsylvania","Rhode Island","South Carolina","South Dakota","Tennessee","Texas","Utah","Vermont","Virginia","Washington","West Virginia","Wisconsin","Wyoming"],
  "regions":[],
},
}

def signup(c):
    nl = c["lang"]=="nl"
    root = "../" if nl else "../../"
    canon = BASE + c["path"] + c["signup"]
    s = dict(SU[c["lang"]]); s["lang"]=c["lang"]; s["storage"]="sugardates-v5-"+c["lang"]; s["root"]=root; s["minAge"]=MIN_AGE
    s["imgs"]={"baby":"woman","daddy":"man"}
    SH = {"nl":"./","en":"../en/signup/"} if nl else {"nl":"../../aanmelden/","en":"./"}
    lang = langmenu(c, SH)
    body = f'''<body>
  <a class="skip" href="#inhoud">{c["skip"]}</a>
  <div class="su-page">
    <header class="top"><div class="wrap top-in" style="max-width:none">{brand(root, "../")}{lang}</div></header>
    <div class="su-wrap">
      <aside class="su-visual">{pic(root,"terrace",c["su_alt"],1280,720,lazy=False)}</aside>
      <section class="su-main">
        <div class="su-card">
          <div class="step-meta">
            <button type="button" class="back-btn" id="back-btn" hidden><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M15 6l-6 6 6 6"/></svg>{s["back"]}</button>
            <p class="step-count" id="step-count"></p>
          </div>
          <div class="progress-track" aria-hidden="true"><div class="progress-fill" id="progress-fill"></div></div>
          <p class="sr-only" id="step-live" aria-live="polite"></p>
          <main id="inhoud"><div id="panel" class="panel-anim"></div></main>
        </div>
        <div class="su-trust" id="trust">{"".join(f"<span>{t}</span>" for t in s["trust"])}</div>
        <footer class="su-foot"><p>{c["f_legal"]}</p>{langline(c, SH)}</footer>
      </section>
    </div>
  </div>
  <noscript><p style="padding:1rem;text-align:center">JavaScript is required.</p></noscript>
  <script>window.SD={json.dumps(s, ensure_ascii=False)};</script>
  <script src="{root}assets/signup.js?v=7"></script>
  {LM_JS}
</body>
</html>
'''
    return head(c, c["su_title"], c["desc"], canon, root, BASE+"aanmelden/", BASE+"en/signup/", robots="noindex,follow") + body

def write(rel, txt):
    p = os.path.join(HERE, rel); os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w", encoding="utf-8").write(txt); print("wrote", rel, len(txt))

write("index.html", landing(COPY["nl"]))
write("en/index.html", landing(COPY["en"]))
write("aanmelden/index.html", signup(COPY["nl"]))
write("en/signup/index.html", signup(COPY["en"]))

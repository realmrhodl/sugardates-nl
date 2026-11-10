#!/usr/bin/env python3
"""Builds the static v5 pages (NL + EN) from one template.

Edit copy in COPY below, then run:  python3 v5/build.py
Outputs:
  v5/index.html            (nl-NL landing, SugarDates.nl)
  v5/aanmelden/index.html  (nl-NL signup)
  v5/en/index.html         (en-US landing, SugarDates.net)
  v5/en/signup/index.html  (en-US signup)
Shared: v5/assets/site.css, v5/assets/signup.js, v5/img/*
"""
import json, os, html

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = "https://realmrhodl.github.io/sugardates-nl/v5/"

ARROW = '<svg class="arr" width="16" height="10" viewBox="0 0 20 12" fill="none" stroke="currentColor" stroke-width="1.2" aria-hidden="true"><path d="M1 6h18M14 1l5 5-5 5"/></svg>'
MONO = '<svg class="mono" viewBox="0 0 40 40" aria-hidden="true"><circle cx="20" cy="20" r="19.25" fill="none" stroke="#e4cf9f" stroke-width=".9"/><text x="20" y="27.2" text-anchor="middle" font-family="Cormorant Garamond, Georgia, serif" font-style="italic" font-size="22" fill="#e4cf9f">S</text></svg>'
ICONS = {
 "lock":'<rect x="5" y="11" width="14" height="10" rx="1.5"/><path d="M8 11V8a4 4 0 0 1 8 0v3"/>',
 "mask":'<path d="M3 9c3-2 6-2 9 0 3-2 6-2 9 0 0 5-3 8-6 8-1.5 0-2.3-1-3-2-.7 1-1.5 2-3 2-3 0-6-3-6-8z"/><circle cx="8" cy="11" r="1"/><circle cx="16" cy="11" r="1"/>',
 "eye":'<path d="M2 12s3.5-6 10-6 10 6 10 6-3.5 6-10 6S2 12 2 12z"/><circle cx="12" cy="12" r="2.5"/>',
 "shield":'<path d="M12 3l7 4v6c0 4.2-2.9 7.2-7 8-4.1-.8-7-3.8-7-8V7l7-4z"/><path d="M9 12l2 2 4-4"/>',
 "flag":'<path d="M5 21V4M5 4h11l-2 4 2 4H5"/>',
 "age":'<circle cx="12" cy="12" r="9"/><path d="M8 9h1.5v6M12.5 10.5a1.5 1.5 0 0 1 3 0c0 1.5-3 2.5-3 4.5h3"/>',
}
def icon(n): return f'<svg viewBox="0 0 24 24" aria-hidden="true" stroke-linecap="round" stroke-linejoin="round">{ICONS[n]}</svg>'

COPY = {
"nl": {
  "lang":"nl", "locale":"nl_NL", "hreflang":"nl-NL", "path":"", "signup":"aanmelden/",
  "title":"SugarDates – sugardating in Nederland, discreet en 21+",
  "desc":"SugarDates is sugardating voor Nederland: discreet, pseudoniem welkom en alleen voor 21+. Meld je nu aan voor de wachtlijst.",
  "skip":"Naar de inhoud", "cta_top":"Aanmelden",
  "hero_h1":"Sugardating, <em>discreet</em> en op jullie voorwaarden.",
  "hero_sub":"SugarDates brengt genereuze, gevestigde mensen en ambitieuze sugarbabies in Nederland bij elkaar. Met duidelijke afspraken, zonder gedoe en zonder dat de wereld meekijkt.",
  "role_baby":"Ik ben sugarbaby", "role_daddy":"Ik ben sugardaddy of sugarmama",
  "hero_note":"<span>Alleen 21+</span> · Aanmelden voor de wachtlijst is kosteloos · SugarDates is nog niet live",
  "p_kicker":"In het kort",
  "promise":[("Profiel","Laat zien wie je bent en wat je zoekt. Een pseudoniem is welkom, jij kiest wat zichtbaar is."),
             ("Gesprek","Bespreek eerlijk wat jullie van elkaar verwachten, voordat je afspreekt."),
             ("Ontmoeten","Spreek af als het voor allebei goed voelt. In jullie tempo.")],
  "how_kicker":"Hoe het werkt", "how_h2":"In drie stappen <em>begonnen</em>",
  "how_lead":"Geen lange vragenlijsten vooraf. Je begint met je rol en vult de rest aan wanneer het jou uitkomt.",
  "how":[("Meld je aan","Kies je rol, een weergavenaam en je regio. Daarna een e-mailadres en wachtwoord."),
         ("Maak je profiel af","Een korte omschrijving en wat je zoekt. Foto's voeg je toe als de site live gaat."),
         ("Ga het gesprek aan","Bij livegang bekijk je profielen in jouw regio en stuur je berichten.")],
  "trust_kicker":"Waarom SugarDates", "trust_h2":"Gemaakt voor <em>discretie</em>",
  "trust_lead":"Sugardating vraagt om vertrouwen. Daarom is dat het uitgangspunt van het platform.",
  "trust":[("mask","Pseudoniem welkom","Je echte naam is niet nodig. Je kiest zelf een weergavenaam.",""),
           ("eye","Jij bepaalt wat je deelt","Wat op je profiel staat, bepaal je zelf. Je woonplaats is een stad of regio, nooit een adres.",""),
           ("lock","Discreet","Je profiel is niet openbaar vindbaar voor bezoekers die niet zijn ingelogd.","bij livegang"),
           ("shield","Profielverificatie","Leden kunnen hun profiel laten verifiëren, zodat je weet dat je met een echt persoon praat.","bij livegang"),
           ("flag","Melden en blokkeren","Iets niet in orde? Je kunt een profiel melden of blokkeren.","bij livegang"),
           ("age","Alleen 21+","SugarDates is uitsluitend voor volwassenen van 21 jaar en ouder.","")],
  "web_kicker":"Overal bij de hand", "web_h2":"Geen app nodig, <em>gewoon je browser</em>",
  "web_lead":"SugarDates werkt op je telefoon, tablet en laptop, rechtstreeks in de browser. Er staat dus geen opvallend app-icoon op je beginscherm.",
  "web_list":["Werkt op iPhone, Android en desktop","Niets te installeren","Inloggen met je e-mailadres en wachtwoord"],
  "web_alt":"Sfeerbeeld: champagne aan een bar met uitzicht op de gracht, geen echte leden",
  "types_kicker":"Wie je hier ontmoet", "types_h2":"Twee kanten van <em>één afspraak</em>",
  "type_daddy_k":"Sugardaddy of sugarmama", "type_daddy_h":"Wat is een <em>sugardaddy</em> of sugarmama?",
  "type_daddy_p":"Iemand die succesvol is, het druk heeft en graag tijd doorbrengt met een aantrekkelijk en energiek gezelschap. Openheid over wat je zoekt en wat je biedt staat voorop.",
  "type_daddy_list":["Gezelschap voor diners, uitjes en reizen","Ruimte om iemand te steunen en te begeleiden","Duidelijke afspraken in plaats van verwachtingen","Discreet, op jouw voorwaarden"],
  "type_daddy_cta":"Aanmelden als sugardaddy of sugarmama", "type_daddy_alt":"Sfeerbeeld: diner bij kaarslicht, geen echte leden",
  "type_baby_k":"Sugarbaby", "type_baby_h":"Wat is een <em>sugarbaby</em>?",
  "type_baby_p":"Iemand die zelfstandig is, ambitie heeft en weet wat ze of hij wil. Sugarbabies zijn studenten, starters, creatievelingen en ondernemers. Jij bepaalt je grenzen.",
  "type_baby_list":["Een ervaren gesprekspartner en mentor","Nieuwe plekken, ervaringen en netwerken","Steun die past bij wat jullie afspreken","Respect voor jouw tempo en grenzen"],
  "type_baby_cta":"Aanmelden als sugarbaby", "type_baby_alt":"Sfeerbeeld: avondlicht op een dakterras, geen echte leden",
  "cr_kicker":"Lidmaatschap", "cr_h2":"Hoe <em>credits</em> werken",
  "cr_lead":"SugarDates gaat werken met credits, net als Paydates. Je betaalt dus voor wat je gebruikt.",
  "credits":[("Aanmelden en profiel","Een account aanmaken en je profiel invullen kost niets."),
             ("Credits voor contact","Voor betaalde functies, zoals berichten sturen, gebruik je credits. Welke functies dat precies zijn, maken we bekend bij de livegang."),
             ("Vooraf duidelijk","Tarieven en pakketten publiceren we vóór de livegang. Je ziet altijd vooraf wat iets kost.")],
  "band_q":"Een goede regeling voelt voor <em>allebei</em> als een cadeau.",
  "band_p":"Sugardating draait om een relatie waarin beide kanten iets krijgen: aandacht, tijd, steun en plezier. SugarDates helpt jullie om dat vanaf het begin eerlijk te bespreken.",
  "faq_kicker":"Veelgestelde vragen", "faq_h2":"Goed om te <em>weten</em>",
  "faq":[("Wat is sugardating?","Een vorm van daten waarin beide partners vooraf openlijk bespreken wat ze van elkaar verwachten, bijvoorbeeld gezelschap, mentorschap of steun. Wat jullie afspreken, bepalen jullie samen."),
         ("Is SugarDates al live?","Nog niet. Je kunt je nu aanmelden voor de wachtlijst. Bij de livegang krijg je bericht op het e-mailadres waarmee je je aanmeldt."),
         ("Waarom 21+?","We kiezen bewust voor een minimumleeftijd van 21 jaar. Bij het aanmelden vragen we je geboortejaar en een bevestiging."),
         ("Moet ik mijn echte naam gebruiken?","Nee. Je kiest een weergavenaam, en een pseudoniem is prima. Je e-mailadres is niet zichtbaar voor andere leden."),
         ("Wat kost het?","Aanmelden is kosteloos. Voor betaalde functies gebruik je straks credits. De tarieven publiceren we vóór de livegang."),
         ("Wat gebeurt er met mijn gegevens?","Je gegevens zijn van jou en worden niet openbaar gemaakt. Je kunt je aanmelding altijd laten verwijderen. Meer staat in ons privacybeleid."),
         ("Is SugarDates escort of betaalde seks?","Nee. SugarDates is een datingplatform. Het aanbieden of vragen van seks tegen betaling hoort hier niet thuis en is niet toegestaan.")],
  "close_kicker":"Klaar om te beginnen?", "close_h2":"Meld je aan voor <em>SugarDates</em>",
  "close_lead":"Zet je naam op de wachtlijst en wees er vanaf de eerste dag bij. Het kost je twee minuten.",
  "close_alt":"Sfeerbeeld: wandeling langs een gracht in de schemer, geen echte leden",
  "hero_alt":"Sfeerbeeld: stel bij het raam van een grachtenpand in de avond, geen echte leden",
  "f_about":"SugarDates is sugardating voor Nederland en Europa. Een platform van Forest Road B.V., ook bekend van Paydates.nl.",
  "f_site":"Site", "f_links":[("Hoe het werkt","#hoe"),("Veelgestelde vragen","#faq"),("Privacy","#"),("Voorwaarden","#"),("Contact","#")],
  "f_region":"Regio", "region_here":"SugarDates.nl · NL/EU", "region_other":"SugarDates.net · USA", "region_soon":"in voorbereiding",
  "f_legal":"Alleen voor 21 jaar en ouder. Forest Road B.V. · Herengracht 449A, 1017 BR Amsterdam · KvK 97957232 · BTW NL868303550B01 · © 2026",
  # signup
  "su_title":"Aanmelden – SugarDates", "su_tag":"Dating op jullie voorwaarden.",
  "su_alt":"Sfeerbeeld: stel bij het raam van een grachtenpand, geen echte leden",
},
"en": {
  "lang":"en", "locale":"en_US", "hreflang":"en-US", "path":"en/", "signup":"signup/",
  "title":"SugarDates – discreet sugar dating, 21+",
  "desc":"SugarDates is sugar dating built around discretion: pseudonyms welcome, 21+ only. Join the waitlist today.",
  "skip":"Skip to content", "cta_top":"Join",
  "hero_h1":"Sugar dating, <em>discreet</em> and on your terms.",
  "hero_sub":"SugarDates connects generous, established people with ambitious sugar babies. Clear expectations, no games, and no one looking over your shoulder.",
  "role_baby":"I'm a sugar baby", "role_daddy":"I'm a sugar daddy or sugar mommy",
  "hero_note":"<span>21+ only</span> · Joining the waitlist is free · SugarDates is not live yet",
  "p_kicker":"At a glance",
  "promise":[("Profile","Show who you are and what you're looking for. Pseudonyms are welcome, and you choose what's visible."),
             ("Talk","Be upfront about what you both expect before you meet."),
             ("Meet","Meet when it feels right for both of you. At your own pace.")],
  "how_kicker":"How it works", "how_h2":"Get started in <em>three steps</em>",
  "how_lead":"No long questionnaire up front. Start with your role and fill in the rest whenever it suits you.",
  "how":[("Sign up","Pick your role, a display name and your area. Then an email address and password."),
         ("Finish your profile","A short intro and what you're looking for. You'll add photos once the site launches."),
         ("Start the conversation","At launch, browse profiles near you and send messages.")],
  "trust_kicker":"Why SugarDates", "trust_h2":"Built for <em>discretion</em>",
  "trust_lead":"Sugar dating runs on trust, so trust is where the platform starts.",
  "trust":[("mask","Pseudonyms welcome","You don't need your real name. Pick any display name you like.",""),
           ("eye","You decide what to share","Your profile shows what you choose. Your location is a city or region, never an address.",""),
           ("lock","Discreet","Profiles aren't visible to visitors who aren't signed in.","at launch"),
           ("shield","Profile verification","Members can verify their profile, so you know you're talking to a real person.","at launch"),
           ("flag","Report and block","Something off? You can report or block any profile.","at launch"),
           ("age","21+ only","SugarDates is for adults aged 21 and over only.","")],
  "web_kicker":"Always within reach", "web_h2":"No app needed, <em>just your browser</em>",
  "web_lead":"SugarDates works on your phone, tablet and laptop, right in the browser. So there's no telltale app icon on your home screen.",
  "web_list":["Works on iPhone, Android and desktop","Nothing to install","Sign in with your email and password"],
  "web_alt":"Mood image: champagne at a bar overlooking a canal, not real members",
  "types_kicker":"Who you'll meet", "types_h2":"Two sides of <em>one arrangement</em>",
  "type_daddy_k":"Sugar daddy or sugar mommy", "type_daddy_h":"What is a <em>sugar daddy</em> or sugar mommy?",
  "type_daddy_p":"Someone successful and busy who enjoys spending time with attractive, lively company. Being open about what you're looking for, and what you offer, comes first.",
  "type_daddy_list":["Company for dinners, events and travel","Room to support and mentor someone","Clear agreements instead of guesswork","Discreet, on your terms"],
  "type_daddy_cta":"Join as a sugar daddy or mommy", "type_daddy_alt":"Mood image: candlelit dinner, not real members",
  "type_baby_k":"Sugar baby", "type_baby_h":"What is a <em>sugar baby</em>?",
  "type_baby_p":"Someone independent and driven who knows what they want. Sugar babies are students, young professionals, creatives and entrepreneurs. You set your boundaries.",
  "type_baby_list":["An experienced mentor to talk things through with","New places, experiences and connections","Support that fits what you agree on","Respect for your pace and boundaries"],
  "type_baby_cta":"Join as a sugar baby", "type_baby_alt":"Mood image: evening light on a rooftop terrace, not real members",
  "cr_kicker":"Membership", "cr_h2":"How <em>credits</em> work",
  "cr_lead":"SugarDates will run on credits, so you pay for what you use.",
  "credits":[("Sign up and profile","Creating an account and filling in your profile is free."),
             ("Credits for contact","Paid features, like sending messages, use credits. We'll confirm exactly which features at launch."),
             ("Clear up front","We'll publish rates and packages before launch. You'll always see what something costs before you use it.")],
  "band_q":"A good arrangement feels like a gift to <em>both</em> of you.",
  "band_p":"Sugar dating is about a relationship where both sides get something: attention, time, support and fun. SugarDates helps you talk about that honestly from the start.",
  "faq_kicker":"FAQ", "faq_h2":"Good to <em>know</em>",
  "faq":[("What is sugar dating?","A way of dating where both partners openly discuss what they expect from each other up front, such as companionship, mentorship or support. What you agree on is up to the two of you."),
         ("Is SugarDates live yet?","Not yet. You can join the waitlist now, and we'll email you at launch."),
         ("Why 21+?","We've chosen a minimum age of 21. When you sign up, we ask for your birth year and a confirmation."),
         ("Do I have to use my real name?","No. You choose a display name, and a pseudonym is fine. Your email address isn't shown to other members."),
         ("What does it cost?","Joining is free. Paid features will use credits, and we'll publish the rates before launch."),
         ("What happens to my data?","Your data is yours and isn't made public. You can ask us to delete your signup at any time. See our privacy policy for details."),
         ("Is SugarDates an escort service?","No. SugarDates is a dating platform. Offering or requesting sex for money isn't allowed.")],
  "close_kicker":"Ready to begin?", "close_h2":"Join <em>SugarDates</em>",
  "close_lead":"Put your name on the waitlist and be there from day one. It takes about two minutes.",
  "close_alt":"Mood image: a walk along a canal at dusk, not real members",
  "hero_alt":"Mood image: a couple by the window of a canal house in the evening, not real members",
  "f_about":"SugarDates.net is the US home of SugarDates, on the same platform as SugarDates.nl. Operated by Forest Road B.V.",
  "f_site":"Site", "f_links":[("How it works","#how"),("FAQ","#faq"),("Privacy","#"),("Terms","#"),("Contact","#")],
  "f_region":"Region", "region_here":"SugarDates.net · USA", "region_other":"SugarDates.nl · NL/EU", "region_soon":"",
  "f_legal":"For adults 21 and over only. Forest Road B.V. · Herengracht 449A, 1017 BR Amsterdam, the Netherlands · Chamber of Commerce 97957232 · VAT NL868303550B01 · © 2026",
  "su_title":"Join – SugarDates", "su_tag":"Dating on your terms.",
  "su_alt":"Mood image: a couple by a canal house window, not real members",
},
}

def e(s): return html.escape(s, quote=True)

def head(c, title, desc, canon, root, alt_nl, alt_en):
    return f'''<!DOCTYPE html>
<html lang="{c["hreflang"]}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <title>{e(title)}</title>
  <meta name="description" content="{e(desc)}">
  <meta name="theme-color" content="#0d0a11">
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
  <link rel="icon" href="{root}assets/monogram.svg" type="image/svg+xml">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;1,400;1,500&family=Inter:wght@300;400;500&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="{root}assets/site.css?v=5">
</head>
'''

def langswitch(c, nl_href, en_href):
    if c["lang"]=="nl":
        return f'<nav class="lang" aria-label="Taal / Language"><span aria-current="true" lang="nl">NL</span><a href="{en_href}" hreflang="en-US" lang="en">EN</a></nav>'
    return f'<nav class="lang" aria-label="Language / Taal"><a href="{nl_href}" hreflang="nl-NL" lang="nl">NL</a><span aria-current="true" lang="en">EN</span></nav>'

def pic(root, name, alt, cls="", w=1280, h=720, lazy=True):
    ld = ' loading="lazy" decoding="async"' if lazy else ' fetchpriority="high"'
    return f'<picture><source srcset="{root}img/{name}.webp" type="image/webp"><img src="{root}img/{name}.jpg" alt="{e(alt)}" width="{w}" height="{h}"{ld}{cls}></picture>'

def roles(c, su):
    return (f'<div class="roles">'
            f'<a class="btn btn-gold" href="{su}?rol=baby">{c["role_baby"]} {ARROW}</a>'
            f'<a class="btn btn-line" href="{su}?rol=daddy">{c["role_daddy"]} {ARROW}</a></div>')

def landing(c):
    nl = c["lang"]=="nl"
    root = "" if nl else "../"
    su = c["signup"]
    canon = BASE + c["path"]
    hdr = f'''<header class="top"><div class="wrap top-in">
    <a class="brand" href="./" aria-label="SugarDates">{MONO}<span class="wordmark">SugarDates</span></a>
    <div class="top-right">{langswitch(c, "../", "en/")}<a class="btn btn-line btn-sm top-cta" href="{su}">{c["cta_top"]}</a></div>
  </div></header>'''
    promise = "".join(f'<li class="rv"><span class="num">{["I","II","III"][i]}</span><div><h3>{t}</h3><p>{p}</p></div></li>' for i,(t,p) in enumerate(c["promise"]))
    how = "".join(f'<li class="rv"><h3>{t}</h3><p>{p}</p></li>' for t,p in c["how"])
    trust = "".join(f'<div class="rv">{icon(i)}<h3>{t}{f" <em class=tag>{tag}</em>" if tag else ""}</h3><p>{p}</p></div>' for i,t,p,tag in c["trust"])
    weblist = "".join(f"<li>{x}</li>" for x in c["web_list"])
    def typ(k, img, alt):
        lst = "".join(f"<li>{x}</li>" for x in c[f"type_{k}_list"])
        btn = "btn-gold" if k=="baby" else "btn-line"
        return f'''<article class="type rv"><div class="type-img">{pic(root,img,c[alt],w=864,h=1152)}</div><div class="type-body">
        <p class="caps">{c[f"type_{k}_k"]}</p><h3>{c[f"type_{k}_h"]}</h3><p>{c[f"type_{k}_p"]}</p><ul class="checks">{lst}</ul>
        <a class="btn {btn}" href="{su}?rol={k}">{c[f"type_{k}_cta"]} {ARROW}</a></div></article>'''
    credits = "".join(f'<div class="credit rv"><h3>{t}</h3><p>{p}</p></div>' for t,p in c["credits"])
    faq = "".join(f'<details><summary>{q}</summary><div class="ans">{a}</div></details>' for q,a in c["faq"])
    links = "".join(f'<li><a href="{h}">{t}</a></li>' for t,h in c["f_links"])
    other_href = "en/" if nl else "../"
    soon = f' <span>({c["region_soon"]})</span>' if c["region_soon"] else ""
    hid = "hoe" if nl else "how"
    body = f'''<body>
  <a class="skip" href="#inhoud">{c["skip"]}</a>
  {hdr}
  <main id="inhoud">
  <section class="hero">
    <div class="hero-img">{pic(root,"salon",c["hero_alt"],lazy=False)}</div>
    <div class="hero-shade"></div>
    <div class="wrap hero-in">
      <div class="rule"></div>
      <h1>{c["hero_h1"]}</h1>
      <p class="sub">{c["hero_sub"]}</p>
      {roles(c, su)}
      <p class="hero-note">{c["hero_note"]}</p>
    </div>
  </section>

  <section class="sec" aria-label="{e(c["p_kicker"])}"><div class="wrap"><ul class="promise">{promise}</ul></div></section>

  <section class="sec sec-alt" id="{hid}"><div class="wrap">
    <div class="sec-head rv"><p class="caps">{c["how_kicker"]}</p><h2>{c["how_h2"]}</h2><p class="lead">{c["how_lead"]}</p></div>
    <ol class="steps">{how}</ol>
  </div></section>

  <section class="sec"><div class="wrap">
    <div class="sec-head rv"><p class="caps">{c["trust_kicker"]}</p><h2>{c["trust_h2"]}</h2><p class="lead">{c["trust_lead"]}</p></div>
    <div class="trust-grid">{trust}</div>
  </div></section>

  <section class="sec sec-alt"><div class="wrap split">
    <div class="split-img rv">{pic(root,"bar",c["web_alt"],w=1152,h=864)}</div>
    <div class="split-copy rv"><p class="caps">{c["web_kicker"]}</p><h2>{c["web_h2"]}</h2><p class="lead">{c["web_lead"]}</p><ul class="checks">{weblist}</ul></div>
  </div></section>

  <section class="sec"><div class="wrap">
    <div class="sec-head rv"><p class="caps">{c["types_kicker"]}</p><h2>{c["types_h2"]}</h2></div>
    <div class="types">{typ("daddy","dinner","type_daddy_alt")}{typ("baby","rooftop","type_baby_alt")}</div>
  </div></section>

  <section class="band"><div class="wrap rv"><blockquote>{c["band_q"]}</blockquote><p>{c["band_p"]}</p></div></section>

  <section class="sec sec-alt"><div class="wrap">
    <div class="sec-head rv"><p class="caps">{c["cr_kicker"]}</p><h2>{c["cr_h2"]}</h2><p class="lead">{c["cr_lead"]}</p></div>
    <div class="credits">{credits}</div>
  </div></section>

  <section class="sec" id="faq"><div class="wrap faq-wrap">
    <div class="sec-head rv"><p class="caps">{c["faq_kicker"]}</p><h2>{c["faq_h2"]}</h2></div>
    <div class="faq">{faq}</div>
  </div></section>

  <section class="close">
    <div class="close-img">{pic(root,"canal",c["close_alt"],w=864,h=1152)}</div><div class="close-shade"></div>
    <div class="wrap rv"><p class="caps">{c["close_kicker"]}</p><h2>{c["close_h2"]}</h2><p class="lead">{c["close_lead"]}</p>{roles(c, su)}</div>
  </section>
  </main>

  <footer class="foot"><div class="wrap">
    <div class="foot-grid">
      <div><a class="brand" href="./" aria-label="SugarDates">{MONO}<span class="wordmark">SugarDates</span></a><p style="margin-top:1rem;max-width:26rem">{c["f_about"]}</p></div>
      <div><h4>{c["f_site"]}</h4><ul>{links}</ul></div>
      <div><h4>{c["f_region"]}</h4><ul class="region"><li><span class="here" aria-current="true">● {c["region_here"]}</span></li><li><a href="{other_href}">{c["region_other"]}</a>{soon}</li></ul></div>
    </div>
    <div class="foot-legal"><span class="age" aria-hidden="true">21+</span><p>{c["f_legal"]}</p></div>
  </div></footer>
  <script>
  (function(){{var els=document.querySelectorAll('.rv');if(!('IntersectionObserver' in window)||matchMedia('(prefers-reduced-motion: reduce)').matches){{els.forEach(function(x){{x.classList.add('in')}});return}}
  var io=new IntersectionObserver(function(es){{es.forEach(function(en){{if(en.isIntersecting){{en.target.classList.add('in');io.unobserve(en.target)}}}})}},{{rootMargin:'0px 0px -8% 0px'}});els.forEach(function(x){{io.observe(x)}});}})();
  </script>
</body>
</html>
'''
    return head(c, c["title"], c["desc"], canon, root, BASE, BASE+"en/") + body

# ---------- signup strings (consumed by assets/signup.js) ----------
SU = {
"nl": {
  "steps":{"role":"Wie ben je?","about":"Over jou","looking":"Wat zoek je","bio":"Profiel","account":"Account"},
  "stepOf":"Stap {n} van {t}","left1":"Laatste stap","done":"Aanmelding ontvangen","back":"Terug","next":"Verder","skip":"Overslaan",
  "role_h":"Wie ben je op <em>SugarDates</em>?","role_p":"Kies wat het beste bij je past. Je kunt dit later nog wijzigen.",
  "role_baby_k":"Op jouw voorwaarden","role_baby_t":"Ik ben sugarbaby","role_daddy_k":"Genereus","role_daddy_t":"Ik ben sugardaddy of sugarmama",
  "lead_baby":"Je meldt je aan als sugarbaby.","lead_daddy":"Je meldt je aan als sugardaddy of sugarmama.",
  "about_h":"Vertel iets <em>over jezelf</em>","about_p":"Alleen de basis. Een pseudoniem is welkom.",
  "f_name":"Weergavenaam","f_loc":"Stad of provincie","f_loc_ph":"Kies een stad of provincie","f_year":"Geboortejaar","f_year_ph":"Kies je geboortejaar",
  "grp_cities":"Grote steden","grp_regions":"Provincies","other":"Ergens anders in Nederland",
  "about_micro":"Je woonplaats is een stad of provincie, nooit een adres. SugarDates is alleen voor 21+.",
  "looking_h":"Wat <em>zoek</em> je?","looking_p":"Dan weten we wie we je straks laten zien.","grp_who":"Ik zoek","grp_what":"Waarvoor (meerdere mag)",
  "who":[["sugardaddy","Een sugardaddy"],["sugarmama","Een sugarmama"],["sugarbaby","Een sugarbaby"],["any","Maakt niet uit"]],
  "what":[["langdurig","Een vaste regeling"],["afentoe","Af en toe afspreken"],["mentor","Mentorschap"],["reizen","Samen reizen"],["chatten","Eerst online kennismaken"]],
  "bio_h":"Je <em>tagline</em>","bio_p":"Eén zin die laat zien wie je bent. Mag je ook later doen.","f_bio":"Tagline (niet verplicht)","bio_micro":"Maximaal 120 tekens. Geen contactgegevens.",
  "acc_h":"Rond je <em>aanmelding</em> af","acc_p":"Nog een e-mailadres en wachtwoord. SugarDates is nog niet live; we zetten je op de wachtlijst.",
  "f_email":"E-mailadres","f_pass":"Wachtwoord (minimaal 8 tekens)","acc_micro":"Je e-mailadres is niet zichtbaar voor andere leden. In deze aanmelding wordt je wachtwoord niet opgeslagen.",
  "chk_age":"Ik ben 21 jaar of ouder","chk_terms":"Ik ga akkoord met de <a href=\"#\">voorwaarden</a> en het <a href=\"#\">privacybeleid</a>","submit":"Zet me op de wachtlijst",
  "e_name":"Vul een weergavenaam in. Een pseudoniem is prima.","e_loc":"Kies een stad of provincie.","e_year":"Kies je geboortejaar. Je moet 21 jaar of ouder zijn.",
  "e_who":"Kies wie je zoekt.","e_what":"Kies minstens één optie.","e_email":"Vul een geldig e-mailadres in.","e_pass":"Gebruik minstens 8 tekens voor je wachtwoord.",
  "e_age":"Bevestig dat je 21 jaar of ouder bent.","e_terms":"Ga akkoord met de voorwaarden en het privacybeleid.",
  "ok_h":"Je staat op de <em>wachtlijst</em>, {name}.","ok_p":"Bedankt. Bij de livegang van SugarDates krijg je bericht op {email}.",
  "s_role":"Rol","s_name":"Naam","s_loc":"Regio","s_year":"Geboortejaar","s_who":"Zoekt","s_what":"Waarvoor","s_bio":"Tagline","s_email":"E-mail",
  "r_baby":"Sugarbaby","r_daddy":"Sugardaddy of sugarmama",
  "ok_next":"Je account wordt actief bij de livegang. Dan bevestig je je e-mail en vul je je profiel verder aan.",
  "home":"Terug naar de homepage","reset":"Nieuwe aanmelding",
  "trust":["Discreet","Pseudoniem welkom","21+","Jij bepaalt wat je deelt"],
  "cities":["Amsterdam","Rotterdam","Den Haag","Utrecht","Eindhoven","Groningen","Almere","Tilburg","Breda","Nijmegen","Arnhem","Haarlem","Amersfoort","Enschede","Den Bosch","Zwolle","Leiden","Maastricht","Delft","Alkmaar"],
  "regions":["Drenthe","Flevoland","Friesland","Gelderland","Groningen","Limburg","Noord-Brabant","Noord-Holland","Overijssel","Utrecht","Zeeland","Zuid-Holland"],
},
"en": {
  "steps":{"role":"Who are you?","about":"About you","looking":"Looking for","bio":"Profile","account":"Account"},
  "stepOf":"Step {n} of {t}","left1":"Last step","done":"You're on the list","back":"Back","next":"Continue","skip":"Skip",
  "role_h":"Who are you on <em>SugarDates</em>?","role_p":"Pick what fits you best. You can change this later.",
  "role_baby_k":"On your terms","role_baby_t":"I'm a sugar baby","role_daddy_k":"Generous","role_daddy_t":"I'm a sugar daddy or mommy",
  "lead_baby":"You're signing up as a sugar baby.","lead_daddy":"You're signing up as a sugar daddy or mommy.",
  "about_h":"Tell us <em>about you</em>","about_p":"Just the basics. Pseudonyms are welcome.",
  "f_name":"Display name","f_loc":"State","f_loc_ph":"Choose your state","f_year":"Birth year","f_year_ph":"Choose your birth year",
  "grp_cities":"States","grp_regions":"","other":"Outside the US",
  "about_micro":"Your location is a state or city, never an address. SugarDates is 21+ only.",
  "looking_h":"What are you <em>looking for</em>?","looking_p":"So we know who to show you at launch.","grp_who":"I'm looking for","grp_what":"For (pick any)",
  "who":[["sugardaddy","A sugar daddy"],["sugarmama","A sugar mommy"],["sugarbaby","A sugar baby"],["any","No preference"]],
  "what":[["langdurig","An ongoing arrangement"],["afentoe","Meeting now and then"],["mentor","Mentorship"],["reizen","Traveling together"],["chatten","Getting to know each other online first"]],
  "bio_h":"Your <em>tagline</em>","bio_p":"One line that shows who you are. You can also do this later.","f_bio":"Tagline (optional)","bio_micro":"Up to 120 characters. No contact details.",
  "acc_h":"Finish <em>signing up</em>","acc_p":"Just an email and password. SugarDates isn't live yet, so we'll add you to the waitlist.",
  "f_email":"Email address","f_pass":"Password (at least 8 characters)","acc_micro":"Your email isn't shown to other members. This signup doesn't store your password.",
  "chk_age":"I'm 21 or older","chk_terms":"I agree to the <a href=\"#\">Terms</a> and <a href=\"#\">Privacy Policy</a>","submit":"Add me to the waitlist",
  "e_name":"Enter a display name. A pseudonym is fine.","e_loc":"Choose your state.","e_year":"Choose your birth year. You must be 21 or older.",
  "e_who":"Choose who you're looking for.","e_what":"Choose at least one option.","e_email":"Enter a valid email address.","e_pass":"Use at least 8 characters for your password.",
  "e_age":"Confirm that you're 21 or older.","e_terms":"Please agree to the Terms and Privacy Policy.",
  "ok_h":"You're on the <em>waitlist</em>, {name}.","ok_p":"Thanks. We'll email you at {email} when SugarDates launches.",
  "s_role":"Role","s_name":"Name","s_loc":"Location","s_year":"Birth year","s_who":"Looking for","s_what":"For","s_bio":"Tagline","s_email":"Email",
  "r_baby":"Sugar baby","r_daddy":"Sugar daddy or mommy",
  "ok_next":"Your account goes live at launch. You'll confirm your email then and finish your profile.",
  "home":"Back to the homepage","reset":"Start over",
  "trust":["Discreet","Pseudonyms welcome","21+","You decide what to share"],
  "cities":["Alabama","Alaska","Arizona","Arkansas","California","Colorado","Connecticut","Delaware","District of Columbia","Florida","Georgia","Hawaii","Idaho","Illinois","Indiana","Iowa","Kansas","Kentucky","Louisiana","Maine","Maryland","Massachusetts","Michigan","Minnesota","Mississippi","Missouri","Montana","Nebraska","Nevada","New Hampshire","New Jersey","New Mexico","New York","North Carolina","North Dakota","Ohio","Oklahoma","Oregon","Pennsylvania","Rhode Island","South Carolina","South Dakota","Tennessee","Texas","Utah","Vermont","Virginia","Washington","West Virginia","Wisconsin","Wyoming"],
  "regions":[],
},
}

def signup(c):
    nl = c["lang"]=="nl"
    root = "../" if nl else "../../"
    canon = BASE + c["path"] + c["signup"]
    s = dict(SU[c["lang"]]); s["lang"]=c["lang"]; s["storage"]="sugardates-v5-"+c["lang"]; s["root"]=root
    home = "../"
    sw_nl = "../" if nl else "../../aanmelden/"
    sw_en = "../en/signup/" if nl else "./"
    lang = langswitch(c, "../../aanmelden/", "../en/signup/")
    body = f'''<body>
  <a class="skip" href="#inhoud">{c["skip"]}</a>
  <div class="su">
    <aside class="su-visual">
      {pic(root,"salon",c["su_alt"],lazy=False)}
      <header class="top"><div class="wrap top-in">
        <a class="brand" href="{home}" aria-label="SugarDates">{MONO}<span class="wordmark">SugarDates</span></a>
        {lang}
      </div></header>
      <p class="su-tag">{c["su_tag"]}</p>
    </aside>
    <section class="su-main">
      <div class="su-inner">
        <div class="su-desk-top">{lang}</div>
        <div class="su-card">
          <div class="step-meta">
            <button type="button" class="back-btn" id="back-btn" hidden><svg width="14" height="10" viewBox="0 0 20 12" fill="none" stroke="currentColor" stroke-width="1.2" aria-hidden="true"><path d="M19 6H1M6 1L1 6l5 5"/></svg> {s["back"]}</button>
            <p class="step-count" id="step-count"></p>
          </div>
          <div class="progress-track" aria-hidden="true"><div class="progress-fill" id="progress-fill"></div></div>
          <p class="sr-only" id="step-live" aria-live="polite"></p>
          <main id="inhoud"><div id="panel" class="panel-anim"></div></main>
          <div class="su-trust" id="trust">{"".join(f"<span>{t}</span>" for t in s["trust"])}</div>
        </div>
        <footer class="su-foot"><p>{c["f_legal"]}</p><p><span>{c["region_here"]}</span> · <a href="{('../en/' if nl else '../../')}">{c["region_other"]}</a></p></footer>
      </div>
    </section>
  </div>
  <noscript><p style="padding:1rem;text-align:center">JavaScript is required.</p></noscript>
  <script>window.SD={json.dumps(s, ensure_ascii=False)};</script>
  <script src="{root}assets/signup.js?v=5"></script>
</body>
</html>
'''
    return head(c, c["su_title"], c["desc"], canon, root, BASE+"aanmelden/", BASE+"en/signup/").replace('<meta name="theme-color"', '<meta name="robots" content="noindex,follow">\n  <meta name="theme-color"') + body

def write(rel, txt):
    p = os.path.join(HERE, rel); os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w", encoding="utf-8").write(txt); print("wrote", rel, len(txt))

write("index.html", landing(COPY["nl"]))
write("en/index.html", landing(COPY["en"]))
write("aanmelden/index.html", signup(COPY["nl"]))
write("en/signup/index.html", signup(COPY["en"]))

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
CSSV = 17
CHECK = '<span class="ck" aria-hidden="true"><svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"><path d="M6 12.5l4 4 8-9"/></svg></span>'

COPY = {
"nl": {
  "lang":"nl", "locale":"nl_NL", "hreflang":"nl-NL", "path":"", "signup":"aanmelden/",
  "title":"SugarDates – discreet sugardating in Nederland en Europa",
  "desc":"Sugardating waarbij je open bent over wat je zoekt. Maak een profiel, blijf discreet en ontmoet iemand die daarbij past. Voor Nederland en Europa.",
  "skip":"Naar de inhoud", "cta_top":"Aanmelden",
  "hero_h1":"Sugardating, open over wat je zoekt.",
  "hero_sub":"Voor wie een gevestigde sugardaddy zoekt, en voor de man die precies weet wat hij wil. Discreet, in Nederland en Europa.",
  "role_baby":"Ik zoek een sugardaddy", "role_daddy":"Ik ben sugardaddy",
  "hero_trust":"Discreet · Geen app nodig · Aanmelden is gratis",
  "hero_alt":"Sfeerbeeld: oudere man en jongere vrouw lopen arm in arm door een winkelstraat in Amsterdam, geen echte leden",
  "intro":"Geen giswerk. Geen app op je telefoon. Geen echte naam als je die niet wilt delen. Alleen volwassenen die open zijn over wat ze zoeken.",
  "how_kicker":"Hoe het werkt", "how_h2":"Drie stappen.",
  "how":[("Maak een profiel","Kies je rol, een gebruikersnaam en je regio. Een bijnaam is genoeg."),
         ("Zeg wat je zoekt","Gezelschap, begeleiding, samen reizen: zeg het vooraf, zodat niemand hoeft te raden."),
         ("Leer elkaar kennen","Stuur berichten en spreek af wanneer het voor jullie allebei goed voelt.")],
  "daddy_k":"Sugardaddy", "daddy_h":"Voor de man die geeft, en geen zin heeft in giswerk.",
  "daddy_p":"Je bent gevestigd, je hebt het druk en je wilt goed gezelschap. Je zegt vooraf wat je zoekt en wat je kunt bieden.",
  "daddy_list":["Gezelschap voor diners, reizen en evenementen","Iemand steunen of begeleiden","Duidelijke afspraken in plaats van verwachtingen"],
  "daddy_cta":"Aanmelden als sugardaddy", "daddy_alt":"Sfeerbeeld: man in pak in een hotellobby, geen echte leden",
  "baby_k":"Sugarbaby", "baby_h":"Voor wie weet wat ze wil, en dat ook zegt.",
  "baby_p":"Je bent zelfstandig en stelt je eigen grenzen. Je zoekt iemand met ervaring die ruimhartig is en jouw tempo respecteert.",
  "baby_list":["Een ervaren gesprekspartner of mentor","Nieuwe plekken en ervaringen","Steun die past bij jullie afspraken"],
  "baby_cta":"Vind je sugardaddy", "baby_alt":"Sfeerbeeld: vrouw met designertas en shoppingtas in een Amsterdamse winkelstraat, geen echte leden",
  "pr_kicker":"Privacy", "pr_h2":"Discreet als uitgangspunt.",
  "pr":[("Bijnaam mag","Je hoeft je echte naam niet te gebruiken."),
        ("Jij kiest wat je deelt","Je woonplaats is een stad of regio, nooit een adres."),
        ("E-mail blijft privé","Andere leden zien je e-mailadres niet."),
        ("Geen app nodig","Werkt in de browser. Geen app-icoon op je telefoon.")],
  "faq_kicker":"Vragen", "faq_h2":"Veelgestelde vragen",
  "faq":[("Wat is sugardating?","Daten waarbij je vooraf eerlijk bespreekt wat je van elkaar verwacht, zoals gezelschap, begeleiding of steun. Wat jullie afspreken, bepalen jullie samen."),
         ("Wat kost het?","Een account aanmaken is gratis. Voor sommige functies, zoals berichten sturen, gebruik je credits. Geen abonnement, en je ziet altijd vooraf wat iets kost."),
         ("Moet ik mijn echte naam gebruiken?","Nee. Je kiest zelf een gebruikersnaam. Je e-mailadres is niet zichtbaar voor andere leden."),
         ("Wat gebeurt er met mijn gegevens?","We maken je gegevens niet openbaar. Je kunt je account altijd laten verwijderen. Zie ons privacybeleid."),
         ("Is dit een escortsite?","Nee. SugarDates is een datingsite. Seks aanbieden of vragen tegen betaling is niet toegestaan.")],
  "band_alt":"Sfeerbeeld: man en vrouw toosten met champagne op een terras aan de gracht, geen echte leden",
  "close_h2":"Kies je rol.", "close_lead":"Aanmelden duurt een paar minuten. Een bijnaam is genoeg.",
  "f_about":"Sugardating voor Nederland en Europa. Een site van Forest Road B.V., het bedrijf achter Paydates.nl.",
  "f_links":[("Hoe het werkt","#hoe"),("Vragen","#faq"),("Privacy","#"),("Voorwaarden","#"),("Contact","#")],
  "f_legal":"Forest Road B.V. · Herengracht 449A, 1017 BR Amsterdam · KvK 97957232 · BTW NL868303550B01 · © 2026",
  "su_title":"Aanmelden – SugarDates",
  "su_alt":"Sfeerbeeld: oudere man en jongere vrouw lopen arm in arm door een winkelstraat, geen echte leden",
},
"en": {
  "lang":"en", "locale":"en_US", "hreflang":"en-US", "path":"en/", "signup":"signup/",
  "title":"SugarDates – discreet sugar dating, without the guesswork",
  "desc":"Sugar dating where you're upfront about what you want. Create a profile, stay discreet and meet someone who fits. For the United States.",
  "skip":"Skip to content", "cta_top":"Join",
  "hero_h1":"Sugar dating, upfront about what you want.",
  "hero_sub":"For anyone looking for an established sugar daddy, and for the man who knows exactly what he wants. Discreet, in the United States.",
  "role_baby":"I'm looking for a sugar daddy", "role_daddy":"I'm a sugar daddy",
  "hero_trust":"Discreet · No app needed · Free to sign up",
  "hero_alt":"Mood image: older man and younger woman walking arm in arm on a shopping street, not real members",
  "intro":"No guesswork. No app on your phone. No real name if you'd rather not share one. Just adults who are open about what they want.",
  "how_kicker":"How it works", "how_h2":"Three steps.",
  "how":[("Create a profile","Choose your role, a username and your area. A nickname is enough."),
         ("Say what you want","Companionship, mentoring, travel: say it up front, so nobody has to guess."),
         ("Get to know each other","Send messages and meet when it feels right for both of you.")],
  "daddy_k":"Sugar daddy", "daddy_h":"For the man who gives, and has no time for guesswork.",
  "daddy_p":"You're established, busy and you want good company. You say up front what you're looking for and what you can offer.",
  "daddy_list":["Company for dinners, travel and events","Supporting or mentoring someone","Clear agreements instead of assumptions"],
  "daddy_cta":"Join as a sugar daddy", "daddy_alt":"Mood image: man in a suit in a hotel lobby, not real members",
  "baby_k":"Sugar baby", "baby_h":"For anyone who knows what she wants, and says so.",
  "baby_p":"You're independent and you set your own boundaries. You're looking for someone experienced and generous who respects your pace.",
  "baby_list":["An experienced mentor to talk to","New places and experiences","Support that fits what you agree on"],
  "baby_cta":"Find your sugar daddy", "baby_alt":"Mood image: woman with a designer bag and shopping bag on a city street, not real members",
  "pr_kicker":"Privacy", "pr_h2":"Discreet by design.",
  "pr":[("Nicknames welcome","You don't have to use your real name."),
        ("You choose what to share","Your location is a city or state, never an address."),
        ("Your email stays private","Other members can't see your email address."),
        ("No app needed","Works in your browser. No app icon on your phone.")],
  "faq_kicker":"Questions", "faq_h2":"Frequently asked questions",
  "faq":[("What is sugar dating?","Dating where you're upfront about what you expect from each other, such as companionship, mentoring or support. What you agree on is up to the two of you."),
         ("What does it cost?","Creating an account is free. Some features, like sending messages, use credits. No subscription, and you always see the cost first."),
         ("Do I have to use my real name?","No. You choose a username. Your email isn't shown to other members."),
         ("What happens to my data?","We don't make your data public. You can ask us to delete your account at any time. See our privacy policy."),
         ("Is this an escort site?","No. SugarDates is a dating site. Offering or asking for sex for money isn't allowed.")],
  "band_alt":"Mood image: man and woman toasting with champagne at a canal-side terrace, not real members",
  "close_h2":"Choose your role.", "close_lead":"Signing up takes a few minutes. A nickname is enough.",
  "f_about":"SugarDates.net is the US site of SugarDates, on the same platform as SugarDates.nl. Operated by Forest Road B.V.",
  "f_links":[("How it works","#how"),("FAQ","#faq"),("Privacy","#"),("Terms","#"),("Contact","#")],
  "f_legal":"Forest Road B.V. · Herengracht 449A, 1017 BR Amsterdam, the Netherlands · Chamber of Commerce 97957232 · VAT NL868303550B01 · © 2026",
  "su_title":"Join – SugarDates",
  "su_alt":"Mood image: older man and younger woman walking arm in arm on a shopping street, not real members",
},
}

def e(s): return html.escape(s, quote=True)

def head(c, title, desc, canon, root, alts=None, robots="index,follow", preload=None, ld=None):
    """alts: {'nl-NL': url, 'en-US': url} for paired pages (adds x-default = nl)."""
    hl = ""
    if alts:
        hl = "".join(f'\n  <link rel="alternate" hreflang="{k}" href="{v}">' for k, v in alts.items())
        hl += f'\n  <link rel="alternate" hreflang="x-default" href="{alts.get("nl-NL", canon)}">'
    pre = ""
    if preload:
        name, sizes = preload
        pre = (f'\n  <link rel="preload" as="image" type="image/webp" fetchpriority="high" href="{root}img/{name}.webp" '
               f'imagesrcset="{srcset(root, name)}" imagesizes="{sizes}">')
    js = f'\n  <script type="application/ld+json">{json.dumps(ld, ensure_ascii=False, separators=(",",":"))}</script>' if ld else ""
    return f'''<!DOCTYPE html>
<html lang="{c["hreflang"]}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <title>{e(title)}</title>
  <meta name="description" content="{e(desc)}">
  <meta name="robots" content="{robots}">
  <meta name="theme-color" content="#ffffff">
  <link rel="canonical" href="{canon}">{hl}
  <meta property="og:type" content="website">
  <meta property="og:locale" content="{c["locale"]}">
  <meta property="og:site_name" content="SugarDates">
  <meta property="og:title" content="{e(title)}">
  <meta property="og:description" content="{e(desc)}">
  <meta property="og:url" content="{canon}">
  <meta property="og:image" content="{BASE}img/og.jpg">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="icon" href="{root}assets/logo.svg" type="image/svg+xml">{pre}
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Inter+Tight:wght@400;500;600&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="{root}assets/site.css?v={CSSV}">{js}
</head>
'''

GLOBE = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c2.6 2.6 2.6 15.4 0 18M12 3c-2.6 2.6-2.6 15.4 0 18"/></svg>'
CHEV = '<svg class="chev" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M6 9l6 6 6-6"/></svg>'
TICKSVG = '<svg class="lm-tick" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12.5l4.5 4.5L19 7.5"/></svg>'
LOCALES = [("nl","nl-NL","Europa · Nederlands","SugarDates.nl"),("en","en-US","United States · English","SugarDates.net")]
SHORT = {"nl":"Europa (NL)","en":"United States (EN)"}

def _nl_flag():
    # Official Netherlands tricolour: bright vermilion, white, cobalt blue.
    return ('<rect width="30" height="20" fill="#FFFFFF"/>'
            '<rect width="30" height="6.667" fill="#AE1C28"/>'
            '<rect y="13.333" width="30" height="6.667" fill="#21468B"/>')

def _us_flag():
    stripes = "".join(f'<rect y="{i*20/13:.3f}" width="30" height="{20/13:.3f}" fill="#b22234"/>' for i in range(0,13,2))
    dots = "".join(f'<circle cx="{1.3+x*2.2+(1.1 if y%2 else 0):.2f}" cy="{1.2+y*1.7:.2f}" r=".42"/>' for y in range(6) for x in range(6 if y%2==0 else 5))
    return f'<rect width="30" height="20" fill="#fff"/>{stripes}<rect width="13.6" height="{20*7/13:.3f}" fill="#3c3b6e"/><g fill="#fff">{dots}</g>'

FLAGS = {"nl":_nl_flag(), "en":_us_flag()}
def flag(code, w=20):
    h = round(w*2/3, 2)
    return f'<svg class="flag" width="{w}" height="{h}" viewBox="0 0 30 20" aria-hidden="true" focusable="false">{FLAGS[code]}</svg>'


def langmenu(c, hrefs):
    """hrefs: {'nl': url, 'en': url} relative to the current page."""
    cur = c["lang"]
    label = "Taal en land" if cur=="nl" else "Language and region"
    items = ""
    for code, hl, name, dom in LOCALES:
        on = code==cur
        attrs = ' aria-current="true"' if on else f' hreflang="{hl}" lang="{code}"'
        items += f'<li><a class="lm-item{" is-on" if on else ""}" href="{hrefs[code]}"{attrs}>{flag(code,24)}<span class="lm-txt"><span class="lm-name">{name}</span><span class="lm-dom">{dom}</span></span>{TICKSVG if on else ""}</a></li>'
    return (f'<div class="lm" data-lm><button type="button" class="lm-btn" aria-expanded="false" aria-controls="lm-list" aria-label="{label}: {dict((l[0],l[2]) for l in LOCALES)[cur]}, {dict((l[0],l[3]) for l in LOCALES)[cur]}">'
            f'{flag(cur)}<span class="lm-code">{cur.upper()}</span>{CHEV}</button>'
            f'<ul class="lm-list" id="lm-list" hidden>{items}</ul></div>')

def langline(c, hrefs):
    out=[]
    for code, hl, name, dom in LOCALES:
        if code==c["lang"]: out.append(f'<span aria-current="true">{flag(code,16)}{SHORT[code]}</span>')
        else: out.append(f'<a href="{hrefs[code]}" hreflang="{hl}" lang="{code}">{flag(code,16)}{SHORT[code]}</a>')
    return '<p class="foot-lang">'+'<span class="sep">/</span>'.join(out)+'</p>'

LM_JS = """<script>(function(){var t=document.querySelector('.top');if(!t)return;function f(){t.classList.toggle('is-scrolled',scrollY>8)}f();addEventListener('scroll',f,{passive:true});})();</script>
<script>(function(){document.querySelectorAll('[data-lm]').forEach(function(m){var b=m.querySelector('.lm-btn'),l=m.querySelector('.lm-list');
function set(o,f){b.setAttribute('aria-expanded',o);l.hidden=!o;if(o&&f){var a=l.querySelector('a');a&&a.focus();}}
b.addEventListener('click',function(e){set(b.getAttribute('aria-expanded')!=='true',e.detail===0);});
b.addEventListener('keydown',function(e){if(e.key==='ArrowDown'){e.preventDefault();set(true,true);}});
l.addEventListener('keydown',function(e){var a=[].slice.call(l.querySelectorAll('a')),i=a.indexOf(document.activeElement);
if(e.key==='ArrowDown'){e.preventDefault();a[(i+1)%a.length].focus();}if(e.key==='ArrowUp'){e.preventDefault();a[(i-1+a.length)%a.length].focus();}
if(e.key==='Escape'){set(false);b.focus();}});
document.addEventListener('click',function(e){if(!m.contains(e.target))set(false);});
m.addEventListener('focusout',function(e){if(e.relatedTarget&&!m.contains(e.relatedTarget))set(false);});
document.addEventListener('keydown',function(e){if(e.key==='Escape'&&!l.hidden){set(false);b.focus();}});});})();</script>"""

SMALL = {"walk":480, "man2":480, "woman2":480, "terrace":768, "car":768}
FULLW = {"walk":864, "man2":864, "woman2":864, "terrace":1280, "car":1280}
def srcset(root, name):
    s = f"{root}img/{name}.webp {FULLW.get(name,864)}w"
    if name in SMALL: s = f"{root}img/{name}-sm.webp {SMALL[name]}w, " + s
    return s

def pic(root, name, alt, w=864, h=1152, lazy=True, sizes="(min-width:1024px) 50vw, 100vw"):
    ld = ' loading="lazy" decoding="async"' if lazy else ' fetchpriority="high" decoding="async"'
    return (f'<picture><source type="image/webp" srcset="{srcset(root, name)}" sizes="{sizes}">'
            f'<img src="{root}img/{name}.jpg" alt="{e(alt)}" width="{w}" height="{h}"{ld}></picture>')

def brand(root, href):
    return f'<a class="brand" href="{href}" aria-label="SugarDates">SugarDates<span class="brand-dot" aria-hidden="true"></span></a>'

ARR = '<svg class="arr" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'

def roles(c, su, first="baby"):
    order = ["baby","daddy"] if first == "baby" else ["daddy","baby"]
    a, b = order
    return (f'<div class="roles"><a class="btn btn-primary" href="{su}?rol={a}">{c["role_"+a]}</a>'
            f'<a class="btn btn-secondary" href="{su}?rol={b}">{c["role_"+b]}</a></div>')

# ---------------------------------------------------------------- shared chrome
NAV = {
 "nl": [("Hoe het werkt","hoe-het-werkt/"),("Sugardaddy","sugardaddy/"),("Sugarbaby","sugarbaby/"),("Sugardating","wat-is-sugardating/"),("Steden","sugardating/"),("Veiligheid","veiligheid/")],
 "en": [("How it works","en/how-it-works/"),("Sugar daddy","en/sugar-daddy/"),("Sugar baby","en/sugar-baby/"),("Sugar dating","en/what-is-sugar-dating/"),("Cities","en/sugar-dating/"),("Safety","en/safety/")],
}
HUB = {
 "nl": [("SugarDates",[("Hoe het werkt","hoe-het-werkt/"),("Kosten","kosten/"),("Veiligheid","veiligheid/"),("Veelgestelde vragen","faq/")]),
        ("Voor wie",[("Sugardaddy","sugardaddy/"),("Sugarbaby","sugarbaby/"),("Wat is sugardating?","wat-is-sugardating/")]),
        ("Populair",[("Dating zonder relatie","dating-zonder-relatie/"),("Discreet daten","discreet-daten/"),("Daten als je getrouwd bent","daten-als-je-getrouwd-bent/"),("No strings attached","no-strings-attached/"),("Arrangement dating","arrangement-dating/"),("Sugardaddy gezocht","sugardaddy-gezocht/"),("Sugarbaby gezocht","sugarbaby-gezocht/")]),
        ("Steden",[("Amsterdam","sugardating/amsterdam/"),("Rotterdam","sugardating/rotterdam/"),("Den Haag","sugardating/den-haag/"),("Utrecht","sugardating/utrecht/"),("Eindhoven","sugardating/eindhoven/"),("België","sugardating/belgie/")])],
 "en": [("SugarDates",[("How it works","en/how-it-works/"),("Safety","en/safety/"),("FAQ","en/faq/")]),
        ("Guides",[("Sugar daddy","en/sugar-daddy/"),("Sugar baby","en/sugar-baby/"),("What is sugar dating?","en/what-is-sugar-dating/")]),
        ("Popular",[("Discreet dating","en/discreet-dating/"),("No strings attached","en/no-strings-attached/"),("Dating while married","en/dating-while-married/"),("Older man, younger woman","en/older-man-younger-woman/"),("Arrangement dating","en/arrangement-dating/")]),
        ("Cities",[("New York","en/sugar-dating/new-york/"),("Los Angeles","en/sugar-dating/los-angeles/"),("Miami","en/sugar-dating/miami/"),("Chicago","en/sugar-dating/chicago/"),("Las Vegas","en/sugar-dating/las-vegas/")])],
}
LEGAL_LINKS = {"nl":[("Privacy","#"),("Voorwaarden","#"),("Contact","#")], "en":[("Privacy","#"),("Terms","#"),("Contact","#")]}
UI = {
 "nl":{"menu":"Menu","close":"Menu sluiten","nav":"Hoofdmenu","crumbs":"Kruimelpad","home":"Home","more_faq":"Alle vragen","more_daddy":"Meer over sugardaddy's","more_baby":"Meer over sugarbaby's","more_how":"Lees hoe het werkt","foot_nav":"Sitemap"},
 "en":{"menu":"Menu","close":"Close menu","nav":"Main menu","crumbs":"Breadcrumb","home":"Home","more_faq":"All questions","more_daddy":"More about sugar daddies","more_baby":"More about sugar babies","more_how":"See how it works","foot_nav":"Sitemap"},
}
BURGER = '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" aria-hidden="true"><path class="b1" d="M4 8h16"/><path class="b2" d="M4 16h16"/></svg>'

def rootfor(slug): return "../" * slug.count("/")
def href(root, slug): return (root + slug) or "./"
def home_slug(lang): return "" if lang == "nl" else "en/"
def su_slug(lang): return "aanmelden/" if lang == "nl" else "en/signup/"

def header(c, root, hrefs, cur=""):
    lang = c["lang"]; u = UI[lang]
    nav = "".join(f'<li><a href="{href(root,s)}"{" aria-current=\"page\"" if cur==s else ""}>{t}</a></li>' for t, s in NAV[lang])
    su = href(root, su_slug(lang))
    return f'''<a class="skip" href="#inhoud">{c["skip"]}</a>
  <header class="top"><div class="top-in">
    {brand(root, href(root, home_slug(lang)))}
    <nav class="dnav" aria-label="{u["nav"]}"><ul>{nav}</ul></nav>
    <div class="top-right">{langmenu(c, hrefs)}<a class="btn btn-primary btn-sm top-cta" href="{su}">{c["cta_top"]}</a>
      <button type="button" class="nav-btn" aria-expanded="false" aria-controls="mnav" aria-label="{u["menu"]}" data-open="{u["menu"]}" data-close="{u["close"]}">{BURGER}</button></div>
  </div></header>
  <div class="mnav" id="mnav" hidden><nav aria-label="{u["nav"]}"><ul class="mnav-list">{nav}</ul></nav>
    <div class="mnav-cta">{roles(c, su)}</div></div>'''

def footer(c, root, hrefs):
    lang = c["lang"]
    cols = "".join(f'<div class="hub-col"><h2 class="hub-h">{h}</h2><ul>' + "".join(f'<li><a href="{href(root,s)}">{t}</a></li>' for t, s in items) + '</ul></div>' for h, items in HUB[lang])
    legal = "".join(f'<li><a href="{h}">{t}</a></li>' for t, h in LEGAL_LINKS[lang])
    return f'''<footer class="foot"><div class="wrap">
    <div class="foot-top">
      <div class="foot-brand">{brand(root, href(root, home_slug(lang)))}<p>{c["f_about"]}</p></div>
      <nav class="hub" aria-label="{UI[lang]["foot_nav"]}">{cols}</nav>
    </div>
    <div class="foot-bottom"><div><ul class="foot-links">{legal}</ul><p>{c["f_legal"]}</p></div>{langline(c, hrefs)}</div>
  </div></footer>'''

NAV_JS = """<script>(function(){var b=document.querySelector('.nav-btn'),p=document.getElementById('mnav');if(!b||!p)return;
function set(o){b.setAttribute('aria-expanded',o);b.setAttribute('aria-label',o?b.dataset.close:b.dataset.open);p.hidden=!o;document.documentElement.classList.toggle('menu-open',o);}
b.addEventListener('click',function(){set(b.getAttribute('aria-expanded')!=='true');});
p.addEventListener('click',function(e){if(e.target.closest('a'))set(false);});
document.addEventListener('keydown',function(e){if(e.key==='Escape'&&!p.hidden){set(false);b.focus();}});
matchMedia('(min-width:1024px)').addEventListener('change',function(m){if(m.matches)set(false);});})();</script>"""

def org_ld():
    return [
     {"@type":"Organization","@id":BASE+"#org","name":"SugarDates","url":BASE,"logo":BASE+"assets/logo.svg",
      "legalName":"Forest Road B.V.","vatID":"NL868303550B01",
      "address":{"@type":"PostalAddress","streetAddress":"Herengracht 449A","postalCode":"1017 BR","addressLocality":"Amsterdam","addressCountry":"NL"}},
     {"@type":"WebSite","@id":BASE+"#site","name":"SugarDates","url":BASE,"inLanguage":["nl-NL","en-US"],"publisher":{"@id":BASE+"#org"}},
    ]

def crumbs_ld(lang, crumbs):
    items = [("Home", home_slug(lang))] + list(crumbs)
    return {"@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":i+1,"name":n,"item":BASE+s} for i,(n,s) in enumerate(items)]}

def faq_ld(qas):
    return {"@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in qas]}

def faq_html(qas):
    return "".join(f'<details><summary>{q}<span class="pm" aria-hidden="true"></span></summary><div class="ans">{a}</div></details>' for q,a in qas)

# ---------------------------------------------------------------- landing extras
OFFER = {
 "nl":{"k":"Vraag en aanbod","h":"Wat zoek je, wat bied je?",
  "cols":[("Wat sugarbaby's zoeken",["Mentorschap en een netwerk","Aandacht en goede gesprekken","Luxe ervaringen: diners, hotels, uitjes","Samen reizen","Financiële ondersteuning, als jullie dat samen afspreken"],("Sugardaddy gezocht","sugardaddy-gezocht/")),
          ("Wat sugardaddy's zoeken",["Tijd en gezelschap","Discretie","Duidelijkheid vooraf","Iemand om mee uit te gaan en te reizen","Geen verwachtingen die niet zijn uitgesproken"],("Sugarbaby gezocht","sugarbaby-gezocht/"))],
  "pop":"Populair"},
 "en":{"k":"What people look for","h":"What you want, what you offer.",
  "cols":[("What sugar babies look for",["Mentoring and a network","Attention and good conversation","Luxury experiences: dinners, hotels, outings","Travel together","Financial support, if you agree on it together"],("Become a sugar baby","en/sugar-baby/")),
          ("What sugar daddies look for",["Time and company","Discretion","Clarity up front","Someone to go out and travel with","No unspoken expectations"],("Become a sugar daddy","en/sugar-daddy/"))],
  "pop":"Popular"},
}
CITY = {
 "nl":{"k":"Amsterdam","h":"Sugardating in Amsterdam.",
  "p":"Van een lunch in de Negen Straatjes tot een diner in Oud-Zuid: Amsterdam is internationaal en tegelijk klein genoeg om discreet af te spreken. Lees welke buurten goed werken voor een eerste ontmoeting.",
  "cta":("Sugardating in Amsterdam","sugardating/amsterdam/"),
  "img":("car","Sfeerbeeld: man helpt een jonge vrouw uit een auto aan een Amsterdamse gracht, geen echte leden"),
  "more":"Andere steden","cities":[("Rotterdam","sugardating/rotterdam/"),("Den Haag","sugardating/den-haag/"),("Utrecht","sugardating/utrecht/"),("Eindhoven","sugardating/eindhoven/"),("België","sugardating/belgie/")]},
 "en":{"k":"New York · Miami","h":"Sugar dating in your city.",
  "p":"From a West Village wine bar to a Brickell rooftop: local tips on neighborhoods that work well for a first date, plus how to meet safely.",
  "cta":("Sugar dating in New York","en/sugar-dating/new-york/"),
  "img":None,
  "more":"More cities","cities":[("Miami","en/sugar-dating/miami/"),("Los Angeles","en/sugar-dating/los-angeles/"),("Chicago","en/sugar-dating/chicago/"),("Las Vegas","en/sugar-dating/las-vegas/")]},
}
def chips(root, items):
    return '<ul class="chips">' + "".join(f'<li><a href="{href(root,s)}">{t}</a></li>' for t, s in items) + '</ul>'

def offer(c, root):
    from pages import POP_NL, POP_EN
    o = OFFER[c["lang"]]; pop = POP_NL if c["lang"]=="nl" else POP_EN
    cols = "".join(f'<div class="offer-col"><h3>{h}</h3><ul class="lines">' + "".join(f"<li>{x}</li>" for x in items) +
                   f'</ul><a class="link-sub" href="{href(root, l[1])}">{l[0]} {ARR}</a></div>' for h, items, l in o["cols"])
    return f'''<section class="offer"><div class="wrap">
    <div class="head-row"><p class="kicker">{o["k"]}</p><h2>{o["h"]}</h2></div>
    <div class="offer-grid">{cols}</div>
    <div class="pop"><p class="kicker">{o["pop"]}</p>{chips(root, pop)}</div>
  </div></section>'''

def city(c, root):
    o = CITY[c["lang"]]
    copy = (f'<div class="feature-copy"><p class="kicker">{o["k"]}</p><h2>{o["h"]}</h2><p class="body">{o["p"]}</p>'
            f'<div class="cta-row"><a class="link-cta" href="{href(root, o["cta"][1])}">{o["cta"][0]} {ARR}</a></div>'
            f'<p class="kicker city-more">{o["more"]}</p>{chips(root, o["cities"])}</div>')
    if o["img"]:
        return f'<section class="feature city-sec"><div class="feature-img">{pic(root, o["img"][0], o["img"][1], 1280, 720, sizes="(min-width:1024px) 50vw, 100vw")}</div>{copy}</section>'
    return f'<section class="feature city-sec no-img">{copy}</section>'

# ---------------------------------------------------------------- landing
def landing(c):
    nl = c["lang"]=="nl"; lang = c["lang"]; u = UI[lang]
    slug = home_slug(lang); root = rootfor(slug)
    su = href(root, su_slug(lang))
    canon = BASE + slug
    LH = {"nl": href(root, ""), "en": href(root, "en/")}
    hid = "hoe" if nl else "how"
    how = "".join(f'<li><span class="n">0{i+1}</span><h3>{t}</h3><p>{p}</p></li>' for i,(t,p) in enumerate(c["how"]))
    pr = "".join(f'<li><h3>{t}</h3><p>{p}</p></li>' for t,p in c["pr"])
    more = {"daddy": "sugardaddy/" if nl else "en/sugar-daddy/", "baby": "sugarbaby/" if nl else "en/sugar-baby/"}
    def feature(k, img, rev=False):
        lst = "".join(f"<li>{x}</li>" for x in c[f"{k}_list"])
        return f'''<section class="feature{' rev' if rev else ''}"><div class="feature-img">{pic(root,img,c[k+"_alt"])}</div>
      <div class="feature-copy"><p class="kicker">{c[k+"_k"]}</p><h2>{c[k+"_h"]}</h2><p class="body">{c[k+"_p"]}</p><ul class="lines">{lst}</ul>
      <div class="cta-row"><a class="link-cta" href="{su}?rol={k}">{c[k+"_cta"]} {ARR}</a><a class="link-sub" href="{href(root, more[k])}">{u["more_"+k]}</a></div></div></section>'''
    faq_slug = "faq/" if nl else "en/faq/"
    how_slug = "hoe-het-werkt/" if nl else "en/how-it-works/"
    body = f'''<body>
  {header(c, root, LH, slug)}
  <main id="inhoud">
  <section class="hero">
    <div class="hero-copy"><div class="hero-copy-in">
      <h1>{c["hero_h1"]}</h1>
      <p class="sub">{c["hero_sub"]}</p>
      {roles(c, su)}
      <p class="hero-trust">{c["hero_trust"]}</p>
    </div></div>
    <div class="hero-img">{pic(root,"walk",c["hero_alt"],lazy=False)}</div>
  </section>

  <section class="intro"><div class="wrap"><p>{c["intro"]}</p></div></section>

  <section class="how" id="{hid}"><div class="wrap">
    <div class="head-row"><p class="kicker">{c["how_kicker"]}</p><h2>{c["how_h2"]}</h2></div>
    <ol class="how-list">{how}</ol>
    <a class="link-sub" href="{href(root, how_slug)}">{u["more_how"]} {ARR}</a>
  </div></section>

  <div class="features">
  {feature("daddy","man2")}
  {feature("baby","woman2", rev=True)}
  </div>

  {offer(c, root)}

  <section class="privacy"><div class="wrap">
    <div class="head-row"><p class="kicker">{c["pr_kicker"]}</p><h2>{c["pr_h2"]}</h2></div>
    <ul class="pr-list">{pr}</ul>
  </div></section>

  <section class="faq-sec" id="faq"><div class="wrap faq-grid">
    <div><p class="kicker">{c["faq_kicker"]}</p><h2>{c["faq_h2"]}</h2><a class="link-sub" href="{href(root, faq_slug)}">{u["more_faq"]} {ARR}</a></div>
    <div class="faq">{faq_html(c["faq"])}</div>
  </div></section>

  {city(c, root)}

  <section class="band">{pic(root,"terrace",c["band_alt"],1280,720,sizes="100vw")}</section>

  <section class="close"><div class="wrap">
    <h2>{c["close_h2"]}</h2><p>{c["close_lead"]}</p>{roles(c, su)}
  </div></section>
  </main>
  {footer(c, root, LH)}
  {LM_JS}
  {NAV_JS}
</body>
</html>
'''
    ld = {"@context":"https://schema.org","@graph": org_ld() + [faq_ld(c["faq"])]}
    return head(c, c["title"], c["desc"], canon, root, {"nl-NL":BASE, "en-US":BASE+"en/"},
                preload=("walk","(min-width:1024px) 50vw, 100vw"), ld=ld) + body

# ---------------------------------------------------------------- subpages
import re
def inline(root, s):
    return re.sub(r"\[\[([^|\]]+)\|([^\]]+)\]\]", lambda m: f'<a href="{href(root, m.group(1))}">{m.group(2)}</a>', s)

def blocks_html(root, blocks):
    out = []; faqs = []
    for b in blocks:
        k = b[0]
        if k == "h2": out.append(f"<h2>{b[1]}</h2>")
        elif k == "p": out.append(f"<p>{inline(root, b[1])}</p>")
        elif k in ("ul", "ol"):
            cls = "steps" if k == "ol" else "lines"
            out.append(f'<{k} class="{cls}">' + "".join(f"<li>{inline(root, x)}</li>" for x in b[1]) + f"</{k}>")
        elif k == "faq":
            faqs += b[1]; out.append(f'<div class="faq">{faq_html(b[1])}</div>')
        elif k == "links":
            out.append(f'<section class="related"><h2>{b[1]}</h2><ul class="rel-list">' +
                       "".join(f'<li><a href="{href(root, s)}"><span>{t}</span>{ARR}</a></li>' for t, s in b[2]) + "</ul></section>")
    return "\n      ".join(out), faqs

def page(p, all_pages):
    c = COPY[p["lang"]]; lang = p["lang"]; u = UI[lang]
    slug = p["slug"]; root = rootfor(slug)
    su = href(root, su_slug(lang))
    canon = BASE + slug
    other = "en" if lang == "nl" else "nl"
    alt = p.get("alt")
    hrefs = {lang: "./", other: href(root, alt if alt else home_slug(other))}
    alts = None
    if alt:
        alts = {"nl-NL": BASE + (slug if lang=="nl" else alt), "en-US": BASE + (slug if lang=="en" else alt)}
    crumbs = p["crumbs"]
    cr = f'<li><a href="{href(root, home_slug(lang))}">{u["home"]}</a></li>'
    for i, (n, s) in enumerate(crumbs):
        cr += f'<li aria-current="page">{n}</li>' if i == len(crumbs)-1 else f'<li><a href="{href(root, s)}">{n}</a></li>'
    content, faqs = blocks_html(root, p["blocks"])
    img = p.get("img")
    media = f'<div class="pg-media">{pic(root, img[0], img[1], lazy=False, sizes="(min-width:1024px) 40vw, 100vw")}</div>' if img else ""
    navcur = next((s for t, s in NAV[lang] if slug.startswith(s)), slug)
    body = f'''<body>
  {header(c, root, hrefs, navcur)}
  <main id="inhoud" class="pg">
    <div class="pg-hero"><div class="wrap pg-head{" has-media" if img else ""}">
      <div class="pg-intro">
        <nav class="crumbs" aria-label="{u["crumbs"]}"><ol>{cr}</ol></nav>
        <h1>{p["h1"]}</h1>
        <p class="lead">{p["lead"]}</p>
        {roles(c, su, p.get("role","baby"))}
      </div>
      {media}
    </div></div>
    <div class="wrap"><article class="prose">
      {content}
    </article></div>
    <section class="close"><div class="wrap">
      <h2>{c["close_h2"]}</h2><p>{c["close_lead"]}</p>{roles(c, su, p.get("role","baby"))}
    </div></section>
  </main>
  {footer(c, root, hrefs)}
  {LM_JS}
  {NAV_JS}
</body>
</html>
'''
    graph = org_ld() + [crumbs_ld(lang, crumbs),
             {"@type":"WebPage","@id":canon,"url":canon,"name":p["title"],"description":p["desc"],"inLanguage":c["hreflang"],"isPartOf":{"@id":BASE+"#site"}}]
    if faqs: graph.append(faq_ld(faqs))
    pre = (img[0], "(min-width:1024px) 40vw, 100vw") if img else None
    return head(c, p["title"], p["desc"], canon, root, alts, preload=pre, ld={"@context":"https://schema.org","@graph":graph}) + body


SU = {
"nl": {
  "steps":{"role":"Rol","about":"Over jou","looking":"Wat zoek je","bio":"Profiel","account":"Account"},
  "stepOf":"Stap {n} van {t}","left1":"Laatste stap","done":"Klaar","back":"Terug","next":"Verder","skip":"Overslaan",
  "role_h":"Wie ben je?","role_p":"Kies wat bij je past. Je kunt dit later wijzigen.",
  "role_baby_k":"Je zoekt een sugardaddy","role_baby_t":"Ik ben sugarbaby","role_daddy_k":"Je zoekt een sugarbaby","role_daddy_t":"Ik ben sugardaddy",
  "lead_baby":"Aanmelden als sugarbaby","lead_daddy":"Aanmelden als sugardaddy",
  "about_h":"Over jou","about_p":"Alleen de basis. Een bijnaam mag.",
  "f_name":"Gebruikersnaam","f_loc":"Stad of provincie","f_loc_ph":"Kies een stad of provincie","f_year":"Geboortejaar","f_year_ph":"Kies je geboortejaar",
  "grp_cities":"Grote steden","grp_regions":"Provincies","other":"Ergens anders in Nederland",
  "about_micro":"We tonen alleen je stad of provincie, nooit je adres. Je moet 18 jaar of ouder zijn.",
  "looking_h":"Wat zoek je?","looking_p":"Zo weten we welke profielen we je straks laten zien.","grp_who":"Ik zoek","grp_what":"Waarvoor? (meerdere mogelijk)",
  "who":[["sugardaddy","Een sugardaddy"],["sugarbaby","Een sugarbaby"],["any","Maakt niet uit"]],
  "what":[["langdurig","Een vaste regeling"],["afentoe","Af en toe afspreken"],["mentor","Begeleiding / mentor"],["reizen","Samen reizen"],["chatten","Eerst online kennismaken"]],
  "bio_h":"Korte profieltekst","bio_p":"Eén zin over jezelf. Je kunt dit ook later doen.","f_bio":"Profieltekst (optioneel)","bio_micro":"Maximaal 120 tekens. Geen telefoonnummer of andere contactgegevens.",
  "acc_h":"Laat je e-mailadres achter","acc_p":"SugarDates is nog niet live. Je komt op de wachtlijst; bij de livegang mailen we je.",
  "f_email":"E-mailadres","acc_micro":"Andere leden zien je e-mailadres niet.",
  "chk_age":"Ik ben 18 jaar of ouder","chk_terms":"Ik ga akkoord met de <a href=\"#\">voorwaarden</a> en het <a href=\"#\">privacybeleid</a>","submit":"Plaats me op de wachtlijst",
  "e_name":"Vul een gebruikersnaam in.","e_loc":"Kies een stad of provincie.","e_year":"Kies je geboortejaar. Je moet 18 jaar of ouder zijn.",
  "e_who":"Kies wie je zoekt.","e_what":"Kies minstens één optie.","e_email":"Vul een geldig e-mailadres in.","e_pass":"Je wachtwoord moet minstens 8 tekens hebben.",
  "e_age":"Bevestig dat je 18 jaar of ouder bent.","e_terms":"Ga akkoord met de voorwaarden en het privacybeleid.",
  "ok_h":"Je staat op de wachtlijst, {name}","ok_p":"Bij de livegang sturen we een e-mail naar {email}.",
  "s_role":"Rol","s_name":"Gebruikersnaam","s_loc":"Regio","s_year":"Geboortejaar","s_who":"Zoekt","s_what":"Waarvoor","s_bio":"Profieltekst","s_email":"E-mail",
  "r_baby":"Sugarbaby","r_daddy":"Sugardaddy",
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
  "role_baby_k":"You're looking for a sugar daddy","role_baby_t":"I'm a sugar baby","role_daddy_k":"You're looking for a sugar baby","role_daddy_t":"I'm a sugar daddy",
  "lead_baby":"Joining as a sugar baby","lead_daddy":"Joining as a sugar daddy",
  "about_h":"About you","about_p":"Just the basics. A nickname is fine.",
  "f_name":"Username","f_loc":"State","f_loc_ph":"Choose your state","f_year":"Birth year","f_year_ph":"Choose your birth year",
  "grp_cities":"States","grp_regions":"","other":"Outside the US",
  "about_micro":"We only show your state or city, never your address. You must be 18 or older.",
  "looking_h":"What are you looking for?","looking_p":"So we know which profiles to show you.","grp_who":"I'm looking for","grp_what":"For what? (choose any)",
  "who":[["sugardaddy","A sugar daddy"],["sugarbaby","A sugar baby"],["any","No preference"]],
  "what":[["langdurig","An ongoing arrangement"],["afentoe","Meeting now and then"],["mentor","Mentoring"],["reizen","Traveling together"],["chatten","Chatting online first"]],
  "bio_h":"Short profile text","bio_p":"One line about yourself. You can also do this later.","f_bio":"Profile text (optional)","bio_micro":"Up to 120 characters. No phone numbers or other contact details.",
  "acc_h":"Leave your email","acc_p":"SugarDates isn't live yet. You'll join the waitlist and we'll email you at launch.",
  "f_email":"Email","acc_micro":"Other members can't see your email.",
  "chk_age":"I'm 18 or older","chk_terms":"I agree to the <a href=\"#\">Terms</a> and <a href=\"#\">Privacy Policy</a>","submit":"Join the waitlist",
  "e_name":"Enter a username.","e_loc":"Choose your state.","e_year":"Choose your birth year. You must be 18 or older.",
  "e_who":"Choose who you're looking for.","e_what":"Choose at least one option.","e_email":"Enter a valid email address.","e_pass":"Your password needs at least 8 characters.",
  "e_age":"Confirm that you're 18 or older.","e_terms":"Please agree to the Terms and Privacy Policy.",
  "ok_h":"You're on the waitlist, {name}","ok_p":"We'll email {email} when we launch.",
  "s_role":"Role","s_name":"Username","s_loc":"Location","s_year":"Birth year","s_who":"Looking for","s_what":"For","s_bio":"Profile text","s_email":"Email",
  "r_baby":"Sugar baby","r_daddy":"Sugar daddy",
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
    s = dict(SU[c["lang"]]); s["lang"]=c["lang"]; s["storage"]="sugardates-v5-2-"+c["lang"]; s["root"]=root; s["minAge"]=MIN_AGE
    s["imgs"]={"baby":"woman2","daddy":"man2"}
    SH = {"nl":"./","en":"../en/signup/"} if nl else {"nl":"../../aanmelden/","en":"./"}
    lang = langmenu(c, SH)
    body = f'''<body>
  <a class="skip" href="#inhoud">{c["skip"]}</a>
  <div class="su-page">
    <header class="top"><div class="top-in">{brand(root, "../")}{lang}</div></header>
    <div class="su-wrap">
      <aside class="su-visual">{pic(root,"walk",c["su_alt"],lazy=False)}</aside>
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
        <p class="su-trust" id="trust">{" · ".join(s["trust"])}</p>
        <footer class="su-foot"><p>{c["f_legal"]}</p>{langline(c, SH)}</footer>
      </section>
    </div>
  </div>
  <noscript><p style="padding:1rem;text-align:center">JavaScript is required.</p></noscript>
  <script>window.SD={json.dumps(s, ensure_ascii=False)};</script>
  <script src="{root}assets/signup.js?v={CSSV}"></script>
  {LM_JS}
</body>
</html>
'''
    return head(c, c["su_title"], c["desc"], canon, root, {"nl-NL":BASE+"aanmelden/","en-US":BASE+"en/signup/"}, robots="noindex,follow", preload=("walk","(min-width:1024px) 50vw, 100vw")) + body

def write(rel, txt):
    p = os.path.join(HERE, rel); os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w", encoding="utf-8").write(txt); print("wrote", rel, len(txt))

from pages import PAGES
write("index.html", landing(COPY["nl"]))
write("en/index.html", landing(COPY["en"]))
write("aanmelden/index.html", signup(COPY["nl"]))
write("en/signup/index.html", signup(COPY["en"]))
for pg in PAGES:
    write(pg["slug"] + "index.html", page(pg, PAGES))

# sitemap + robots
urls = [("", "en/"), ("en/", "")] + [(pg["slug"], pg.get("alt")) for pg in PAGES]
sm = ['<?xml version="1.0" encoding="UTF-8"?>',
      '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">']
for s, alt in urls:
    sm.append(f"  <url><loc>{BASE}{s}</loc>")
    if alt is not None:
        nl_s, en_s = (s, alt) if not s.startswith("en/") else (alt, s)
        sm.append(f'    <xhtml:link rel="alternate" hreflang="nl-NL" href="{BASE}{nl_s}"/>')
        sm.append(f'    <xhtml:link rel="alternate" hreflang="en-US" href="{BASE}{en_s}"/>')
        sm.append(f'    <xhtml:link rel="alternate" hreflang="x-default" href="{BASE}{nl_s}"/>')
    sm.append("  </url>")
sm.append("</urlset>")
write("sitemap.xml", "\n".join(sm) + "\n")
write("robots.txt", f"# Note: crawlers only read robots.txt at the domain root; copy this there at launch.\nUser-agent: *\nAllow: /\nSitemap: {BASE}sitemap.xml\n")

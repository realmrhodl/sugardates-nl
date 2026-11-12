# SugarDates – handoff (status 11 Nov 2026, desktop layout polish)

## Repo & hosting
- GitHub: `realmrhodl/sugardates-nl` (branch `main`), local clone `/workspace/sugardates-nl`
- Preview (GitHub Pages): https://realmrhodl.github.io/sugardates-nl/v5/ (root `/` redirects to `/v5/`)
- Commit as `realmrhodl <realmrhodl@users.noreply.github.com>` (`git -c user.name=… -c user.email=…`), `git pull --rebase` before push, verify Pages with curl ~1 min after push.
- v4 removed (backup `/workspace/sugardates-nl-notes/v4-backup/`), old root page backup `/workspace/sugardates-nl-notes/root-index-backup.html`, old photos `/workspace/sugardates-nl-notes/img-backup-pre-photo/`, competitor notes `/workspace/sugardates-nl-notes/ANALYSIS.md` (not in repo).

## Structure (v5 is the chosen concept)
- `v5/build.py` – generator. Run `python3 v5/build.py` from repo root. Contains:
  - `COPY` (landing copy nl/en), `SU` (signup strings nl/en), `OFFER` (vraag-en-aanbod), `CITY` (homepage city section)
  - `NAV`, `HUB` (footer link hub), `header()/footer()` shared on all pages, mobile menu (`NAV_JS`), language/region dropdown with SVG flags (`langmenu`, `LM_JS`; Netherlands flag for SugarDates.nl, US flag for SugarDates.net)
  - `landing()`, `page()` (generic subpage renderer: breadcrumbs, H1, lead, optional image, content blocks, CTA), `signup()`
  - JSON-LD (Organization, WebSite, WebPage, BreadcrumbList, FAQPage), canonical, hreflang pairs, OG
  - writes `sitemap.xml` (with xhtml alternates) and `robots.txt` (only effective at a domain root; copy there at launch)
  - `CSSV` = cache-bust version for `assets/site.css` / `assets/signup.js` – bump on CSS/JS changes
- `v5/pages.py` – all subpage content (NL + EN): role pages, guides, kosten, FAQ, city hubs (NL: Amsterdam, Rotterdam, Den Haag, Utrecht, Eindhoven, België; US: New York, Los Angeles, Miami, Chicago, Las Vegas), intent pages (dating-zonder-relatie, discreet-daten, daten-als-je-getrouwd-bent, no-strings-attached, oudere-man-jongere-vrouw, rijke-man-ontmoeten, sugardaddy-gezocht, sugarbaby-gezocht, arrangement-dating, sugardating-studenten + EN mirrors). Inline links: `[[slug|label]]`; `alt` = slug of the other-language twin (hreflang).
- `v5/assets/site.css` – mobile-first theme; `v5/assets/signup.js` – 3-step waitlist signup (localStorage placeholder, no password collected); `v5/img/` – webp + jpg + `-sm.webp` (480w / 768w) variants, sizes 864×1152 (portrait) and 1280×720 (wide), `og.jpg` 1200×630.
- `PLATFORM.md` – platform notes (one DB/accounts for both domains).

## Decisions
- **Domains:** SugarDates.nl = Netherlands + rest of EU (nl-NL, EUR); SugarDates.net = USA (en-US, USD). One platform, shared database and accounts (`home_region`, `country`, `locale`).
- **Sugardaddy focus:** roles are only *sugardaddy* and *sugarbaby* (sugarmama removed everywhere). Hero/CTAs lead with "Ik zoek een sugardaddy" / "Ik ben sugardaddy".
- **Age:** 18+ everywhere, but shown **only on signup** (checkbox, birth-year validation, one trust line). No 18+, "niet live", "wachtlijst", "bij livegang" on landing/content pages. Don't claim the site is live.
- **Signup (waitlist):** 3 steps only — role, basics (username, city/region, birth year), email + 18+ + terms. No password (none is stored or collected). Submit CTA is "Plaats me op de wachtlijst" / "Join the waitlist". Looking-for and bio are deferred until launch.
- **Copy:** Dutch primary, EN mirror; no personal names, fake stats, testimonials, timers or invented features; "Online" never "Virtueel"; not an escort site (no sex for money) stated where relevant; privacy claims limited to: username/pseudonym, own photo choice, city/region only, email private, no app, account deletion.
- **Design:** light premium editorial (Inter Tight 500 headlines, Inter body, hairlines, pill buttons) with a clean white and red palette: white `#ffffff` backgrounds, off-white `#faf8f7` alternating sections, near-black `#1a1a1a` / grey `#5f5f5f` text, deep red `#b3122e` (hover `#8f0e24`) for primary buttons, links, kickers, the wordmark dot and small details, hairlines `#ececec`, footer near-black `#141414` with white text. No purple, plum, champagne, blush or lavender. No dark/gold/ornate "AI" look. Text wordmark "SugarDates" + red dot. Header "Aanmelden" is a small primary button (visible on mobile too). Homepage hero states the value prop in the H1, with a true trust line under the role CTAs ("Discreet · Geen app nodig · Aanmelden is gratis"). Mobile hero image is 3:2 so both role CTAs fit above the fold. Desktop rhythm is tighter (≈80px section padding, no 100svh feature blocks); role and city sections are true 50/50 photo+copy splits; section kickers sit stacked above headings rather than in a wide 1fr/2fr grid.
- **Photos:** AI-generated but realistic candid style (35mm/Portra, natural light, real backgrounds); older distinguished man + attractive young adult woman, luxury cues (designer-style bag with a **generic rosette pattern – never LV or any real logo/letters**, champagne, hotel lobby, shopping bags, car). No real hotel/brand names visible. Alt text always "Sfeerbeeld …, geen echte leden" / "Mood image …, not real members".
- **SEO/perf:** unique title/meta/H1 per page; Lighthouse mobile ≥ 90 (last run: 99/100/100/100 on home and intent pages).

## Pricing & payments (research conclusions, not yet on site)
- Credits model, no subscription: **€3–6 per unlock** (e.g. opening a conversation).
- Packs roughly **€49 / €149 / €279 (/ €449)**; kosten page currently says "tarieven volgen".
- PSPs: **Verotel** for EU (.nl); **CCBill / Segpay** for US (.net) – high-risk dating-friendly processors.
- **Neutral billing descriptor** on bank statements (discreet-daten page only promises that the statement wording will be shown with the rates – don't claim more until confirmed).

## Open items
- KvK number 97957232 confirmed by Stefan (10 Nov 2026). Footer: Forest Road B.V., Herengracht 449A, 1017 BR Amsterdam, BTW NL868303550B01.
- Confirm "zonder abonnement / geen abonnement" wording (matches credits model).
- Footer line "het bedrijf achter Paydates.nl" – keep or remove?
- Privacy/Voorwaarden/Contact pages are `#` placeholders.
- Real backend (accounts, credits, payments, moderation, age verification) – front-end only so far.
- Move robots.txt/sitemap to the real domain roots at launch; canonicals currently point at the GitHub Pages preview (`BASE` in build.py).

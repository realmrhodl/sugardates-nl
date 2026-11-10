# SugarDates platform: one platform, two domains

Status: concept. Only the v5 preview pages exist. Neither domain runs on this platform yet, and SugarDates.net is not live.

| | SugarDates.nl | SugarDates.net |
|---|---|---|
| Region | Netherlands / EU | USA |
| Default locale | `nl-NL` | `en-US` |
| Currency | EUR | USD |
| Preview | `/v5/` and `/v5/aanmelden/` | `/v5/en/` and `/v5/en/signup/` |
| Operator | Forest Road B.V., Amsterdam | Forest Road B.V., Amsterdam |

## One database, one user base
- Both domains run on a single application and share **one database**. There is one `users` table and one set of profiles, messages and credits.
- An account is **shared**: the same email and password log in on both domains. A user has a `home_region` (`nl` or `us`) and a `locale`. These are set at signup from the domain the user came in on, and the user can change them later.
- Which members a user sees is decided by search filters (region, distance, country), not by the domain. By default a user browses members in their own region.
- Credits are stored once, per user. Each purchase is recorded in its own currency (EUR or USD). Prices are set per region in a price table, never by converting at runtime.

## Domain, region and locale
- The request host sets the region: `sugardates.nl` gives `nl`/EUR/`nl-NL`, and `sugardates.net` gives `us`/USD/`en-US`.
- The UI language can be switched on either domain (NL/EN). This switch changes the language only. It does **not** change the region, currency or legal entity of the site.
- Each domain has its own legal pages, pricing page, payment providers, VAT and sales-tax handling, and support address.

## SEO: hreflang between the domains
Each public page links to its counterpart on the other domain:
```html
<link rel="alternate" hreflang="nl-NL" href="https://sugardates.nl/...">
<link rel="alternate" hreflang="en-US" href="https://sugardates.net/...">
<link rel="alternate" hreflang="x-default" href="https://sugardates.nl/...">
```
- Each domain has a self-referencing canonical. The two domains are never canonical to each other.
- Each domain has its own sitemap and robots.txt. Search Console is set up per domain.
- The v5 preview already outputs these tags, pointing at the GitHub Pages preview URLs.

## Legal and age rules per region
- **NL/EU: 21+.** We ask for the birth year and an explicit confirmation. GDPR applies: a privacy policy, data export and deletion, and a processing register.
- **USA:** 18+ is legally possible, but **we keep 21+ unless Stefan decides otherwise.** The minimum age should be a per-region config value (`min_age`), so it can change without new code.
- US-specific items to settle before launch: Terms and Privacy for US users (including CCPA/CPRA for California), sales tax, payment-provider rules for dating, and any state-level age-verification laws.
- Both regions: no offering or requesting sex for money. Profiles can be reported and blocked, and profile verification comes at launch.

## Front-end preview (this repo)
- `v5/build.py` builds all four v5 pages from one template. The copy is in its `COPY` and `SU` dictionaries. Run `python3 v5/build.py` after any copy change.
- `v5/assets/site.css` holds the shared styles. `v5/assets/signup.js` is the shared signup logic, which takes its strings per page from `window.SD`.
- Signup is front-end only. Answers and the email address go into `localStorage` as a placeholder. The password is never stored.

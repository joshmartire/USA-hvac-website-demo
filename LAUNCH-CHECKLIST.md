# Launch Checklist, Test Report & Technical Notes

USA version. Template build: October 22, 2026. Sample business "Kelvin Heating & Cooling" with placeholder contact details and **sample estimate pricing**. Not ready to index until the client items below are done and `demo_mode` is `false`.

## 1. Test report

### Passed (verified by running tests, not by reading code)

**Static QA** (`python3 _build/qa.py`, output in `_build/qa-latest.txt`): 31 passed, 0 warnings, 0 failed.
- 71 pages; 0 broken internal links or assets; 0 orphan pages.
- 69 indexable pages: unique titles and descriptions, titles ≤ 65 characters, descriptions ≤ 160, one H1 per page, no duplicate IDs, every form field labelled, every image has alt text.
- Canonical and `og:url` match the file path on every page. `sitemap.xml` is valid with 69 URLs, exactly matching the indexable inventory. `robots.txt` points to it.
- JSON-LD parses everywhere: HVACBusiness ×1, WebSite ×1, Service ×56, BreadcrumbList ×69, ItemList ×1, ContactPage ×1, WebApplication ×1.
- All 14 service pages have 500–600 words of main content (506–548). The 42 city pages have 334–419 words each, and the highest overlap between any two city pages is 44%.
- Contrast ≥ 4.5:1 on all key colour pairs, including the heat colour (lowest 4.6). No template tokens or placeholder text. No "best / #1 / guarantee / years of experience / star rating" claims. Legal links in every footer. Demo banner on every page.
- Opening animation is on exactly the 69 indexable pages, never the 404 or thank-you page. The estimate page carries the config prices; the home picker submits to it.
- 
**Browser QA** (`python3 _build/qa_browser.py --axe axe.min.js`, headless Chromium at 1440×900 and 390×844, output in `_build/qa-browser-latest.txt`): 31 passed, 0 failed.
- Opening animation plays when landing on a service page, the dial counts up, it clears itself and doesn't replay on the next page. Skipped for a `#hash` and reduced motion; a click skips it.
- Hero airflow canvas draws. Home page CLS 0.005.
- The pinned sequence steps through all 5 stages and builds the full drawing.
- Services dropdown opens inside the window (including hover-then-click) and Escape closes it. Mobile menu and mobile call bar work.
- **Instant estimate:** all 60 system × home size × efficiency combinations match prices recalculated from `site.config.json`; add-ons add correctly; ductless prices per zone and hides home size and duct add-ons; the home picker deep-links the chosen system; the lead form opens with system, options and range filled in and blocks empty submissions; the phone live-price bar shows while the result is off screen.
- Repair-or-replace check flips at the configured threshold.
- Contact form blocks empty submissions and flags invalid email.
- No horizontal scrolling at 390 px on 12 key pages. No JavaScript errors.
- axe-core (WCAG 2.1 A/AA): 0 violations on home, estimate, a service page, contact and a city hub.

### Not tested yet (needs the deployed site or client accounts)
- Form delivery: needs the client's email in `form_endpoint` and FormSubmit activation.
- Live domain, HTTPS, PageSpeed Insights / Core Web Vitals in the field, Rich Results Test, real iOS Safari and Android devices, Search Console.

### Requires client input
| Item | Where |
|---|---|
| Business name, legal name, phone, email, domain, hours | `site.config.json` |
| Public address or service-area business | `address` |
| **Real installed prices per system, size and efficiency multipliers, add-on prices, minimum job** | `estimator` |
| Whether they truly offer 24/7 no-heat service | `emergency_24_7` |
| Form recipient + FormSubmit activation | `form_endpoint` |
| Google Business Profile and social URLs | `site.config.json` |
| Confirm hero badges and working standards are true (licensed gas and refrigerant techs, recorded start-up readings) | `_build/pages.py` (`tags`, `features`, `statement_points`) |
| Maintenance plan details, if they offer one (the page only says "ask us") | `content_services.py` → `hvac-maintenance` |
| Real About story, TSSA registration, licences, insurance, manufacturer dealer status | `pages.py` → `about` |
| Real job photos | `photos` in config |
| Legal review of Privacy, Terms, Cookie drafts | `pages.py` |

## 2. Manual launch tasks
1. Fill in config, set real estimate pricing, set `"demo_mode": false`, run `build.py`, `qa.py`, `qa_browser.py`. All must pass.
2. **Hosting (Cloudflare Pages, like the other demos):** connect the repo, no build command, output `/`. Add the custom domain in Pages and the DNS records Cloudflare shows. `_headers` noindexes only `*.pages.dev`.
3. Submit a test quote and a test estimate, confirm the FormSubmit activation email, and submit again.
4. Search Console: verify the domain and submit `https://CLIENTDOMAIN/sitemap.xml`.
5. Rich Results Test and PageSpeed Insights (mobile) on home, a service page and the estimate page.
6. Make sure the Google Business Profile name, phone and service areas match the site.
7. If analytics, ad pixels, chat, financing or booking widgets are added: update the Privacy and Cookie policies and add consent blocking where required.

## 3. Instant estimate: how prices are calculated
`base × home-size multiplier × efficiency multiplier + add-ons` → ± `range_pct`, rounded to `round_to`, never below `minimum_job`. Ductless: `base + (zones − 1) × extra_zone`, × efficiency, no size multiplier or duct add-ons. Shown as a ballpark with "not a quote" wording on the page, the result card and in the Terms. Rebates are deliberately not included because programs change often.

Repair-or-replace: age × repair price compared with `repair_rule.threshold` (5,000 by default, a common industry rule of thumb), with wording that it isn't advice for specific equipment and that safety issues override it.

## 4. Licensing and safety wording (Michigan)
The copy refers to licensed mechanical contractors and mechanical permits for furnace, AC and heat pump installs, EPA Section 608 certification for refrigerant work, and licensed electricians with electrical permits for new circuits, and tells visitors who smell gas to leave and call their gas utility's emergency line. For a client in another state, check that state's licensing and permit rules and review `content_services.py`, `content_costs.py`, `content_cities.py` and `pages.py`. Privacy and Terms are US drafts governed by the client's state law (`legal_jurisdiction`).

## 5. SEO and technical summary
- `lang="en-US"`, unique title and description, canonical, Open Graph and Twitter card on every page; favicon set and 1200×630 share image generated in the brand colours.
- Schema: one `HVACBusiness` (`/#business`) on home; `Service` on service and city pages; `BreadcrumbList` matching visible breadcrumbs; `WebSite`, `ItemList`, `ContactPage`, `WebApplication` (estimate). No reviews, ratings, prices or FAQ markup.
- Internal linking: mega menu and footer link every service; each service links its 3 city pages and related services; city pages cross-link and link the hub; the estimate is linked from the nav, footer, hero, asides, CTAs and the relevant city pages.
- Performance: no images or video in the hero (the airflow is drawn on a canvas after load), self-hosted fonts, one 69 KB stylesheet, 20 KB of deferred site JS and 8 KB more on the estimate page.
- Privacy: no cookies, no analytics, no third-party requests; one sessionStorage flag for the intro.

## 6. URL structure and redirects
Directory-style URLs with trailing slashes; legal pages use `.html`. If a page is renamed after launch, add a Cloudflare redirect rule (or keep a page at the old path with `<meta http-equiv="refresh">` and a canonical pointing to the new URL).

## 7. Page inventory
Full list with canonical URLs: `_build/page-inventory.json`. Home 1, estimate 1, services hub 1, services 14, service × city 42, areas hub 1, city hubs 3, about/FAQ/contact 3, legal 3, thank-you 1 (noindex), 404 1.

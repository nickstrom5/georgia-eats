# Georgia Eats (ga-eats) — notes for Claude Code sessions

Started 2026-10-26 from `../state-prompts/GEORGIA_PROMPT.md` and `../STATE_EATS_PLAYBOOK.md`. Pipeline and app ported from `../tn-eats/`
(plus or-eats' bcore() fix, oh-eats' Denny's delivery brands and search folding, wa-eats' private_dining.py, co-eats' tracking/injection).
Leaderboard artifact (private, v2): link in `LOCAL.md`. Sources and calibration: `playbook/12-sources.md`. Brand (Nick, 2026-10-26):
`playbook/05-naming.md` — "Georgia Eats: Restaurants", subtitle "Wings, Barbecue & Lowcountry", Home Screen "GA Eats", peach icon on
pine, landscape palette (pine #1F4D3A, clay #A63D24, cream #FFF8EE, peach fill only), clay band under pines.

## Rebuild
```bash
cd pipeline
../.venv/bin/python listings.py && ../.venv/bin/python geocode_official.py && ../.venv/bin/python geocode_census.py
../.venv/bin/python calibrate.py && ../.venv/bin/python build_research.py && ../.venv/bin/python georgia.py
GA_APP=1 ../.venv/bin/python georgia.py && cd .. && cp data/app/places.json data/app/detail-*.json GeorgiaEats/Resources/
.venv/bin/python scripts/make-leaderboard.py      # then republish site/index.html + georgia.json, ga_detail.json, ga_shapes.json
```
Official spine: DOR Active Alcohol Licenses (June 2026 xlsx; includes pending). Fulton inspections = calibration only. No grades shown.
MICHELIN 2026 Georgia (64) read via Claude's web fetcher (check_sources.FETCHER_HOSTS). JBF: data/research/jbf.json. Weaver D's closed.

## Site, listing and screenshots
- `scripts/make-site.py` writes docs/ (17 pages; CSP hash-pinned) and `playbook/site-numbers.json`; `scripts/explore.js` is the web app
  (storage prefix "gaeats-", default guide wings); `scripts/qa-site.py` is the QA (static + Playwright/Chrome; calls
  `publish_app_data.app_data_checks()`). Run QA in the background: the browser half takes several minutes.
- `scripts/make-listing.py` writes playbook/06 (listing), 13 (App Review reply + recording script) and app-store/listing.json from
  site-numbers.json. Re-run after every data refresh. Keywords 97/100, reply 3,988/4,000 (tight: trim before adding).
- Screenshots: `scripts/capture-screenshots.sh <sim>` (screens: home wings buford lowcountry soul detail map honors oldest saved
  about; ScreenshotMode pins Midtown Atlanta, Doraville for buford, Savannah for lowcountry), then `scripts/site-images.sh`, then
  make-site + qa-site. App Store frames: `scripts/appstore-screenshots.py` (8 iPhone, 6 iPad; pine band, clay rule, cream).
- OTA data updates (`../OTA-DATA.md`): app side is the shared DataUpdates.swift; site side is `scripts/publish_app_data.py`
  (docs/data/app/manifest.json). Publish after each re-export.
- Records requests: `playbook/records-requests.md` (DPH statewide, GNR, optional Fulton). Drafts only; Nick sends.

## Status (2026-10-28, 16:40)
- Done: pipeline, research guides (soul 5, Buford Hwy 9, lemon pepper wings 21, BBQ 3, Lowcountry 7, peach 1, GA chains 1, oldest 7;
  build_research.py regenerates data/research/app/*.json), leaderboard artifact v2, app (GeorgiaEats/, com.georgiaeats.ios), brand,
  site (make-site, explore.js, qa-site), listing copy, records-request drafts (unsent), OTA copy docs/data/app 2026-10-28.1 (fresh:
  the never-published 2026-10-27.1 files were removed, no "previous").
- QA 2026-10-28 fixes (Nick approved GA-1, GA-2):
  - GA-1: calibrate.py no longer writes Google 2021's open share into calibration_app.json (calibration.json keeps it for the private
    leaderboard). NoGoogleDataTests (GeorgiaEatsTests.swift) failed on the old bundle (2 open_google_2021 keys) and passes now;
    `grep -ri google docs GeorgiaEats/Resources` finds nothing.
  - GA-2: adult_venues.json adds Fannies' Cabaret (4401 Fulton Industrial Blvd SW), Club Wax (4375 Commerce Dr SW, an adult club in the
    same cluster, juice only) and Sugar Daddy Palace (149 Cobblestone Blvd, Stockbridge: Overture's "bakery" lists a Ning social
    network and a toll-free number; not a place to eat). Overture files Fannies' and Club Wax as plain bars, so the near-a-club
    check missed them. Riley's Show Bar, Trapeze and "Atlanta's Hottest Gentlemen's Club" are nearby but in neither dataset.
  - Cuisine: research entries can carry "cuisine" (build_research.py CUISINE): Mary Mac's Tea Room -> Soul & Southern (was Coffee &
    Café from "TEA"), Las Delicias de la Abuela -> Latin & Caribbean (was Bakery & Sweets). The Briarcliff J.R. Crickets lookup now
    uses "JR Crickets" + 4805 (the display rename had broken it).
- QA 2026-10-28 P1 fixes (Nick approved; evening):
  - Same place twice with pins apart (Taco Mac Gainesville, Tequila Mexican Restaurant Dallas, Chicken and Beer ATL): the DOR gives no
    coordinates, so a license's pin is a geocoder's guess (Census put Taco Mac on the far stretch of Jesse Jewell Pkwy and Tequila on
    Paulding Blvd, not Paulding Plaza; every airport license shares one point at the Domestic Terminal; an address point ignores
    Atlanta's quadrant). georgia.py's second pass now joins a license to the listing at its street address (same house number, the
    same street with a spelling slip allowed, the same trailing direction, the same business; up to 30 km, any county), and the
    listing keeps its pin and county. QA_DEBUG["license_same_address"] lists the joins. In all three named pairs the listing's pin is
    right (its neighbours at the same address agree; Concourse D's labelled listings sit at lon -84.4293).
  - Paul Thomas Chocolates: georgia.py WEB_HOME ships its home page instead of a past free-tasting event page.
  - Websites: qa-site.py website_problem() and the app's DataGuards.notOneURL check that every website is one URL (no space, no second
    link, not a map pin; a bare host is fine).
  - Swift TrackingParams mirrors tracking_params.py's new rules (after "#", in the path, no scheme, _kx); the guard's logic, run on
    macOS, finds 4 tagged links in the old bundle and none in the new.
  - Result: app 24,540 -> 24,495 places (23,300 -> 23,275 restaurants; 87 license joins), web 28,518 -> 28,486 restaurants. OTA
    docs/data/app re-published fresh as 2026-10-28.1 (the earlier, never-pushed files replaced). Retaken on iOS 27.0: iPhone and iPad
    01-home and docs/img/screen-home now show "23,275 restaurants in 459 towns"; the other shots didn't change.
  - Tests after the fixes (iPhone 17 Pro Max, iOS 27.0): 52/52 unit, the new tracking and one-URL guards included. Full site QA OK.
  - Left (flagged, not fixed): ~14 listing-vs-listing duplicates with pins 1-30 km apart (Your Pie Roswell, Spice and Sky); 7 town-
    fallback license pins 9+ km from their own ZIP (Hilton Atlanta Airport, Hattie B's Moreland Way); gad_source/gad_campaignid tags
    (3, shared tracking_params.py); ~29 websites that are one-off event, sign-up, careers or gift-card pages.
- App Store screenshots (iOS 27.0): playbook/app-store/iphone (8, 1320x2868: home wings detail buford lowcountry map honors saved) and
  ipad (6, 2064x2752: home wings buford map lowcountry oldest; honors and soul titles truncate in the iPad list column), framed;
  raws in playbook/app-store/raw/. Landing page has real iPhone 17 Pro Max captures (docs/img).
- Tests (Xcode.app 27.1 27A9269, iOS 27.0): iPhone 17 Pro Max 52/52 unit; iPad Pro 13" (M5) 52/52 unit + 6 UI pass (Bib Gourmand skips
  on iPad by design; launch 4.69 s at load 10). Earlier on the Duo: iPhone UI flow passes. All GA simulators deleted.
- Nothing committed or pushed; no repo, ASC or DNS action. Xcode.app and Xcode-beta.app are 27.1 (27A9269), Xcode 1.app 27.1
  (27A9275): check a public release before any archive.

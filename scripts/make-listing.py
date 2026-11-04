#!/usr/bin/env python3
"""Writes the App Store listing and the App Review reply from the build's own counts (playbook/site-numbers.json, which
scripts/make-site.py rewrites on every run), so the copy never drifts from the data. Ported from tn-eats (mi-eats lineage; modeled on wa-eats/playbook/06
and 13).

Usage (from ga-eats/): .venv/bin/python scripts/make-listing.py   (after make-site.py)
Writes playbook/06-app-store-listing.md, playbook/13-app-review-reply.md and playbook/app-store/listing.json (what
../scripts/asc_listing.py uploads once Nick creates the App Store Connect record and its FOLDERS line is added).
Checks before writing anything: Apple's length limits, no keyword repeating a name/subtitle word, no "best"/"top"/"#1", no price
claim outside the description's plain "free guide", the reply under 4,000 characters.
"""
import json, os, re, sys

ROOT = os.path.join(os.path.dirname(__file__), "..")
N = json.load(open(os.path.join(ROOT, "playbook", "site-numbers.json")))
R, T, LIC, HON, ALC = N["restaurants"], N["towns"], N["on_an_official_list"], N["honors"], N["serves_alcohol_state_license"]
MI, JBF = N["michelin"], N["james_beard"]
G = {k[6:]: v for k, v in N.items() if k.startswith("guide_") and isinstance(v, int)}
OLD = N["oldest"]
FLOOR = R // 1000 * 1000   # "23,000+": promo text and What's New outlive small data changes
SITE = "https://georgia.eatsranked.com/"   # until the CNAME resolves: https://nickstrom5.github.io/georgia-eats/
# the app's Home shows a hand-checked guide card only with three or more places (HomeView): the copy names only those
assert all(G[k] >= 3 for k in ("soul", "buford", "wings", "bbq", "lowcountry")), G

NAME = "Georgia Eats: Restaurants"
SUB = "Wings, Barbecue & Lowcountry"
# no word from the name or subtitle; towns and Atlanta's food words are the biggest search win (rotate after a month of App Store
# Connect search-term data)
KW = "atlanta,savannah,buford highway,soul food,lemon pepper,athens,augusta,macon,decatur,seafood,peach"
PROMO = (f"{G['wings']} lemon pepper wing spots, {G['buford']} Buford Highway kitchens, soul food and Lowcountry seafood, each checked "
         f"by hand. Plus {FLOOR:,}+ Georgia restaurants near you.")
WHATS_NEW = f"First release: lemon pepper wings, Buford Highway, soul food, Lowcountry seafood and {FLOOR:,}+ Georgia restaurants."

DESC = f"""Georgia's restaurants, from a ten-piece of Atlanta lemon pepper wings to oysters on the Savannah coast.

Georgia Eats is a free guide to eating in Georgia: {G['wings']} lemon pepper wing spots, {G['buford']} Buford Highway restaurants, {G['soul']} soul food and meat-and-three places, {G['lowcountry']} Lowcountry seafood restaurants and {G['bbq']} barbecue places we checked by hand, plus {R:,} restaurants, cafés, bars and bakeries in {T} towns, from Atlanta and Savannah to Athens, Augusta, Macon and Columbus. No account, no ads.

GEORGIA GUIDES
• Lemon Pepper Wings: Atlanta's own wing, from the Atlanta Journal-Constitution's 2026 lemon pepper taste test and other 2026 picks.
• Buford Highway: Korean barbecue, hand-pulled noodles, Malaysian, Filipino, Colombian and Mexican kitchens in Doraville.
• Meat-and-Threes & Soul Food: plate lunches and family-style tables, Mrs. Wilkes' and The Busy Bee among them.
• Lowcountry Seafood: oysters, shrimp and local fish from Savannah to Darien and Brunswick.
• Barbecue & Brunswick Stew: pork, ribs and the stew both Brunswicks claim.
• Oldest Places: {OLD} restaurants open at the same address since 1960 or earlier.
• MICHELIN & James Beard: the MICHELIN Guide's {MI.get('1 MICHELIN Star', 0)} one-star restaurants, {MI.get('Bib Gourmand', 0)} Bib Gourmands and Recommended places, and James Beard winners, nominees, semifinalists and America's Classics ({HON} places).

FIND IT FAST
• Sort by distance, or browse the map by guide.
• Search by name, town, street or dish: "buford hwy", "lemon pepper decatur".
• Filter by town or cuisine, show Bib Gourmands only, or hide chains.
• Save places, and find hand-checked places from iPhone search (Spotlight).

LIVE DETAILS FROM APPLE MAPS
Tap "Ratings, hours & photos" on any place to open Apple Maps' own place card, with current hours, photos, ratings and directions.

HOW THE LISTS ARE BUILT
Every guide place was checked by hand in October 2026 against a 2025 or 2026 source: the place's own site or menu, dated local news or the MICHELIN Guide. The rest come from Overture Maps open data, checked against the Georgia Department of Revenue's alcohol licenses, which also say which {ALC:,} places are licensed to serve alcohol. Each place links to the health department's own inspection search, where Georgia posts its A, B, C and U grades. Website links are checked too. Nothing is ranked by star ratings, and the app computes no grades. Newer restaurant data downloads from the Georgia Eats website when there is some.

PRIVATE BY DESIGN
No account, no tracking, no ads. Your location, if you share it, only sorts lists on your device. Saved places stay on your device.

Places open and close, so check before you go. Spot a mistake? Email nick@eatsranked.com.

An independent app, not affiliated with any restaurant, chain or government agency (including the State of Georgia, the Georgia Department of Revenue, the Georgia Department of Public Health, GNR Public Health and Fulton County), or with the MICHELIN Guide or the James Beard Foundation. MICHELIN and the MICHELIN Guide are trademarks of Michelin. James Beard Foundation and James Beard Award are trademarks of the James Beard Foundation. Place data from Overture Maps Foundation (CDLA Permissive 2.0) and others; sources and licenses are on the About tab."""

REPLY = f"""Thank you. Here is the information requested. A screen recording from an iPhone running the latest iOS, starting at launch, is attached.

1. Screen recording: attached. There is no account, login, user-generated content or paid content.

2. Purpose and audience: Georgia Eats is a free guide to restaurants in Georgia (the U.S. state). Its focus is the state's own food: {G['wings']} Atlanta lemon pepper wing spots, {G['buford']} Buford Highway restaurants, {G['soul']} soul food and meat-and-three places, {G['lowcountry']} Lowcountry seafood restaurants and {G['bbq']} barbecue places, each checked by hand in October 2026 against a 2025 or 2026 source, plus the MICHELIN Guide and James Beard honorees. It also lists {R:,} restaurants, cafés and bars statewide from open map data, checked against Georgia's state alcohol license list. It is for Georgia residents and visitors deciding where to eat, with no ads, account or tracking.

3. How to use it (no login, no setup, no sample files needed):
- Home → Lemon Pepper Wings (or Buford Highway, Meat-and-Threes & Soul Food, Barbecue & Brunswick Stew, Lowcountry Seafood, MICHELIN & James Beard, Oldest Places, Near Me) → tap any place.
- On a place, tap "Ratings, hours & photos" to open Apple Maps' own place card through MapKit. Directions, Call and Website are below it; further down, a link opens the Georgia Department of Public Health's inspection search in Safari.
- Search from the Home search box by name, town, street or dish ("buford hwy", "lemon pepper decatur").
- The Map tab shows each guide as pins. "My location" and the Nearest sort use location only if allowed, on the device.
- The heart saves a place on the device, under the Saved tab. The About tab lists the data sources, licenses and the independence statement.
- On iPad, a sidebar replaces the tabs; a place opens in the right-hand column.
- Location: if you're outside Georgia (as App Review usually is), the map says so and stays on Georgia, and distance sorting still works from where you are.
- "GA Eats" is the Home Screen name of "Georgia Eats: Restaurants".

4. External services and data:
- Apple MapKit: maps, local search to find a place's Apple Maps listing, and Apple's place card for live hours, photos and ratings.
- Core Location: optional, on-device only, for distance sorting.
- Core Spotlight: on-device indexing so places appear in iPhone search.
- Data updates: at most once a day, the app checks the Georgia Eats website (static files on GitHub Pages) for newer restaurant data and downloads it if there is some. The requests carry no identifiers or location.
- No backend, accounts, analytics, advertising, payments or AI services. The restaurant data is bundled in the app.
- Bundled data sources: Overture Maps Foundation open place data (CDLA Permissive 2.0 and others; license texts are in the app); the Georgia Department of Revenue's Active Alcohol Licenses report (a public record); MICHELIN Guide and James Beard Foundation honors (facts only); and our own research of public websites and local news. Inspection reports are not copied: each place links to the health department's own public search.
- The website with the privacy policy and support page is static and hosted on GitHub Pages: {SITE}

5. Regional differences: none. The content covers Georgia; the app is offered in the United States and works the same everywhere.

6. Regulated or protected material: the app is not in a regulated industry and includes no protected third-party material. The data is open-licensed or public record, with attribution and licenses on the About tab. Ratings, hours and photos are shown only inside Apple's own place card through MapKit; the app stores no ratings or reviews. The app shows no inspection scores and computes no grades. Every website link was checked before release, and adult venues are excluded. The app is independent and not affiliated with any restaurant, agency, the MICHELIN Guide or the James Beard Foundation.

Support: nick@eatsranked.com"""

# ---------------- checks (nothing is written unless all pass)
problems = []
for label, text, limit in (("name", NAME, 30), ("subtitle", SUB, 30), ("keywords", KW, 100), ("promotional text", PROMO, 170),
                           ("What's New", WHATS_NEW, 4000), ("description", DESC, 4000), ("review notes", REPLY, 4000)):
    if len(text) > limit:
        problems.append(f"{label}: {len(text)} characters, limit {limit}")
title_words = set(re.findall(r"[a-z]+", (NAME + " " + SUB).lower()))
for kw in KW.split(","):
    if kw != kw.strip() or not kw:
        problems.append(f"keyword {kw!r}: no spaces around commas, no empty entries")
    if set(kw.split()) & title_words:
        problems.append(f"keyword {kw!r} repeats a word from the name or subtitle")
for text, label in ((KW, "keywords"), (PROMO, "promotional text"), (SUB, "subtitle"), (WHATS_NEW, "What's New")):
    for bad in (r"\bbest\b", r"\btop\b", r"#1", r"\bfree\b", r"\bevery\b"):
        if re.search(bad, text, re.I):
            problems.append(f"{label}: contains {bad!r}")
if re.search(r"\bevery (?:restaurant|place)\b|\ball [\d,]+ ", DESC + REPLY, re.I):
    problems.append("description/reply: an 'every restaurant' or 'all N' claim the data can't back")
if problems:
    sys.exit("not written:\n  " + "\n  ".join(problems))

listing = {"bundleId": "com.georgiaeats.ios", "name": NAME, "subtitle": SUB, "privacyPolicyUrl": SITE + "privacy.html",
           "primaryCategory": "FOOD_AND_DRINK", "secondaryCategory": "TRAVEL", "description": DESC, "keywords": KW,
           "promotionalText": PROMO, "supportUrl": SITE, "marketingUrl": SITE, "reviewNotes": REPLY}
os.makedirs(os.path.join(ROOT, "playbook", "app-store"), exist_ok=True)
json.dump(listing, open(os.path.join(ROOT, "playbook", "app-store", "listing.json"), "w"), indent=1, ensure_ascii=False)

open(os.path.join(ROOT, "playbook", "06-app-store-listing.md"), "w").write(f"""# App Store listing (ASO)

Written by `scripts/make-listing.py` from `site-numbers.json` ({N['generated']}); re-run it after every data refresh, never hand-edit.
The machine copy is `app-store/listing.json` (read by `../scripts/asc_listing.py` once Nick creates the App Store Connect record and
adds `"com.georgiaeats.ios": "ga-eats"` to its FOLDERS). The URLs assume georgia.eatsranked.com is live; until Nick's CNAME
resolves, use https://nickstrom5.github.io/georgia-eats/.

## Name (30 max)
`{NAME}` ({len(NAME)})

## Subtitle (30 max)
`{SUB}` ({len(SUB)})

Together they index: georgia, eats, restaurants, wings, barbecue, lowcountry. Home Screen name: GA Eats. "Georgia" also matches the
country in App Store search (Tbilisi delivery apps), so the keywords carry Georgia towns and Atlanta's food words.

## Keywords (100 max)
`{KW}` ({len(KW)})

- No word repeats the name or subtitle; no trademarks (no Chick-fil-A, Waffle House, The Varsity, Vidalia, "Georgia Grown",
  "Explore Georgia"), no "best", "top" or "#1".
- Towns are the biggest win; Columbus, Marietta, Roswell, Alpharetta, Tybee and St. Simons didn't fit. Rotate them in after a month
  of App Store Connect search-term data. Apple's public search can't be used for this research (itunes.apple.com's robots.txt blocks Claude).

## Promotional text (170 max, editable any time without review)
`{PROMO}` ({len(PROMO)})

## Description ({len(DESC)} of 4,000)
```
{DESC}
```

## What's New (1.0)
`{WHATS_NEW}`

## Screenshots
Framed by `scripts/appstore-screenshots.py`: `app-store/iphone/` (8, 1320x2868, the 6.9" slot) and `app-store/ipad/` (6, 2064x2752, the
13" slot). Upload one file at a time in file order and check the order after a reload. No negative board appears in any image, and
captions name no award body.

## Category and age rating
Primary Food & Drink, secondary Travel. Age rating: alcohol references "Infrequent" (bars, alcohol licenses) → 13+; everything
else None/No. Pricing $0.00, available in the United States. Content rights: yes, third-party content, with the rights (open data, public
records, Apple's place card). Untick "Sign-in required".

## App Review
Reply and recording script: `13-app-review-reply.md`. Put the reply in App Review Information → Notes from the start.
""")

open(os.path.join(ROOT, "playbook", "13-app-review-reply.md"), "w").write(f"""# App Review: prepared before submitting (Guideline 2.1 "Information Needed")

Written by `scripts/make-listing.py` ({N['generated']}). Wisconsin's new-developer review asked for a screen recording from a physical
device, starting at launch, plus answers to six questions; Georgia Eats should expect the same. Put the reply below in **App Review
Information → Notes** from the start ({len(REPLY):,} of 4,000 characters), and record the video before submitting. If Apple raises
Guideline 4.3(a), answer with Georgia's own guides and sources (lemon pepper wings, Buford Highway, soul food, Lowcountry seafood,
the MICHELIN Guide American South, the Department of Revenue's alcohol licenses, DPH's inspection search and its A/B/C/U grades);
never compare with the other state apps in the Notes.

## Screen recording (Nick, on his iPhone, latest iOS, 60–120 seconds, no sound)

Install from TestFlight first (the internal tester's email must be the Apple ID under Settings › your name › Media & Purchases on the
phone, or TestFlight says "not available"). Record with Control Center → Screen Recording:

1. Start on the Home Screen and tap **GA Eats**. The recording must begin with the launch.
2. Home: scroll the cards a little.
3. Tap **Meat-and-Threes & Soul Food**, then **The Busy Bee**.
4. Tap **Ratings, hours & photos**; Apple's place card opens. Close it, then scroll to the Health inspections section.
5. Tap the **heart** (Save), then go back to Home.
6. Tap the search box and type `buford hwy`. Open one result.
7. Tap the **Map** tab, then **Georgia picks**, then a pin and its name.
8. Tap the **Saved** tab, where the saved place shows. Then tap **About** and scroll to the sources.

## Reply text

```
{REPLY}
```
""")
print(f"wrote listing.json, 06-app-store-listing.md, 13-app-review-reply.md | keywords {len(KW)}/100, promo {len(PROMO)}/170, "
      f"description {len(DESC):,}/4,000, reply {len(REPLY):,}/4,000")

# Georgia sources (checked 2026-10-26)

Every host below was robots-checked with `pipeline/check_sources.py` (ClaudeBot, Claude-User and anthropic-ai; RFC 9309 matcher; an
empty 202 counts as a bot check) in its own step, before any other request. User agent on every scripted request:
`GeorgiaEatsBuild/1.0 (+nick@eatsranked.com)`. Raw files are in `data/raw/official/` (git-ignored, never public).

Georgia publishes **no food-permit list and no current inspection data in bulk**. The one statewide official list we can read is
the Department of Revenue's alcohol licenses. Everything else statewide comes from map listings, honors and our own hand-checked
research.

## The official grade (shown nowhere as data; explained and linked)

- **Rule:** Ga. Comp. R. & Regs. 511-6-1-.10(l), "Grading Inspections": A = 90-100 ("food safety excellence"), B = 80-89
  ("satisfactory compliance"), C = 70-79 ("marginal compliance"), U = 69 or less ("unsatisfactory compliance"). Read in DPH's own
  rule PDF, "Georgia Food Service Rules and Regulations, Chapter 511-6-1 (Revised 2/2025)"
  (`dph.georgia.gov/document/document/envhealthfoodfoodservice-rulespdf/download`, 189 pages; rule .10 last revised "Filed January
  13, 2025; effective February 12, 2025").
- **The 2026 amendment:** DPH's notice of January 27, 2026 adopts the December 22, 2025 proposal (`dph.georgia.gov/node/61271`,
  effective February 26, 2026 per its notice). Both notices' documents answer 404 on dph.georgia.gov today; search summaries
  describe the change as bringing cottage food operators under the definition of a food service establishment. Nothing found
  touches the grade bands, so the bands above stand. The official rules site (`rules.sos.ga.gov`) robots-blocks ClaudeBot and
  was not read.
- Use in the products: the bands are explained in words with a link to the portal. No grade is computed, copied or shown.

## Official records

| Source | What | Terms | Cadence | Status |
|---|---|---|---|---|
| **Georgia Department of Revenue**, "Active Alcohol Licenses" (`dor.georgia.gov/active-alcohol-licenses`, file `alcohol-accounts-active-june-2026.xlsx`, page modified 2026-08-06) | 25,576 accounts (22,464 with a Georgia address): account id, commence date, name, one-line address, beer/wine/liquor flags, the local licensing city or county, license type. CONSUMPTION 8,112 (on the premises), RETAIL 13,488 (package: stores, and some restaurants' to-go licenses), BREWPUB 57, BREWERY 196, DISTILLERY 265, WINERY 152, FARMWINE 578, HOTEL 134, plus brokers, wholesalers, importers, shippers and events. The page says the report "reflects all active licenses issued and/or assigned numbers to entities pending issuance" (247 accounts commence after June 30, 2026). | Public record; no reuse terms stated | Quarterly | **used**: confirms listings (6,848 matched in the web build), "serves alcohol" (5,447 consumption + 7 brewpub + 89 maker licenses), and adds 609 on-premises license holders whose names say they're a place to eat or drink. Unknown is never "no": cities and counties license too, and the list carries pending licenses. Names are the license names: no holder field, so an LLC-only name is never shown (dropped when it's an added row). |
| Overture address points (Georgia) | 652,666 points, but only Atlanta, DeKalb and Athens-Clarke | CDLA-Permissive-2.0 | Monthly | placed 3,323 licenses by house number, street and zip |
| **US Census Bureau batch geocoder** (`geocoding.geo.census.gov/geocoder/locations/addressbatch`, Public_AR_Current) | Address to point | Public domain | — | placed 5,447 of the 6,257 food and maker licenses the address points couldn't (kept only when the match agrees with the record's zip or town); 810 unmatched |
| **Fulton County Board of Health**, "Food Service Inspections" (data.fultoncountyga.gov `w896-7wba`; violations `56iw-x8kz`) | 33,124 inspections of 6,340 permits, 2010-06-25 to 2022-01-12 (nearly all 2016-2021): facility, address, score, official letter grade, purpose. No coordinates in the export. | CC BY 4.0, "Fulton County Government" | Labeled daily, last updated 2022-02-21 | **calibration only**: 4,055 permits last inspected in 2020-2021. History, never shown as a current result |
| **Georgia DPH inspection portal** (`ga.healthinspections.us/stateofgeorgia/`, Tyler Technologies) | Every county but Gwinnett, Newton and Rockdale (DPH: "Gwinnett/Newton/Rockdale are not included in the state-wide search"); current reports with score and grade | No export, no reuse terms; a JavaScript app over an undocumented API | — | **not harvested.** No robots.txt (404). The home page answers 200 to curl and renders in a browser; places link to it (there is no stable per-place URL to test) |
| Cobb & Douglas Public Health | Links its own Tyler portal, `cobb.healthinspections.us` (robots: no file) | — | — | search only; no bulk data found |
| **GNR Public Health** (Gwinnett, Newton, Rockdale): `inspections.myhealthdepartment.com/gwinnett-ga` | Inspection portal | — | — | **not used**: the host answers our agent 403 at robots.txt (a bot check). `gnrhealth.com` (robots allow) is linked instead |
| DeKalb Public Health (`dekalbpublichealth.com`) | — | — | — | 403 bot check. The old `dekalbhealth.net` now redirects to a gambling site: added to `pipeline/website_blocklist.json`, never linked |
| Coastal (Chatham), North Central (Macon-Bibb), Northeast (Athens-Clarke) health districts | Their sites link the state portal | — | — | no bulk data. East Central (Augusta) and West Central (Columbus) sites didn't answer |
| Socrata catalog (`api.us.socrata.com`) | Searched "restaurant inspections", "food inspection" | — | — | no Georgia dataset besides Fulton's |
| Georgia Department of Agriculture food sales licenses | Grocery and retail food | — | — | not used: stores, not restaurants (per the prompt) |
| **Property values**: Fulton "Tax Parcels 2025" (`gisdata.fultoncountyga.gov`, robots Crawl-delay 60), Cobb assessor layer (`gis.cobbcounty.org`) | Parcel values | "As is", no open license | — | **not used** (no redistribution terms). Gwinnett's open parcels carry no values |

**Getting real inspection data.** DPH's inspections page says record requests go to the county environmental health office.
Georgia's Open Records Act (O.C.G.A. 50-18-70 et seq.) is open to any person. A request for a bulk extract is drafted in
`playbook/records-requests.md`; nothing is sent without Nick's yes. Until data arrives there are no inspection boards, and the
app and site say so plainly.

## Statewide base

| Source | What | Terms | Cadence | Rows |
|---|---|---|---|---|
| Overture Maps places `2026-10-21.0` (newest release) | Map listings, state and county outlines (land division areas, so the coast and the Savannah and Chattahoochee borders follow the shore) | CDLA-Permissive-2.0 / Apache-2.0 + Foursquare NOTICE | Monthly | 49,276 Georgia eating/drinking listings (`region = 'GA'`, 2,533 marked closed); 604,317 places in the state; 159 counties |
| UCSD Google Local 2021 (`meta-Georgia.json.gz`, mcauleylab.ucsd.edu, 37.2 MB) | 2021 ratings, reviews, price: **web leaderboard only, never the app** | research dataset | frozen Sep 2021 | 28,911 food listings (3,451 closed by 2021); 22,330 matched to Overture listings |
| BLS QCEW, private NAICS 722, 2026 Q1 (from the prompt) | 24,150 eating and drinking places | public | quarterly | benchmark: the app build keeps 23,299 restaurants, the web build 28,522 |

Spillover (Chattanooga's suburbs, North Augusta SC, Phenix City AL, Jacksonville's northern edge) is clipped three ways: Overture's
own `region = 'GA'`, a Georgia ZIP (300xx-319xx, 398xx-399xx), and the state outline with a 100 m buffer.

## Calibration (2026-10-26, `data/ga/calibration*.json`)

Two lists test the map listings. Fulton County's permits cover every kind of kitchen but are four to five years old, so they
favor listings of places that have been around; the DOR's on-premises licenses are current but only cover places that serve
alcohol, so their shares are floors for comparing kinds of listings, not rates of real restaurants. Statewide, the share Google
2021 still showed open is the third check.

| Kind of listing (app grouping) | Fulton, on a 2020-21 food permit | Statewide, on a DOR on-premises license | Open in Google 2021 (statewide) |
|---|---|---|---|
| Meta >= 0.95 | 50.2% of 2,774 | 19.2% of 18,644 | 70.6% of 18,646 |
| Meta 0.90-0.95 with a website | 24.0% of 425 | 9.7% of 3,769 | 45.8% of 3,770 |
| Meta 0.90-0.95, no website | 9.5% of 84 | 4.9% of 1,196 | 18.6% of 1,196 |
| Meta < 0.90 | 5.2% of 793 | 5.6% of 5,720 | 4.6% of 5,720 |
| Chain store lists (AllThePlaces, DAC) | 31.7% of 120 | 1.6% of 1,115 | 19.6% of 1,115 |
| BrightQuery >= 0.95 | 25.7% of 763 | 6.0% of 3,584 | 32.6% of 3,584 |
| Other sources (Foursquare, Microsoft, ...) | 18.9% of 2,457 | 2.7% of 12,540 | 25.8% of 12,541 |

Web grouping, Fulton: Meta + open in Google 2021 66.2%, Meta only 8.9%, Foursquare only 5.1%, BrightQuery only 10.3%, Microsoft
only 11.8%. Same order as Colorado, Texas, Idaho, Arizona and Tennessee, so the same keep rules: web = Meta and chain store lists
(plus official and hand-checked), minus what Google showed closed in 2021; app = Meta >= 0.95, Meta 0.90-0.95 with a website,
chain store lists, official, hand-checked. BrightQuery >= 0.95 matched Fulton's permits about as often as Meta 0.90-0.95 with a
website, but far less often statewide and in Google 2021, so it stays out. Coverage the other way: the open map listings hold
66.2% of the 6,856 placed on-premises license businesses and 55.5% of Fulton's 3,704 permits of 2020-21.

## Honors (data/research)

- **MICHELIN Guide American South 2026** (revealed 2026-10-21 in Nashville). guide.michelin.com answers our curl with an empty 202
  (an AWS WAF challenge, never retried); the Georgia list (`/us/en/georgia/restaurants`, 2 pages), its 1-star page and the
  restaurant pages for addresses were read through Claude's web fetcher on 2026-10-26, as Tennessee did. Georgia: **64**: 10 One
  Star (Atlas, Bacchanalia, Hayakawa, Lazy Betty, Mujō, O by Brush, Omakase Table, Spring in Marietta, and new: So. Fox in Atlanta
  and Uberto Restaurant in Gay, the first outside metro Atlanta), 12 Bib Gourmands (new: Summerland, Tipsy Thaiger in Roswell),
  42 Recommended. No Green Star icon on any Georgia card this year (Bacchanalia and The Chastain had one in 2025): none claimed.
  Atlanta Magazine (2026-10-22, robots allow) lists the drop-offs: Masterpiece (was Bib), Gunshow, Marcel, Ñàdair (closed), The
  White Bull; Superica and Table & Main moved from Bib to Recommended.
- **James Beard Foundation** (jamesbeard.org, robots allow): research in progress (`data/research/jbf.json`).

## Hosts that block us (recorded so nobody retries them)

guide.michelin.com (202 WAF challenge; read only through Claude's fetcher), inspections.myhealthdepartment.com (403),
dekalbpublichealth.com (403), rules.sos.ga.gov (robots disallow ClaudeBot), apps.apple.com (robots disallow all three agents),
www.atlantanewsfirst.com (robots disallow ClaudeBot, anthropic-ai), whois.com (bot check).

# App Review: prepared before submitting (Guideline 2.1 "Information Needed")

Written by `scripts/make-listing.py` (2026-10-28). Wisconsin's new-developer review asked for a screen recording from a physical
device, starting at launch, plus answers to six questions; Georgia Eats should expect the same. Put the reply below in **App Review
Information → Notes** from the start (3,988 of 4,000 characters), and record the video before submitting. If Apple raises
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
Thank you. Here is the information requested. A screen recording from an iPhone running the latest iOS, starting at launch, is attached.

1. Screen recording: attached. There is no account, login, user-generated content or paid content.

2. Purpose and audience: Georgia Eats is a free guide to restaurants in Georgia (the U.S. state). Its focus is the state's own food: 21 Atlanta lemon pepper wing spots, 9 Buford Highway restaurants, 5 soul food and meat-and-three places, 7 Lowcountry seafood restaurants and 3 barbecue places, each checked by hand in October 2026 against a 2025 or 2026 source, plus the MICHELIN Guide and James Beard honorees. It also lists 23,275 restaurants, cafés and bars statewide from open map data, checked against Georgia's state alcohol license list. It is for Georgia residents and visitors deciding where to eat, with no ads, account or tracking.

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
- The website with the privacy policy and support page is static and hosted on GitHub Pages: https://georgia.eatsranked.com/

5. Regional differences: none. The content covers Georgia; the app is offered in the United States and works the same everywhere.

6. Regulated or protected material: the app is not in a regulated industry and includes no protected third-party material. The data is open-licensed or public record, with attribution and licenses on the About tab. Ratings, hours and photos are shown only inside Apple's own place card through MapKit; the app stores no ratings or reviews. The app shows no inspection scores and computes no grades. Every website link was checked before release, and adult venues are excluded. The app is independent and not affiliated with any restaurant, agency, the MICHELIN Guide or the James Beard Foundation.

Support: nick@eatsranked.com
```

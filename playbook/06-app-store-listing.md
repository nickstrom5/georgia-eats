# App Store listing (ASO)

Written by `scripts/make-listing.py` from `site-numbers.json` (2026-10-28); re-run it after every data refresh, never hand-edit.
The machine copy is `app-store/listing.json` (read by `../scripts/asc_listing.py` once Nick creates the App Store Connect record and
adds `"com.georgiaeats.ios": "ga-eats"` to its FOLDERS). The URLs assume georgia.eatsranked.com is live; until Nick's CNAME
resolves, use https://nickstrom5.github.io/georgia-eats/.

## Name (30 max)
`Georgia Eats: Restaurants` (25)

## Subtitle (30 max)
`Wings, Barbecue & Lowcountry` (28)

Together they index: georgia, eats, restaurants, wings, barbecue, lowcountry. Home Screen name: GA Eats. "Georgia" also matches the
country in App Store search (Tbilisi delivery apps), so the keywords carry Georgia towns and Atlanta's food words.

## Keywords (100 max)
`atlanta,savannah,buford highway,soul food,lemon pepper,athens,augusta,macon,decatur,seafood,peach` (97)

- No word repeats the name or subtitle; no trademarks (no Chick-fil-A, Waffle House, The Varsity, Vidalia, "Georgia Grown",
  "Explore Georgia"), no "best", "top" or "#1".
- Towns are the biggest win; Columbus, Marietta, Roswell, Alpharetta, Tybee and St. Simons didn't fit. Rotate them in after a month
  of App Store Connect search-term data. Apple's public search can't be used for this research (itunes.apple.com's robots.txt blocks Claude).

## Promotional text (170 max, editable any time without review)
`21 lemon pepper wing spots, 9 Buford Highway kitchens, soul food and Lowcountry seafood, each checked by hand. Plus 23,000+ Georgia restaurants near you.` (153)

## Description (3204 of 4,000)
```
Georgia's restaurants, from a ten-piece of Atlanta lemon pepper wings to oysters on the Savannah coast.

Georgia Eats is a free guide to eating in Georgia: 21 lemon pepper wing spots, 9 Buford Highway restaurants, 5 soul food and meat-and-three places, 7 Lowcountry seafood restaurants and 3 barbecue places we checked by hand, plus 23,275 restaurants, cafés, bars and bakeries in 459 towns, from Atlanta and Savannah to Athens, Augusta, Macon and Columbus. No account, no ads.

GEORGIA GUIDES
• Lemon Pepper Wings: Atlanta's own wing, from the Atlanta Journal-Constitution's 2026 lemon pepper taste test and other 2026 picks.
• Buford Highway: Korean barbecue, hand-pulled noodles, Malaysian, Filipino, Colombian and Mexican kitchens in Doraville.
• Meat-and-Threes & Soul Food: plate lunches and family-style tables, Mrs. Wilkes' and The Busy Bee among them.
• Lowcountry Seafood: oysters, shrimp and local fish from Savannah to Darien and Brunswick.
• Barbecue & Brunswick Stew: pork, ribs and the stew both Brunswicks claim.
• Oldest Places: 7 restaurants open at the same address since 1960 or earlier.
• MICHELIN & James Beard: the MICHELIN Guide's 10 one-star restaurants, 12 Bib Gourmands and Recommended places, and James Beard winners, nominees, semifinalists and America's Classics (75 places).

FIND IT FAST
• Sort by distance, or browse the map by guide.
• Search by name, town, street or dish: "buford hwy", "lemon pepper decatur".
• Filter by town or cuisine, show Bib Gourmands only, or hide chains.
• Save places, and find hand-checked places from iPhone search (Spotlight).

LIVE DETAILS FROM APPLE MAPS
Tap "Ratings, hours & photos" on any place to open Apple Maps' own place card, with current hours, photos, ratings and directions.

HOW THE LISTS ARE BUILT
Every guide place was checked by hand in October 2026 against a 2025 or 2026 source: the place's own site or menu, dated local news or the MICHELIN Guide. The rest come from Overture Maps open data, checked against the Georgia Department of Revenue's alcohol licenses, which also say which 5,452 places are licensed to serve alcohol. Each place links to the health department's own inspection search, where Georgia posts its A, B, C and U grades. Website links are checked too. Nothing is ranked by star ratings, and the app computes no grades. Newer restaurant data downloads from the Georgia Eats website when there is some.

PRIVATE BY DESIGN
No account, no tracking, no ads. Your location, if you share it, only sorts lists on your device. Saved places stay on your device.

Places open and close, so check before you go. Spot a mistake? Email nick@eatsranked.com.

An independent app, not affiliated with any restaurant, chain or government agency (including the State of Georgia, the Georgia Department of Revenue, the Georgia Department of Public Health, GNR Public Health and Fulton County), or with the MICHELIN Guide or the James Beard Foundation. MICHELIN and the MICHELIN Guide are trademarks of Michelin. James Beard Foundation and James Beard Award are trademarks of the James Beard Foundation. Place data from Overture Maps Foundation (CDLA Permissive 2.0) and others; sources and licenses are on the About tab.
```

## What's New (1.0)
`First release: lemon pepper wings, Buford Highway, soul food, Lowcountry seafood and 23,000+ Georgia restaurants.`

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

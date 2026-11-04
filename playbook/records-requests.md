# Open Records requests to send (drafts for Nick; nothing has been sent)

All three are Nick's to send, from his own account, only if he wants them. Georgia's Open Records Act (O.C.G.A. 50-18-70 et seq.)
is open to any person, not only Georgia residents, so these can cite it. Agencies answer within three business days (with the
records or a timeline) and may charge for search and retrieval past the first quarter hour; each draft asks for an estimate first.

Why ask: Georgia publishes its inspection reports and official letter grades (A, B, C, U) only in search portals with no export
(`12-sources.md`). With a bulk extract the app could show each place's latest official grade, as the health department published
it, with its date and a link to the report, and compute nothing of its own. The app is free, with no ads, purchases or resale.

## 1. Georgia Department of Public Health, Environmental Health Section: statewide inspections
To: the Department's open records officer (Georgia Department of Public Health, 200 Piedmont Avenue SE, Atlanta, GA 30334; the
Environmental Health office is 404-657-6534). Confirm the current open-records address on dph.georgia.gov before sending.
Subject: Open Records Act request: food service inspection scores and grades (non-commercial restaurant guide)

> Hello. Under the Georgia Open Records Act, O.C.G.A. 50-18-70 et seq., I request an electronic copy (CSV or Excel, in whatever
> format the records are kept) of food service establishment inspections recorded in the Department's environmental health
> system for January 1, 2024 to the present, for every county the Department's inspection search covers, with these fields where
> they exist: permit number, establishment name, street address, city, ZIP, county, inspection date, inspection type or purpose
> (routine, follow-up and so on), score and letter grade. I don't need owner names, home addresses or violation narratives.
>
> I build Georgia Eats, a free restaurant guide for iPhone and the web, with no advertising, no purchases and no resale. Each place
> in it links to the Department's public inspection search today. With this extract we would show each place's latest score and
> grade exactly as the Department published it, with its date and a link to the full report, and compute no grade of our own.
>
> If there are fees, please send an estimate before any work begins. If some counties' records are held only by their county
> environmental health offices, please tell me which, and I'll ask them directly. Thank you.
> Nick Soderstrom, nick@eatsranked.com

## 2. GNR Public Health (Gwinnett, Newton and Rockdale counties): their inspections
To: GNR Public Health's open records contact (find it on gnrhealth.com before sending).
Subject: Open Records Act request: food service inspection scores and grades (non-commercial restaurant guide)

> Hello. Under the Georgia Open Records Act, O.C.G.A. 50-18-70 et seq., I request an electronic copy (CSV or Excel) of food service
> establishment inspections in Gwinnett, Newton and Rockdale counties from January 1, 2024 to the present, with permit number,
> establishment name, street address, city, ZIP, county, inspection date, inspection type, score and letter grade. I don't need
> owner names, home addresses or violation narratives.
>
> I build Georgia Eats, a free restaurant guide for iPhone and the web, with no advertising, no purchases and no resale. We would
> show each place's latest score and grade as GNR published it, with its date and a link to GNR's own report, and compute no grade
> of our own. If there are fees, please send an estimate first. Thank you.
> Nick Soderstrom, nick@eatsranked.com

## 3. (Optional) Fulton County Board of Health: the open dataset
Fulton County's "Food Service Inspections" dataset on data.fultoncountyga.gov (w896-7wba, CC BY 4.0) stopped on January 12, 2022.
Fulton is also in DPH's search, so request 1 covers it; ask Fulton only if DPH says county boards hold their own records.

> Hello. Fulton County's open data portal publishes "Food Service Inspections" (w896-7wba) under CC BY 4.0, but the set hasn't been
> updated since January 2022. Does the Board of Health plan to resume it? If not, under the Georgia Open Records Act I request an
> electronic copy of the same fields for inspections from January 13, 2022 to the present. Thank you.
> Nick Soderstrom, nick@eatsranked.com

When a file arrives, save it in `data/raw/official/manual/` and tell the ga-eats session: `pipeline/official.py` gets a loader for
it, the app shows the latest official grade only as the agency published it (with the date and a link to the report), and the
"Inspections" explainer page and About text change from "linked, not copied" to name the source and date.

"""Writes data/research/app/*.json (hand-checked Georgia guides) from the compact lists below. Ported from tn-eats.

Each entry cites the 2025-26 page that names it (robots-checked host: check_sources.py). Every page below is dated on its face, or is
the place's own current page. The address comes from the map listing we already hold for that name in that town (site/georgia.json),
never from memory; a name that isn't found exactly once in its town (or at the street number given) is left out and listed in
data/research/app/LEADS.md. A place the map data lacks is added only when the dated page prints its street address (ADDR).
Usage: ../.venv/bin/python build_research.py   (then georgia.py)"""
import json, os, re
from brands import brand_of
from common import norm_name
ROOT = os.path.join(os.path.dirname(__file__), "..")
R = os.path.join(ROOT, "data", "research")
d = json.load(open(os.path.join(ROOT, "site", "georgia.json")))
C, M = d["cols"], d["meta"]
norm = lambda s: re.sub(r"\s+", " ", re.sub(r"[^a-z0-9 ]", " ", (s or "").lower().replace("'", "").replace("’", ""))).strip()

# each dated on its face (read 2026-10-26)
AM_OLD = "https://www.atlantamagazine.com/dining-news/built-to-last-more-than-65-years-later-these-atlanta-restaurants-are-still-serving/"   # 2026-05-11
RD_DOR = "https://roughdraftatlanta.com/2025/04/11/marta-dining-guide-doraville-restaurants/"        # 2025-04-11, updated 2025-06-16
MI_GA = "https://guide.michelin.com/us/en/georgia/restaurants"                                       # the 2026 selection (2026-10-21)
AJC_LP = "https://www.ajc.com/food-and-dining/2026/03/if-youre-looking-for-atlantas-best-lemon-pepper-wings-weve-found-them/"   # 2026-03-27
AJC_WINGS = "https://www.ajc.com/food-and-dining/2026/06/7-metro-atlanta-wing-spots-to-try-from-hidden-gems-to-hibachi/"           # 2026-06-14
RESY_SAV = "https://blog.resy.com/guides/where-to-eat-in-savannah/"                                  # 2026-10-26
AJC_SAV_JAN = "https://www.ajc.com/food-and-dining/2026/01/a-new-live-fire-restaurant-a-celebration-of-brunswick-stew-and-more-from-savannahs-dining-scene/"   # 2026-01-06
AJC_SAV_JUN = "https://www.ajc.com/food-and-dining/2026/06/longtime-coastal-georgia-steakhouse-expands-and-more-from-savannahs-dining-scene/"   # 2026-06-02
GT_PEACH = "https://www.georgiatrend.com/2026/06/16/unofficial-guide-issue-6-16-eat-peaches-visit-athfest-whitewater-rafting-ponce-city-market/"   # 2026-06-16
GT_JUL = "https://www.georgiatrend.com/2026/07/14/unofficial-guide-issue-07-14-eat-visit-do-and-shop/"   # 2026-07-14
AJC_PH = "https://www.ajc.com/accessatl/2025/12/a-bustling-history-and-a-caring-neighborhood-your-city-guide-to-piedmont-heights/"   # 2025-12-10
FOX_DH = "https://fox5atlanta.com/news/chick-fil-a-dwarf-house-hapeville-landmark-celebrates-80-years"   # 2026-05-15
MRSW = "https://www.mrswilkes.com/"   # the restaurant's own page: family-style lunch, Mon-Fri, 107 W Jones St (2026-10)
WAC = "https://en.wikipedia.org/wiki/List_of_James_Beard_America%27s_Classics"

# (name as the source writes it, town, street number to pick the location (or None), note, founded, founded_note, [sources])
GUIDES = {
 "soul food": [
  ("The Busy Bee", "Atlanta", "810", "Soul food on MLK Jr. Drive since 1947: a MICHELIN Bib Gourmand and a James Beard America's Classic.", None, None, [AM_OLD, MI_GA, WAC]),
  ("Mary Mac's Tea Room", "Atlanta", "224", "Southern plates on Ponce de Leon Avenue, founded in 1945; reopened after a 2024 roof collapse.", 1945, "Founded on Ponce de Leon Avenue in 1945 (Atlanta Magazine, May 2026).", [AM_OLD]),
  ("Paschal's Restaurant", "Atlanta", "180", "Opened in 1947 in Sweet Auburn; now on Northside Drive.", None, None, [AM_OLD]),
  ("Twisted Soul Cookhouse & Pours", "Atlanta", "1133", "Chef Deborah VanTrece's modern soul food; MICHELIN Recommended.", None, None, [MI_GA]),
  ("Mrs. Wilkes Dining Room", "Savannah", "107", "Homestyle Southern cooking served family style at shared tables, weekday lunch only; a James Beard America's Classic.", 1943, "Sema Wilkes took over the boardinghouse in 1943 (the restaurant's own site).", [MRSW, WAC]),
 ],
 "buford highway": [
  ("Yokohama Sushi", "Doraville", "5412", "Sushi, hand rolls and kushiyaki on Buford Highway.", None, None, [RD_DOR]),
  ("Han Il Kwan", "Doraville", "5458", "Korean barbecue on Buford Highway; MICHELIN Recommended.", None, None, [RD_DOR, MI_GA]),
  ("El Rey Del Taco", "Doraville", "5288", "Mexican, known for its late-night hours.", None, None, [RD_DOR]),
  ("Las Delicias de la Abuela", "Doraville", "5600", "Colombian cooking on Buford Highway.", None, None, [RD_DOR]),
  ("LanZhou Ramen", "Doraville", "5231", "Hand-pulled noodles; MICHELIN Recommended.", None, None, [RD_DOR, MI_GA]),
  ("Java Saga", "Doraville", "5145", "Taiwanese fried chicken.", None, None, [RD_DOR]),
  ("Mamak", "Doraville", "5150", "Malaysian, in Asian Square.", None, None, [RD_DOR]),
  ("Kamayan ATL", "Doraville", "5150", "Filipino, in Asian Square; MICHELIN Recommended.", None, None, [MI_GA]),
  ("Woo Nam Jeong", "Doraville", "5953", "Korean stone-bowl cooking; MICHELIN Recommended.", None, None, [MI_GA]),
 ],
 "lemon pepper wings": [   # the AJC's March 2026 blind taste test of lemon pepper wings (finalists) and its June 2026 wing guide
  ("JR Crickets", "Atlanta", "129", "The AJC's 2026 lemon pepper taste-test winner (J.R. Crickets has locations across Atlanta).", None, None, [AJC_LP]),
  ("JR Crickets", "Smyrna", "4479", "J.R. Crickets, the AJC's 2026 lemon pepper taste-test winner.", None, None, [AJC_LP]),
  ("JR Crickets", "Lithonia", "2617", "J.R. Crickets, the AJC's 2026 lemon pepper taste-test winner.", None, None, [AJC_LP]),
  ("JR Crickets", "College Park", "3529", "J.R. Crickets, the AJC's 2026 lemon pepper taste-test winner.", None, None, [AJC_LP]),
  ("JR Crickets", "Atlanta", "4805", "J.R. Crickets, the AJC's 2026 lemon pepper taste-test winner.", None, None, [AJC_LP]),
  ("J.r. Crickets Union City", "Union City", "4550", "J.R. Crickets, the AJC's 2026 lemon pepper taste-test winner.", None, None, [AJC_LP]),
  ("J.R. Crickets Halftime", "Atlanta", "2348", "J.R. Crickets, the AJC's 2026 lemon pepper taste-test winner.", None, None, [AJC_LP]),
  ("J.R. Crickets McDonough", "McDonough", "1095", "J.R. Crickets, the AJC's 2026 lemon pepper taste-test winner.", None, None, [AJC_LP]),
  ("J.r Crickets At Lakewood", "Atlanta", "1959", "J.R. Crickets, the AJC's 2026 lemon pepper taste-test winner.", None, None, [AJC_LP]),
  ("G Town Wings & Fish", "Atlanta", "2084", "On Campbellton Road; a finalist in the AJC's 2026 lemon pepper taste test.", None, None, [AJC_LP]),
  ("Wing Factory", "Atlanta", "1100", "A finalist in the AJC's 2026 lemon pepper taste test.", None, None, [AJC_LP]),
  ("Wing Factory", "Atlanta", "4279", "A finalist in the AJC's 2026 lemon pepper taste test.", None, None, [AJC_LP]),
  ("International Cafe", "Brookhaven", "3066", "A finalist in the AJC's 2026 lemon pepper taste test.", None, None, [AJC_LP]),
  ("Hungry AF Decatur", "Decatur", "2701", "Hungry AF, a finalist in the AJC's 2026 lemon pepper taste test.", None, None, [AJC_LP]),
  ("Hungry AF Camp Creek", "East Point", "3650", "Hungry AF, a finalist in the AJC's 2026 lemon pepper taste test.", None, None, [AJC_LP]),
  ("Tandoori Pizza & Wing", "Atlanta", "1175", "A finalist in the AJC's 2026 lemon pepper taste test.", None, None, [AJC_LP]),
  ("Sunnyside Pizzeria", "Sandy Springs", "220", "A finalist in the AJC's 2026 lemon pepper taste test.", None, None, [AJC_LP]),
  ("The Local", "Atlanta", "758", "The Ponce de Leon bar the AJC calls a popular lemon pepper stop (2026).", None, None, [AJC_LP]),
  ("Wings On Wheat", "Jonesboro", "2779", "Honey lemon pepper ranch wings.", None, None, [AJC_WINGS]),
  ("Wings R Us", "Atlanta", "490", "A self-serve lemon pepper station.", None, None, [AJC_WINGS]),
  ("Buffalo Bar", "Atlanta", "1269", "Atlanta-style wings with hibachi; honey lemon pepper.", None, None, [AJC_WINGS]),
 ],
 "georgia bbq": [
  ("Heirloom Market BBQ", "Atlanta", "2243", "Korean-influenced smoked meats by Cumberland; MICHELIN Bib Gourmand.", None, None, [MI_GA]),
  ("Little Barn", "Lawrenceville", "60", "Barbecue and Brunswick stew.", None, None, [GT_JUL]),
  ("Fat Matt's Rib Shack", "Atlanta", "1811", "Ribs and pulled pork with Brunswick stew on the side; open since 1990.", None, None, [AJC_PH]),
 ],
 "lowcountry": [
  ("Brochu's Family Tradition", "Savannah", "2400", "Oysters (from Georgia farms) alongside the whole-chicken dinner.", None, None, [RESY_SAV]),
  ("Fishbar", "Savannah", "2218", "Live-fire seafood in Starland, opened December 2025: a raw bar, local line-caught fish and grilled Georgia shrimp.", None, None, [RESY_SAV, AJC_SAV_JAN]),
  ("The Grey", "Savannah", "109", "Mashama Bailey's seasonal menu with local seafood, in a 1938 Greyhound station.", None, None, [RESY_SAV]),
  ("Common Thread Savannah", "Savannah", "122", "Local seafood on a sharing menu in Starland.", None, None, [RESY_SAV]),
  ("Husk Savannah", "Savannah", "12", "Georgia seafood on a seasonal menu.", None, None, [RESY_SAV]),
  ("B&J's Steaks & Seafood", "Darien", None, "Shrimp bought from Shell Creek Seafood; the Darien original.", None, None, [AJC_SAV_JUN]),
  ("B&J's Steaks & Seafood", "Brunswick", None, "The second B&J's, opened in April 2026: a half-pound shrimp basket, fried, grilled, blackened or boiled.", None, None, [AJC_SAV_JUN]),
 ],
 "peach": [
  ("Lane Southern Orchards", "Fort Valley", None, "A peach orchard's cafe and bakery: peach cobbler, peach ice cream and pecan pie, with rocking chairs on the porch.", None, None, [GT_PEACH]),
 ],
 "georgia-born chain": [
  ("Chick-fil-A Dwarf House", "Hapeville", "461", "S. Truett Cathy's original 1946 diner, where the chicken sandwich began; still serving on the spot it opened.", 1946, "Opened in 1946 'in this very spot' (FOX 5 Atlanta, May 2026).", [FOX_DH]),
 ],
 "oldest": [   # a founding year the dated page ties to the place as it stands; moved places (The Colonnade, Paschal's, Henri's) are left out
  ("Atkins Park Restaurant", "Atlanta", "794", "A Virginia-Highland tavern; the original location is still the anchor.", 1922, "Opened in 1922 (Atlanta Magazine, May 2026).", [AM_OLD]),
  ("Majestic Diner", "Atlanta", "1031", "A 24-hour diner on Ponce de Leon Avenue.", 1929, "In the same space on Ponce de Leon Avenue since 1929 (Atlanta Magazine, May 2026).", [AM_OLD]),
  ("The White House Restaurant", "Atlanta", "3172", "A Buckhead breakfast-and-lunch fixture.", 1948, "A Buckhead fixture since 1948 (Atlanta Magazine, May 2026).", [AM_OLD]),
  ("The Silver Skillet", "Atlanta", "200", "A diner on 14th Street, largely unchanged.", 1956, "Opened in 1956 and largely unchanged since (Atlanta Magazine, May 2026).", [AM_OLD]),
  ("Chick-fil-A Dwarf House", "Hapeville", "461", "S. Truett Cathy's original diner, where the chicken sandwich began.", 1946, "Opened in 1946 'in this very spot' (FOX 5 Atlanta, May 2026).", [FOX_DH]),
 ],
}
# street addresses as the dated page prints them, for places the map data lacks
ADDR = {("Las Delicias de la Abuela", "Doraville"): "5600 Buford Hwy", ("Chick-fil-A Dwarf House", "Hapeville"): "461 N Central Ave",
        ("B&J's Steaks & Seafood", "Darien"): "901 North Way", ("B&J's Steaks & Seafood", "Brunswick"): "1600 Newcastle St"}
# cuisine checked by hand where the listing's guess is wrong (a "Tea Room" isn't a café; a Colombian kitchen isn't a bakery)
CUISINE = {("Mary Mac's Tea Room", "Atlanta"): "Soul & Southern", ("Las Delicias de la Abuela", "Doraville"): "Latin & Caribbean"}
KINDS = {"soul food": ["soul food"], "buford highway": ["buford highway"], "lemon pepper wings": ["lemon pepper wings"],
         "georgia bbq": ["georgia bbq"], "lowcountry": ["lowcountry"], "peach": ["peach"], "georgia-born chain": ["georgia-born chain"],
         "oldest": ["oldest"]}


def key(s):
    """The name key without a leading "the": "Varsity" is our "The Varsity"."""
    return re.sub(r"^the ", "", norm(s))


def find(name, town, num):
    k = key(name)
    hits = [i for i, n in enumerate(C["name"]) if C["city"][i] is not None and M["cities"][C["city"][i]] == town
            and (key(n) == k or key(n).startswith(k + " ") or k.startswith(key(n) + " ") or key(n).replace(" ", "") == k.replace(" ", "")
                 or (key(n).split()[:2] == k.split()[:2] and len(k.split()) >= 2))]
    if num:
        hits = [i for i in hits if (C["addr"][i] or "").split(" ")[0] == num]
    return hits


leads, n_out = [], {}
for kind, rows in GUIDES.items():
    out = []
    for name, town, num, note, founded, fnote, srcs in rows:
        hits = find(name, town, num)
        if not hits and (name, town) in ADDR:
            out.append({"name": name, "address": ADDR[(name, town)], "city": town, "zip": None, "kinds": KINDS[kind], "dishes": [], "note": note,
                        "founded": founded, "founded_note": fnote, "website": None, "open": True, "evidence_date": "2026-10",
                        "sources": srcs, "match_names": []} | ({"cuisine": CUISINE[(name, town)]} if (name, town) in CUISINE else {}))
            continue
        if len(hits) != 1:
            leads.append(f"- {kind}: {name} ({town}{', ' + num if num else ''}) — {len(hits)} matches in our data; not added"); continue
        i = hits[0]
        out.append({"name": C["name"][i], "address": C["addr"][i], "city": town, "zip": str(C["zip"][i]) if C["zip"][i] else None,
                    "kinds": KINDS[kind], "dishes": [], "note": note, "founded": founded, "founded_note": fnote, "website": None, "open": True,
                    "evidence_date": "2026-10", "sources": srcs, "match_names": [name.upper()] if norm(name) != norm(C["name"][i]) else []})
        if brand_of(norm_name(name)):   # a chain shows under its own spelling at every branch, whatever the listing says
            out[-1]["display"] = {"JR Crickets": "J.R. Crickets"}.get(brand_of(norm_name(name)), name)
        elif re.match(r"(?i)^j\.? ?r\.? crickets", name):
            out[-1]["display"] = "J.R. Crickets"
        if (name, town) in CUISINE:
            out[-1]["cuisine"] = CUISINE[(name, town)]
    fn = re.sub(r"[^a-z]+", "_", kind).strip("_")
    json.dump(out, open(f"{R}/app/{fn}.json", "w"), indent=1, ensure_ascii=False)
    n_out[kind] = len(out)

open(f"{R}/app/LEADS.md", "w").write("# Georgia research leads (not yet verified)\n\nWritten by pipeline/build_research.py.\n\n" + "\n".join(leads) + """

## Waiting for a 2025-26 source we may use
- The Varsity, 61 North Ave (1928, Atlanta Magazine May 2026 names the North Avenue original, but no street number is printed and our
  map data lacks it): thevarsity.com answered 429 once; read it for the address, then add it to oldest and Georgia-born chains.
- Matthews Cafeteria (Tucker, 1955; Atlanta Magazine May 2026): not in our map data; needs a page that prints the street address.
- Fox Bros. Bar-B-Q, Fresh Air Bar-B-Que (Jackson, 1929), Sprayberry's (Newnan, 1926), Southern Soul Barbeque (St. Simons), Wiley's
  (Savannah), Zombie Pig (Columbus), Old Brick Pit (Chamblee), Taylor'd Bar-B-Q (Avondale Estates): only pre-2025 or undated pages
  (Atlanta Magazine's "75 Best" list isn't dated on its face; goldenisles.com pages carry only a copyright year).
- Peach: Dickey Farms (Musella) and Pearson Farm (Fort Valley) are farm markets (Georgia Trend, June 2026): not restaurants, left out.
- Georgia-born chains: Zaxby's first store (Statesboro, 1990; zaxbys.com is a bot check), the Flying Biscuit's Candler Park original,
  Taco Mac's first location, Huddle House (Decatur, 1964): no 2025-26 page found yet.
- Lowcountry: Tybee (Sea Wolf, The Crab Shack, Bubba Gumbo's) and the Golden Isles (Georgia Sea Grill, Southern Soul, The Crab Trap)
  have only 2024 or undated pages so far; visittybee.com and visitsavannah.com answer with a bot check, wsav.com and wtoc.com
  robots-block Claude.
- Soul food: K&K Soul Food, Zion Delight, Q-Time, Gocha's Breakfast Bar, Auntie Vee's Kitchen (discoveratlanta.com answers Claude's
  fetcher 403, though its robots.txt allows; Atlanta Magazine's lists naming them are undated).
- Blocked or unusable hosts: discoveratlanta.com (403 to Claude's fetcher), exploregeorgia.org, visitsavannah.com, visittybee.com
  (bot checks), atlanta.eater.com, southernliving.com, gardenandgun.com, wabe.org, savannahnow.com, flagpole.com, wsav.com, wtoc.com,
  visitperry.com, restaurantinformer.com, atlantanewsfirst.com (robots), zaxbys.com (bot check).
""")
print(n_out, "| leads:", len(leads))
for l in leads: print(l)

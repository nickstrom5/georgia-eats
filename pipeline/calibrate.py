"""How often is a map listing a real food or drink business? Measured against Georgia's official lists -> data/ga/calibration*.json

Adapted from co-eats/pipeline/calibrate.py (via tx-eats, az-eats and tn-eats). Georgia has two lists to measure against:
- Statewide, the Department of Revenue's active alcohol licenses for consumption on the premises (and brewpubs), placed on a point.
  Only places that serve alcohol hold one (coffee shops, bakeries, most fast food don't), so the share of listings found on it is a
  floor for comparing kinds of listings with each other, not a rate of real restaurants. The other direction (licenses found among
  the open map listings) says how much of the state's licensed bar and restaurant trade the listings hold.
- Fulton County, the Board of Health's food service permits last inspected in 2020-2021 (the open dataset stops in January 2022):
  every kind of food service, but four to five years old, so it favors listings of places that have been around a while.
Statewide, the share Google's Sep 2021 snapshot showed open is the third check (Idaho's and Hawaii's method).
A match is the same business name nearby, or the same street address with a distinctive name word in common.
"""
import json
import numpy as np, pandas as pd
from shapely.geometry import shape, Point
from shapely import STRtree
from common import GA
from listings_util import official_match
import official

o = pd.read_pickle(f"{GA}/stage1.pkl")
F = pd.read_pickle(f"{GA}/official.pkl")
_CN = json.load(open(f"{GA}/ga_counties_detail.geojson"))
_NAMES = list(_CN)
_GEOMS = [shape(_CN[n]).buffer(0.0003) for n in _NAMES]
_TREE = STRtree(_GEOMS)


def county_of(la, lo):
    if la != la:
        return None
    p = Point(lo, la)
    for i in _TREE.query(p):
        if _GEOMS[i].contains(p):
            return _NAMES[i]
    return None


o["county"] = [county_of(la, lo) for la, lo in zip(o.lat, o.lon)]
F["county"] = [county_of(la, lo) for la, lo in zip(F.lat, F.lon)]
o.to_pickle(f"{GA}/stage1.pkl")
F.to_pickle(f"{GA}/official.pkl")
FUL = official.load_fulton()
base = ~o.j_junk & ~o.j_outside
print("listings with a county:", int(o.county.notna().sum()), "of", len(o), "| licenses placed:", int(F.lat.notna().sum()), "of", len(F))


def groups(L, app=False):
    s = L.src.fillna("none")
    if app:
        conf = L.confidence.fillna(0)
        has_web = L.n_web.fillna(0).astype(int) > 0
        return np.select([L.ov_closed | L.j_closedname, (s == "meta") & (conf >= 0.95), (s == "meta") & (conf >= 0.9) & has_web,
                          (s == "meta") & (conf >= 0.9), s.isin(["AllThePlaces", "DAC"]), (s == "BrightQuery") & (conf >= 0.95), s == "meta"],
                         ["closed per Overture/name", "meta_high", "meta_mid_web", "meta_mid_noweb", "brand_feed", "bq_high", "meta_low"],
                         "other_sources")
    return np.select([L.closed21, L.ov_closed, (s == "meta") & L.in21, s == "meta", s.isin(["AllThePlaces", "DAC"]) & L.in21,
                      s.isin(["AllThePlaces", "DAC"]), L.in21, s == "Foursquare", s == "BrightQuery", s == "Microsoft"],
                     ["Google 2021 says closed", "Overture says closed", "Meta + open in Google 2021", "Meta only",
                      "brand feed + Google 2021", "brand feed only", "Foursquare/BrightQuery/Microsoft + Google 2021",
                      "Foursquare only", "BrightQuery only", "Microsoft only"], "other")


def measure(label, L, R, store_web, store_app, by_county=True):
    L = L.reset_index(drop=True)
    R = R.reset_index(drop=True)
    m = {}
    if by_county:   # "100 Main St" is in dozens of towns: match inside one county
        for cty, idx in L.groupby("county").groups.items():
            Rc = R[R.county == cty]
            if not len(Rc):
                continue
            Lc = L.loc[idx].reset_index()
            for i, j in official_match(Lc, Rc.reset_index(drop=True)).items():
                m[int(Lc.at[i, "index"])] = int(Rc.index[j])
    else:
        m = official_match(L, R)
    L["hit"] = L.index.map(lambda i: i in m)
    for mode, store in ((False, store_web), (True, store_app)):
        L["grp"] = groups(L, mode)
        t = L.groupby("grp").agg(n=("id", "size"), official=("hit", "mean"), open21=("in21", "mean")).sort_values("n", ascending=False)
        print(f"\n== {label} ({'app grouping' if mode else 'web grouping'}): {len(L)} listings, {len(R)} official records")
        print(t.assign(official=(t.official * 100).round(1), open21=(t.open21 * 100).round(1)).to_string())
        store[label] = {"listings": int(len(L)), "official_records": int(len(R)),
                        "groups": {g: {"n": int(r.n), "official": round(float(r.official), 3)} for g, r in t.iterrows()}}
    keepish = ~(L.ov_closed | L.j_closedname | L.closed21)
    got = set(R.biz.iloc[[m[i] for i in L.index[keepish] if i in m]])
    Rr = R[R.kind.eq("food")].drop_duplicates("biz")
    cover = float(np.mean([b in got for b in Rr.biz])) if len(Rr) else None
    print(f"{label}: official food businesses found among open map listings: {cover * 100:.1f}% of {len(Rr)}")
    store_web[label]["coverage"] = round(cover, 3)
    store_web[label]["official_food"] = int(len(Rr))


res, app = {}, {}
on_prem = F[F.kind.eq("food") & F.lat.notna() & F.county.notna()]
measure("Georgia (DOR alcohol licenses for consumption on premises)", o[base & o.county.notna()], on_prem, res, app)
measure("Fulton County (food service permits inspected 2020-2021)", o[base & (o.county == "Fulton County")], FUL[FUL.kind.eq("food")], res, app,
        by_county=False)

# the share Google 2021 still showed open, statewide, per app group (a listing Google had in 2021 and didn't call closed)
L = o[base].copy()
L["grp"] = groups(L, True)
L["open21"] = L.in21 & ~L.closed21
g21 = L.groupby("grp").open21.agg(["size", "mean"])
print("\n== open in Google 2021 (statewide, app grouping)\n" + (g21.assign(mean=(g21["mean"] * 100).round(1))).to_string())
# the app ships no Google-derived number, so calibration_app.json leaves the 2021 share out (calibration.json, read only by the
# private leaderboard, keeps it), as in sc-eats

per = o[base & o.county.notna() & ~o.ov_closed & ~o.j_closedname].groupby("county").size()
print("\n== open, cleaned listings per county (top 15)\n" + per.sort_values(ascending=False).head(15).to_string())
json.dump({"areas": res, "per_county_listings": {c: int(n) for c, n in per.items()},
           "open_google_2021": {g: {"n": int(r["size"]), "share": round(float(r["mean"]), 3)} for g, r in g21.iterrows()}},
          open(f"{GA}/calibration.json", "w"), indent=1)
json.dump(app, open(f"{GA}/calibration_app.json", "w"), indent=1)

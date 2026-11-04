"""Official records for Georgia -> one table of licensed food and drink businesses.

Georgia publishes no food-permit list and no current inspection data in bulk: county environmental health offices inspect under
DPH's rules (Ga. Comp. R. & Regs. 511-6-1) and file reports in search-only portals (DPH's Tyler portal for 156 counties, GNR's
for Gwinnett, Newton and Rockdale), never harvested. The one statewide official list (playbook/12-sources.md):
- "dor": Georgia Department of Revenue, "Active Alcohol Licenses" (dor.georgia.gov/active-alcohol-licenses), a quarterly Excel
         report of every active state alcohol license, "issued and/or assigned numbers to entities pending issuance": account id,
         commence date, name, one-line address, beer/wine/liquor flags, the local licensing city or county, and the license type.
         CONSUMPTION (on the premises) and BREWPUB mean drinks are served there; RETAIL is package sales (stores, and some
         restaurants' to-go licenses); BREWERY, DISTILLERY, WINERY and FARMWINE are makers (with taprooms); the rest are wholesale,
         brokers, importers, shippers and events. Cities and counties issue their own local licenses too, so a place missing
         from the list is unknown, never "no". Public record, no reuse terms stated.

Fulton County's food service inspections (CC BY 4.0, 2016-2021, stopped 2022-01-12) are history only: calibrate.py reads them,
nothing here shows them.

load() returns: jur, lic (our id), name, keys (name keys), addr, city, zip, num, street, lat, lon, kind, active, ltype, sub.
kind: food (consumption on premises, brewpub) | maker (brewery, distillery, winery, farm winery) | retail (package) | other.
"""
import os, re, json, datetime
import numpy as np, pandas as pd
from common import norm_name, RAW, name_sim, _stems, GENERIC, canon_city

OFF = os.path.join(RAW, "official")
DIRS = {"N": "N", "S": "S", "E": "E", "W": "W", "NORTH": "N", "SOUTH": "S", "EAST": "E", "WEST": "W"}
TYPES = set("ST STREET AVE AV AVENUE BLVD BOULEVARD RD ROAD DR DRIVE LN LANE CT COURT PL PLACE PKWY PARKWAY TER TRL TRAIL WAY HWY CIR "
            "CIRCLE PLZ SQ MALL BND PASS XING RUN ROW WALK RDG LOOP FWY FREEWAY EXPY EXPRESSWAY PIKE PK PKE".split())


def road(a):
    """One spelling for numbered roads: 'US HIGHWAY 41' = 'US-41' = 'US 41'; 'STATE ROUTE 20' = 'SR 20' = 'GA-20' = 'SH 20';
    'N INTERSTATE 75' = 'I-75'; 'COUNTY ROAD 5' = 'CR 5'."""
    a = re.sub(r"(\d)\s*&\s*(\d)", r"\1-\2", a.upper())
    a = re.sub(r"\b(US|GA|SR|SH|CR|I|IH)-(\w)", r"\1 \2", a)
    a = re.sub(r"\b(?:INTERSTATE(?: HIGHWAY| HWY)?|IH|I H)\s*(?=\d)", "I ", a)
    a = re.sub(r"\b(?:US|U S)\s+(?:HIGHWAY|HWY)\b", "US", a)
    a = re.sub(r"\b(?:FARM[- ]TO[- ]MARKET(?: ROAD| RD)?|FARM (?:ROAD|RD)|F M)\b", "FM", a)
    a = re.sub(r"\b(?:RANCH[- ]TO[- ]MARKET(?: ROAD| RD)?|RANCH (?:ROAD|RD)|RR|RM)\b(?=\s*\d)", "RM", a)
    a = re.sub(r"\b(?:STATE (?:HIGHWAY|HWY|ROAD|RD|ROUTE|RTE)|SR|SH|GEORGIA (?:HIGHWAY|HWY|STATE (?:HIGHWAY|ROUTE))|GA (?:HIGHWAY|HWY)|GA)\b(?=\s*\d)", "SH", a)
    a = re.sub(r"\b(?:HISTORIC )?(?:ROUTE|RT|RTE) 66\b", "US 66", a)
    a = re.sub(r"\b(?:COUNTY (?:HIGHWAY|HWY|ROAD|RD)|CO RD|CTY (?:HWY|RD)|CR)\b", "CR", a)
    a = re.sub(r"\bHIGHWAY\b", "HWY", a)
    return re.sub(r"\b(US|SH|CR|HWY|FM|RM|I) (\w+)\s*-\s*\w+", r"\1 \2", a)


ORD = {"FIRST": "1ST", "SECOND": "2ND", "THIRD": "3RD", "FOURTH": "4TH", "FIFTH": "5TH", "SIXTH": "6TH", "SEVENTH": "7TH",
       "EIGHTH": "8TH", "NINTH": "9TH", "TENTH": "10TH", "ELEVENTH": "11TH", "TWELFTH": "12TH"}


def street_key(a):
    """'2505 Monroe St' -> ('2505', 'MONROE'); '1000 OSAGE STREET' -> ('1000', 'OSAGE'); 'E Colfax Ave' keeps 'COLFAX'."""
    if not isinstance(a, str):
        return None, None
    a = re.sub(r"[.,#]", " ", road(a))
    m = re.match(r"^\s*(\d+)[A-Z]?(?:\s*-\s*\d+[A-Z]?)?\s+(.*)$", a)
    if not m:
        return None, None
    words = [w for w in m.group(2).split() if w]
    if len(words) > 1 and words[0] in DIRS:
        words = words[1:]
    core = []
    for w in words:
        if w in TYPES and core:
            break
        core.append(w)
    core = [ORD.get(w, w) for w in core]
    return m.group(1), " ".join(core[:3]) or None


def street_compat(a, b):
    """Same street, or one is a whole-word prefix of the other: Boulder's 2025 set sometimes truncates ("1206 CENTAUR" = Centaur Village Dr)."""
    if not isinstance(a, str) or not isinstance(b, str) or not a or not b:
        return False
    return a == b or a.startswith(b + " ") or b.startswith(a + " ")


def street_nums(a):
    """'157-159 W Main St' -> {'157', '159'}; '2505 Monroe St' -> {'2505'}."""
    if not isinstance(a, str):
        return set()
    a = road(a)
    m = re.match(r"^\s*(\d+)[A-Z]?(?:\s*-\s*(\d+)[A-Z]?)?\s", a.upper() + " ")
    if not m:
        return set()
    lo = int(m.group(1)); hi = int(m.group(2)) if m.group(2) else lo
    if hi < lo:   # "1500-02"
        hi = int(str(lo)[: len(str(lo)) - len(m.group(2))] + m.group(2)) if m.group(2) else lo
    return {str(x) for x in range(lo, hi + 1, 2 if (hi - lo) % 2 == 0 else 1)} if 0 <= hi - lo <= 12 else {str(lo)}


def _names(*vals):
    out = []
    for v in vals:
        if not isinstance(v, str):
            continue
        v = re.sub(r"\s*\((?:MOBILE|MOBILE UNIT|COMMISSARY|CATERING|SPECIAL EVENT|SPEC EVENT|TEMP(?:ORARY)? EVENT|CP|INSIDE [^)]*)\)\s*$", "", v, flags=re.I)
        for part in re.split(r"\s*/\s*|\s+\bdba\b\s+|\s+&\s+(?=[A-Z][a-z])", v, flags=re.I):
            k = norm_name(re.sub(r"\b(?:LLC|INC|CORP|CORPORATION|LTD|CO)\b\.?", "", part, flags=re.I))
            if k and k not in out:
                out.append(k)
    return out





LIST_DATE = None   # set by load(): the quarter the DOR report covers
DOR_FILE = os.path.join(OFF, "dor", "alcohol-accounts-active-june-2026.xlsx")
DOR_REPORT = "June 2026"
DOR_PAGE = "https://dor.georgia.gov/active-alcohol-licenses"
KIND = {"CONSUMPTION": "food", "BREWPUB": "food", "BREWERY": "maker", "DISTILLERY": "maker", "WINERY": "maker", "FARMWINE": "maker",
        "RETAIL": "retail"}
LTYPE = {"CONSUMPTION": "Consumption on premises", "BREWPUB": "Brewpub", "BREWERY": "Brewery", "DISTILLERY": "Distillery",
         "WINERY": "Winery", "FARMWINE": "Farm winery", "RETAIL": "Package (retail)", "HOTEL": "Hotel in-room service",
         "WHOLESALER": "Wholesaler", "BROKER": "Broker", "IMPORTER": "Importer", "SPCORDSHPR": "Special order shipper"}


def liq_kind(t):
    """A license type as shown -> on-premises, maker or retail."""
    if not isinstance(t, str):
        return None
    return "onprem" if t.startswith(("Consumption", "Brewpub")) else "maker" if t in ("Brewery", "Distillery", "Winery", "Farm winery") \
        else "retail" if t.startswith("Package") else None


def _zip(z):
    z = re.sub(r"\D", "", str(int(z)) if isinstance(z, float) and z == z else str(z or ""))
    return z[:5] if len(z) >= 5 else ""


OTHER = re.compile(r"\b(?:SCHOOL|ELEMENTARY|ACADEMY|HOSPITAL|JAIL|DETENTION|SENIOR|NURSING|FOOD TRUCK|CATERING|CATERER|COMMISSARY|"
                   r"CONCESSION|CHURCH|PARISH|CAMP|CORRECTION(?:AL)?|CAMPUS|WAREHOUSE|COLLEGE|UNIVERSITY|DISTRIBUT\w*|WHOLESALE)\b", re.I)


def _row(jur, lic, name, addr, city, z, la, lo, kind, active=True, ltype=None, holder=None):
    num, st = street_key(addr)
    if kind == "food" and OTHER.search(name or ""):
        kind = "other"
    return {"jur": jur, "lic": lic, "name": name, "dba": name, "holder": holder, "keys": _names(name), "addr": addr, "city": city,
            "zip": _zip(z), "num": num, "street": st, "lat": la, "lon": lo, "kind": kind, "active": active, "ltype": ltype}


_TOWNS = None


def _towns():
    """Georgia's town names (the towns of Overture's Georgia places, and the address points' municipalities), longest first, for
    splitting the DOR's one-line addresses ("2790 LAWRENCEVILLE SUWANEE RD STE 130 SUWANEE GA 30024-2671")."""
    global _TOWNS
    if _TOWNS is None:
        import duckdb
        from common import GA
        rows = duckdb.connect().execute(f"""SELECT upper(t) FROM (SELECT city t FROM '{GA}/overture_ga_bbox.parquet' WHERE region = 'GA'
                                            UNION ALL SELECT muni FROM '{GA}/addresses_ga.parquet' WHERE state = 'GA')
                                            WHERE t IS NOT NULL GROUP BY 1 HAVING count(*) >= 3""").fetchall()
        _TOWNS = sorted({re.sub(r"^(?:CITY|TOWN) OF ", "", r[0]).strip() for r in rows if r[0] and re.fullmatch(r"[A-Z .'-]+", r[0])},
                        key=len, reverse=True)
    return _TOWNS


def split_addr(a):
    """'265 NEWTON BRIDGE RD ATHENS GA 30607-1145' -> ('265 NEWTON BRIDGE RD', 'ATHENS', '30607'); a town the list doesn't name stays None."""
    a = re.sub(r"\s+", " ", a or "").strip()
    m = re.match(r"^(.*?)\s+([A-Z]{2})\s+(\d{5})(?:-\d{4})?$", a)
    if not m:
        return a, None, ""
    rest, st, z = m.groups()
    if st != "GA":
        return rest, None, z
    for t in _towns():
        if rest.endswith(" " + t) and len(rest) > len(t) + 3:
            return rest[: -len(t) - 1].strip(), t, z
    return rest, None, z


def _addr(a):
    """'2790 LAWRENCEVILLE SUWANEE RD STE 130' -> '2790 Lawrenceville Suwanee Rd Ste 130'."""
    a = re.sub(r"\s+", " ", a or "").strip()
    return re.sub(r"\b([A-Z]{2,})\b", lambda m: m.group(1).title() if m.group(1) not in ("NE", "NW", "SE", "SW") else m.group(1), a)


def load_dor():
    global LIST_DATE
    d = pd.read_excel(DOR_FILE)
    LIST_DATE = DOR_REPORT
    rows = []
    for r in d.itertuples(index=False):
        lt = getattr(r, "_11")
        street, town, z = split_addr(getattr(r, "_4"))
        kind = KIND.get(lt, "other")
        x = _row("dor", f"dor-{int(r.ID):07d}", re.sub(r"\s+", " ", str(getattr(r, "_3") or "")).strip(), _addr(street),
                 canon_city(town.title()) if town else None, z, np.nan, np.nan, kind, active=True, ltype=LTYPE.get(lt, lt.title() if isinstance(lt, str) else lt))
        x["drinks"] = [w for w, f in (("beer", r.Beer), ("wine", r.Wine), ("liquor", r.Liquor)) if f == 1]
        cd = getattr(r, "_1")
        x["issued"] = cd.date().isoformat() if hasattr(cd, "date") else None
        x["local"] = (str(getattr(r, "_8") or "").title() or None) if isinstance(getattr(r, "_8"), str) else None
        x["out_of_state"] = not bool(re.search(r"\sGA\s+\d{5}", str(getattr(r, "_4") or "")))
        rows.append(x)
    df = pd.DataFrame(rows)
    return df[~df.out_of_state].reset_index(drop=True)


FULTON_FILE = os.path.join(OFF, "fulton", "inspections.json")
FULTON_ITEM = "https://data.fultoncountyga.gov/d/w896-7wba"


def load_fulton(since="2020-01-01"):
    """Fulton County Board of Health food service permits whose latest inspection is on or after `since` (CC BY 4.0, Fulton County
    Government; the dataset stopped on 2022-01-12): one row per permit, for calibration only. Scores and grades are never read."""
    d = pd.DataFrame(json.load(open(FULTON_FILE)))
    d["date"] = pd.to_datetime(d["date"])
    last = d.sort_values("date").groupby("permit_number").tail(1)
    last = last[last["date"] >= since]
    rows = []
    for r in last.itertuples(index=False):
        x = _row("ful", f"ful-{r.permit_number}", re.sub(r"\s+", " ", r.facility or "").strip(), _addr(r.address),
                 canon_city((r.city or "").strip().title()), r.zipcode, np.nan, np.nan, "food", ltype="Fulton food service permit")
        x["last"] = r.date.date().isoformat()
        rows.append(x)
    df = pd.DataFrame(rows)
    df["biz"] = np.arange(len(df)) + 10_000_000
    df["county"] = "Fulton County"
    return df


def load():
    df = load_dor()
    # one business can hold several records (consumption plus package at one address under one name): same address and a name in common
    df["biz"] = np.arange(len(df))
    town = df.city.fillna("").str.upper().str.strip()
    for num, g in df[df.num.notna() & df.street.notna()].groupby("num"):
        idx = list(g.index)
        if len(idx) < 2 or len(idx) > 400:
            continue
        for x in range(len(idx)):
            for y in range(x + 1, len(idx)):
                a, b = idx[x], idx[y]
                if not street_compat(df.at[a, "street"], df.at[b, "street"]):
                    continue
                if not ((df.at[a, "zip"] and df.at[a, "zip"] == df.at[b, "zip"]) or (town[a] and town[a] == town[b])):
                    continue
                ka, kb = df.at[a, "keys"], df.at[b, "keys"]
                if not ka or not kb:
                    continue
                if any(name_sim(p, q) >= 85 or ((_stems(p) - GENERIC) & (_stems(q) - GENERIC)) for p in ka for q in kb):
                    old, new = df.at[b, "biz"], df.at[a, "biz"]
                    df.loc[df.biz == old, "biz"] = new
    df["county"] = None   # set from the point (geocode_official.py, calibrate.py)
    return df

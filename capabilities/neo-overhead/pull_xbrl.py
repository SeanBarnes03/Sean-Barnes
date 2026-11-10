import json, gzip, sys, urllib.request, os
OUT = sys.argv[1]
UA = {"User-Agent": "ResearchClient research@example.org", "Accept-Encoding": "gzip"}
CIKS = {"NEO": 1077183, "DGX": 1022079, "LH": 920148, "MYGN": 899923, "EXAS": 1124140,
        "NTRA": 1604821, "VCYT": 1384101, "CSTL": 1447362, "FLGT": 1674930}
CONCEPTS = ["Revenues", "RevenueFromContractWithCustomerExcludingAssessedTax", "SellingGeneralAndAdministrativeExpense",
            "GeneralAndAdministrativeExpense", "SellingAndMarketingExpense", "MarketingAndAdvertisingExpense",
            "ShareBasedCompensation", "AllocatedShareBasedCompensationExpense", "AmortizationOfIntangibleAssets",
            "AccountsReceivableNetCurrent", "CostOfRevenue", "CostOfGoodsAndServicesSold", "ResearchAndDevelopmentExpense",
            "OperatingExpenses", "DepreciationDepletionAndAmortization", "Depreciation", "SellingExpense"]
res = {}
for t, c in CIKS.items():
    url = f"https://data.sec.gov/api/xbrl/companyfacts/CIK{c:010d}.json"
    raw = urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60).read()
    try:
        raw = gzip.decompress(raw)
    except OSError:
        pass
    d = json.loads(raw)
    gaap = d["facts"].get("us-gaap", {})
    res[t] = {}
    for k in CONCEPTS:
        if k not in gaap:
            continue
        for unit, vals in gaap[k]["units"].items():
            for v in vals:
                # FY2025 annual values from the FY2025 10-K
                if v.get("form") == "10-K" and v.get("fy") == 2025 and v.get("fp") == "FY":
                    if "start" in v and not v["start"].startswith("2025-01"):
                        continue
                    if v["end"] != "2025-12-31":
                        continue
                    res[t].setdefault(k, set()).add(v["val"])
    res[t] = {k: sorted(s) for k, s in res[t].items()}
json.dump(res, open(OUT, "w"), indent=1)
for t, r in res.items():
    print(t)
    for k, v in r.items():
        print("  ", k, [round(x / 1e6, 1) for x in v])

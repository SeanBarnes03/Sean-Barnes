"""Download FY2025 10-K text for oncology-dx peers with a separate pharma/biopharma revenue line."""
import json, gzip, sys, urllib.request, re, html, os
OUTDIR = sys.argv[1]
UA = {"User-Agent": "ResearchClient research@example.org", "Accept-Encoding": "gzip"}
TICK = {"GH": None, "TEM": None, "CAI": None, "PSNL": None}

def get(url):
    raw = urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=90).read()
    try:
        return gzip.decompress(raw)
    except OSError:
        return raw

tick = json.loads(get("https://www.sec.gov/files/company_tickers.json"))
for v in tick.values():
    if v["ticker"] in TICK:
        TICK[v["ticker"]] = v["cik_str"]
print(TICK)
for t, c in TICK.items():
    if not c:
        continue
    sub = json.loads(get(f"https://data.sec.gov/submissions/CIK{c:010d}.json"))["filings"]["recent"]
    try:
        i = next(i for i, f in enumerate(sub["form"]) if f == "10-K" and sub["reportDate"][i] == "2025-12-31")
    except StopIteration:
        print(t, "no FY2025 10-K"); continue
    url = f"https://www.sec.gov/Archives/edgar/data/{c}/{sub['accessionNumber'][i].replace('-', '')}/{sub['primaryDocument'][i]}"
    h = get(url).decode("utf-8", "ignore")
    h = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", h, flags=re.S | re.I)
    h = re.sub(r"</(p|div|tr|li|h\d)>", "\n", h, flags=re.I)
    h = re.sub(r"</t[dh]>", " | ", h, flags=re.I)
    h = html.unescape(re.sub(r"<[^>]+>", " ", h))
    h = re.sub(r"[ \t\xa0]+", " ", h); h = re.sub(r"\n\s*\n+", "\n", h)
    open(os.path.join(OUTDIR, f"{t}.txt"), "w").write(h)
    print(t, url, len(h))

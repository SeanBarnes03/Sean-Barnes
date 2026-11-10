"""Download each company's FY2025 10-K primary document (HTML) and save as plain text."""
import json, gzip, sys, urllib.request, re, html, os
OUTDIR = sys.argv[1]
UA = {"User-Agent": "ResearchClient research@example.org", "Accept-Encoding": "gzip"}
CIKS = {"MYGN": 899923, "EXAS": 1124140, "VCYT": 1384101, "CSTL": 1447362, "FLGT": 1674930,
        "NTRA": 1604821, "DGX": 1022079, "LH": 920148, "NEO24": 1077183}

def get(url):
    raw = urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=90).read()
    try:
        return gzip.decompress(raw)
    except OSError:
        return raw

for t, c in CIKS.items():
    sub = json.loads(get(f"https://data.sec.gov/submissions/CIK{c:010d}.json"))
    r = sub["filings"]["recent"]
    want = "2024-12-31" if t == "NEO24" else "2025-12-31"
    idx = next(i for i, f in enumerate(r["form"]) if f == "10-K" and r["reportDate"][i] == want)
    acc = r["accessionNumber"][idx].replace("-", "")
    url = f"https://www.sec.gov/Archives/edgar/data/{c}/{acc}/{r['primaryDocument'][idx]}"
    h = get(url).decode("utf-8", "ignore")
    txt = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", h, flags=re.S | re.I)
    txt = re.sub(r"</(p|div|tr|li|h\d)>", "\n", txt, flags=re.I)
    txt = re.sub(r"</t[dh]>", " | ", txt, flags=re.I)
    txt = re.sub(r"<[^>]+>", " ", txt)
    txt = html.unescape(txt)
    txt = re.sub(r"[ \t\xa0]+", " ", txt)
    txt = re.sub(r"\n\s*\n+", "\n", txt)
    open(os.path.join(OUTDIR, f"{t}.txt"), "w").write(txt)
    print(t, url, len(txt))

"""Find NeoGenomics quarterly earnings releases (8-K EX-99.1) on EDGAR and save them as text."""
import json, gzip, sys, urllib.request, re, html, os
OUTDIR = sys.argv[1]
UA = {"User-Agent": "ResearchClient research@example.org", "Accept-Encoding": "gzip"}

def get(url):
    raw = urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=90).read()
    try:
        return gzip.decompress(raw)
    except OSError:
        return raw

sub = json.loads(get("https://data.sec.gov/submissions/CIK0001077183.json"))["filings"]["recent"]
for i, form in enumerate(sub["form"]):
    if form != "8-K" or sub["filingDate"][i] < "2024-04-01":
        continue
    acc = sub["accessionNumber"][i].replace("-", "")
    idx = json.loads(get(f"https://www.sec.gov/Archives/edgar/data/1077183/{acc}/index.json"))
    for it in idx["directory"]["item"]:
        n = it["name"].lower()
        if "earningsrelea" in n and n.endswith(".htm"):
            h = get(f"https://www.sec.gov/Archives/edgar/data/1077183/{acc}/{it['name']}").decode("utf-8", "ignore")
            t = re.sub(r"</t[dh]>", " | ", h, flags=re.I)
            t = re.sub(r"</(p|div|tr)>", "\n", t, flags=re.I)
            t = html.unescape(re.sub(r"<[^>]+>", " ", t))
            t = re.sub(r"[ \t\xa0]+", " ", t)
            fn = os.path.join(OUTDIR, f"rel_{sub['filingDate'][i]}.txt")
            open(fn, "w").write(t)
            print(fn, it["name"])

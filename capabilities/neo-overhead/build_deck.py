"""Build the NEO overhead deep-dive deck (HTML), styled to match NEO_Cost_Breakdown_Savings_v2.

Run:  python3 build_deck.py   -> writes neo-overhead-deck.html next to this file
Then: node render.js <abs html> <abs pdf> <png dir>

v2: every figure is reported in a filing (10-K, proxy, earnings release) or is plain arithmetic on
reported figures. Sources for each number: data/neo-overhead-sources.md.
"""
from pathlib import Path
import math

OUT = Path(__file__).with_name("neo-overhead-deck.html")

# ---------- NeoGenomics FY2025, $M (FY2025 10-K unless noted) ----------
REV = 727.332
GA = 273.337
SM = 92.007
SBC_TOTAL = 41.316
SBC_GA, SBC_SM = 34.321, 3.089                # Note 9, stock-based compensation by line
DEP_GA, DEP_SM = 20.798, 0.091                # Note 5, depreciation by line
CASH_GA = 205.414                             # Note 17, "Other general and administrative"
AMORT_GA = round(GA - CASH_GA - SBC_GA - DEP_GA, 3)   # 12.804, remainder of the non-cash G&A
LIT, DEAL, CEO_T = 11.283, 7.266, 3.500       # adjusted EBITDA reconciliation
ONE_TIME = LIT + DEAL + CEO_T                 # 22.049
PATHLINE_GA = 4.7
EXEC, BOARD, AUDIT = 6.682, 0.618, 2.775        # 2026 proxy: NEO cash pay (salary+bonus+incentive+other), director cash fees, total Deloitte fees
CORE = CASH_GA - ONE_TIME - EXEC - BOARD      # 176.0
AR = 159.242
HEADCOUNT, HEADCOUNT_24 = 2500, 2200          # FTEs, FY2025 and FY2024 10-Ks
LEASE_COST = 9.551
NONCASH_GA = GA - CASH_GA

def pct(x, base=REV):
    return 100 * x / base

SGA_EX_AMORT = GA + SM - AMORT_GA             # 352.5 -> 48.5%
DAYS_NEO = AR / REV * 365                     # 79.9

# ---------- peers FY2025, $M (XBRL company facts + 10-K text) ----------
# name: (revenue, SG&A, S&M, G&A, stock pay total, stock pay in G&A, amortization inside G&A, receivables, group)
PEERS = {
    "Labcorp":            (13951.7, 2216.3, None, None, 125.8, None, 0, 2103.8, "r"),
    "Quest Diagnostics":  (11035.0, 1967.0, None, None, 88.0, None, 0, 1408.0, "r"),
    "Exact Sciences":     (3247.0, 1938.9, 1050.2, 888.7, 217.7, 96.3, 0, 298.7, "s"),
    "Natera":             (2306.1, 1177.3, None, None, 354.4, None, 0, 296.5, "s"),
    "Myriad Genetics":    (824.5, 537.6, 280.8, 256.8, 35.2, 22.1, 34.7, 115.3, "s"),
    "NeoGenomics":        (REV, GA + SM, SM, GA, SBC_TOTAL, SBC_GA, AMORT_GA, AR, "n"),
    "Veracyte":           (517.1, 211.0, 100.2, 110.8, 43.6, 25.1, 0, 44.7, "s"),
    "Castle Biosciences": (344.2, 229.3, 138.1, 91.2, 45.9, 17.4, 0, 43.4, "s"),
    "Fulgent Genetics":   (322.7, 160.1, 43.4, 116.7, 39.6, 16.5, 0, 84.8, "s"),
}
QUEST_DSO = 48  # Quest FY2025 10-K, as reported

def median(xs):
    xs = sorted(xs); n = len(xs)
    return xs[n // 2] if n % 2 else (xs[n // 2 - 1] + xs[n // 2]) / 2

MED_SGA = median([100 * v[1] / v[0] for v in PEERS.values() if v[8] == "s"])
MED_SM = median([100 * v[2] / v[0] for v in PEERS.values() if v[8] == "s" and v[2] is not None])
MED_GA = median([100 * v[3] / v[0] for v in PEERS.values() if v[8] == "s" and v[3] is not None])
MED_SBC = median([100 * v[4] / v[0] for v in PEERS.values() if v[8] == "s"])
MED_DAYS = median([v[7] / v[0] * 365 for v in PEERS.values() if v[8] == "s"])

def ga_like(v):
    """G&A excluding stock pay and any amortization booked in G&A, % of sales."""
    return 100 * (v[3] - v[5] - v[6]) / v[0]

LIKE = {k: ga_like(v) for k, v in PEERS.items() if v[3] is not None}
MED_LIKE = median([x for k, x in LIKE.items() if k != "NeoGenomics"])
NEO_LIKE = LIKE["NeoGenomics"]
NEO_LIKE_EX1 = 100 * (GA - SBC_GA - AMORT_GA - ONE_TIME) / REV
GAP_LIKE = NEO_LIKE - MED_LIKE
GAP_LIKE_EX1 = NEO_LIKE_EX1 - MED_LIKE

# ---------- palette (matches v2 deck) ----------
NAVY = "#14284B"; BLUE = "#3D5E98"; LBLUE = "#9DB0CF"; ORANGE = "#DB8A4B"
DORANGE = "#9E4F12"; GREEN = "#2E6B3A"; LGREEN = "#8FC08F"; RED = "#A52F22"; PINK = "#E7A79A"
GREY = "#6B7280"

CSS = f"""
@page {{ size: 1334px 750px; margin: 0; }}
* {{ box-sizing: border-box; }}
html, body {{ margin:0; padding:0; background:#F3F4F8; }}
body {{ font-family: 'DM Sans', 'Inter', system-ui, sans-serif; color:#1E2433; }}
.slide {{ width:1334px; height:750px; padding:28px 45px 0; position:relative; overflow:hidden;
         background:#F3F4F8; page-break-after:always; break-after:page; }}
.hdr {{ background:{NAVY}; border-radius:8px; padding:14px 30px 16px; text-align:center; color:#fff; }}
.hdr h1 {{ margin:0; font-size:40px; font-weight:800; letter-spacing:.5px; text-transform:uppercase; line-height:1.15; }}
.hdr p {{ margin:6px 0 0; font-size:18px; font-style:italic; color:#D6DDEB; }}
.tag {{ font-size:12px; margin:-4px 0 2px; font-weight:700; letter-spacing:1px;
        color:#AFC0DD; text-transform:uppercase; }}
.card {{ background:#fff; border-radius:8px; padding:16px 22px; box-shadow:0 1px 2px rgba(0,0,0,.05); }}
.card h3 {{ margin:0 0 10px; font-size:19px; font-weight:800; color:{NAVY}; text-transform:uppercase; letter-spacing:.3px; }}
.src {{ position:absolute; left:45px; right:45px; bottom:22px; font-size:14px; color:{GREY}; line-height:1.4; }}
.callout {{ background:#FDF3E6; border:1px solid #F1DCC0; border-radius:8px; padding:14px 22px; font-size:18px; line-height:1.4; }}
.callout.dark {{ background:{NAVY}; color:#fff; border:none; }}
.row {{ display:flex; gap:18px; }}
table.t {{ width:100%; border-collapse:collapse; font-size:16px; background:#fff; }}
table.t th {{ background:#E5EAF3; text-align:left; padding:8px 10px; font-weight:700; border:1px solid #CDD3DF; }}
table.t td {{ padding:6px 10px; border:1px solid #D9DEE8; vertical-align:top; }}
table.t td.n, table.t th.n {{ text-align:right; white-space:nowrap; }}
.hl td {{ background:#FBEDEA; font-weight:700; }}
.sub td {{ background:#F6F7FA; color:#4B5563; }}
.est {{ font-size:11px; font-weight:700; color:{DORANGE}; border:1px solid {ORANGE}; border-radius:3px;
        padding:0 3px; margin-left:4px; vertical-align:2px; }}
.wf {{ display:grid; grid-template-columns: 330px 1fr 90px; align-items:center; row-gap:6px; font-size:17px; }}
.wf .lab {{ padding-right:10px; }}
.wf .track {{ position:relative; height:26px; }}
.wf .bar {{ position:absolute; top:2px; height:22px; border-radius:3px; }}
.wf .zero {{ position:absolute; top:-4px; bottom:-4px; width:1.5px; background:#8A93A6; }}
.wf .val {{ text-align:right; font-weight:700; }}
.hatch {{ background-image: repeating-linear-gradient(45deg, rgba(255,255,255,.55) 0 4px, transparent 4px 9px); }}
.kpi {{ font-size:34px; font-weight:800; line-height:1.1; }}
.small {{ font-size:15px; color:#4B5563; line-height:1.4; }}
.cards3 {{ display:grid; grid-template-columns:repeat(3,1fr); gap:16px; }}
.topline {{ border-top:5px solid {BLUE}; }}
"""

def est():
    return '<span class="est">EST</span>'

def slide(title, subtitle, body, source, tag=""):
    t = f'<div class="tag">{tag}</div>' if tag else ""
    return f"""<section class="slide">
<div class="hdr">{t}<h1>{title}</h1><p>{subtitle}</p></div>
{body}
<div class="src">{source}</div></section>"""

def waterfall(rows, lo, hi, width_px=700, zero=True):
    """rows: (label, start, end, color, value_text, bold, hatch). Positions in data units."""
    span = hi - lo
    def x(v):
        return (v - lo) / span * 100
    out = ['<div class="wf">']
    for lab, s, e, col, vt, bold, hatch in rows:
        a, b = sorted((s, e))
        w = max(x(b) - x(a), 0.35)
        z = f'<div class="zero" style="left:{x(0):.2f}%"></div>' if zero and lo < 0 < hi or (zero and lo == 0) else ""
        fw = "font-weight:800;" if bold else ""
        h = " hatch" if hatch else ""
        out.append(f'<div class="lab" style="{fw}">{lab}</div>'
                   f'<div class="track">{z}<div class="bar{h}" style="left:{x(a):.2f}%;width:{w:.2f}%;background:{col}"></div></div>'
                   f'<div class="val" style="color:{col if col not in (LBLUE, LGREEN, PINK) else NAVY}">{vt}</div>')
    out.append("</div>")
    return "\n".join(out)

def hbars(rows, maxv, barw=520, labw=300, valfmt="{:.1f}", font=17, gap=8):
    out = [f'<div style="display:grid;grid-template-columns:{labw}px {barw}px 1fr;row-gap:{gap}px;align-items:center;font-size:{font}px">']
    for lab, v, col, extra in rows:
        w = v / maxv * barw
        out.append(f'<div>{lab}</div><div><div style="height:22px;width:{w:.1f}px;background:{col};border-radius:3px"></div></div>'
                   f'<div style="font-weight:700;padding-left:8px">{valfmt.format(v)}{extra}</div>')
    out.append("</div>")
    return "\n".join(out)

slides = []


def m(x, d=1):
    return f"{x:,.{d}f}"

slides = []
SRC_NEO = "NeoGenomics FY2025 10-K"
quest_sga = 100 * 1967.0 / 11035.0
neo_sga = pct(SGA_EX_AMORT)
gap_q = neo_sga - quest_sga
sbc_gap = pct(SBC_GA + SBC_SM) - 100 * 88.0 / 11035.0
one_pts = pct(ONE_TIME)
dep_pts = pct(DEP_GA + DEP_SM)
rem_q = gap_q - sbc_gap - one_pts - dep_pts
sbc_ga_share = 100 * SBC_GA / SBC_TOTAL
cash_free = (DAYS_NEO - QUEST_DSO) * REV / 365

# ================= 0. EXECUTIVE SUMMARY =================
body = f"""
<div class="row" style="margin-top:14px">
  <div class="card" style="flex:1;border-top:5px solid {NAVY};padding:14px 20px">
    <h3 style="margin-bottom:6px">1 &middot; What&rsquo;s in G&amp;A (slide 5)</h3>
    <ul class="small" style="font-size:16px;margin:0;padding-left:18px;line-height:1.45">
      <li><b>${m(GA)}M, {pct(GA):.1f}% of sales,</b> but only <b>${CORE:.0f}M is the day-to-day back office.</b></li>
      <li><b>${NONCASH_GA:.0f}M is non-cash:</b> stock pay ${SBC_GA:.1f}M, depreciation ${DEP_GA:.1f}M, amortization ${AMORT_GA:.1f}M.</li>
      <li><b>${ONE_TIME:.0f}M is &ldquo;one-time&rdquo;</b> (Natera litigation, Pathline deal, CEO change) and <b>${EXEC+BOARD:.1f}M</b> is executive and board cash pay.</li>
      <li>G&amp;A dollars rose 24% since 2021; the ratio fell only because sales rose 50%. People (+$11.5M) and software (+$8.0M) drove 2025.</li>
    </ul>
  </div>
  <div class="card" style="flex:1;border-top:5px solid {RED};padding:14px 20px">
    <h3 style="margin-bottom:6px">2 &middot; Why it&rsquo;s above peers (slide 6)</h3>
    <ul class="small" style="font-size:16px;margin:0;padding-left:18px;line-height:1.45">
      <li><b>vs. Quest: {gap_q:.1f} pts (${gap_q*REV/100:.0f}M).</b> {sbc_gap+one_pts+dep_pts:.1f} pts is stock pay, one-offs and depreciation; {rem_q:.1f} pts is recurring cash overhead.</li>
      <li><b>vs. specialty labs, total SG&amp;A is <i>low</i></b> ({pct(GA+SM):.1f}% vs. {MED_SGA:.1f}% median) because NEO spends little on selling.</li>
      <li><b>G&amp;A is the outlier:</b> {NEO_LIKE:.1f}% of sales like for like vs. a {MED_LIKE:.1f}% peer median: <b>{GAP_LIKE:.1f} pts, ~${GAP_LIKE*REV/100:.0f}M</b> (${GAP_LIKE_EX1*REV/100:.0f}M ex one-offs).</li>
      <li>Behind it: four acquisitions, <b>{DAYS_NEO:.0f} days to collect</b> vs. {QUEST_DSO} at Quest, {sbc_ga_share:.0f}% of stock pay landing in G&amp;A, CEO turnover, headcount +14% vs. sales +10%.</li>
    </ul>
  </div>
</div>
<div class="row" style="margin-top:14px">
  <div class="card" style="flex:1;border-top:5px solid {GREEN};text-align:center;padding:12px">
    <div class="kpi" style="color:{GREEN};font-size:30px">${GAP_LIKE_EX1*REV/100:.0f}&ndash;{GAP_LIKE*REV/100:.0f}M / yr</div>
    <div class="small">Recurring G&amp;A above the specialty median</div></div>
  <div class="card" style="flex:1;border-top:5px solid {BLUE};text-align:center;padding:12px">
    <div class="kpi" style="color:{BLUE};font-size:30px">~${cash_free:.0f}M cash</div>
    <div class="small">One-time, if NEO collected in {QUEST_DSO} days like Quest</div></div>
  <div class="card" style="flex:1;border-top:5px solid {ORANGE};text-align:center;padding:12px">
    <div class="kpi" style="color:{DORANGE};font-size:30px">~40% SG&amp;A</div>
    <div class="small">A credible goal; Quest&rsquo;s 18% is the wrong target</div></div>
</div>
<div class="callout dark" style="margin-top:14px"><b>Recommendation:</b> judge overhead against specialty labs, not Quest and Labcorp. Target G&amp;A ex stock pay
and amortization at ~24% of sales (from {NEO_LIKE:.1f}%) by finishing integration and fixing billing and collections. Hold G&amp;A dollars flat while sales grow, and
move stock pay out of G&amp;A-heavy grants. Protect the sales force: at {pct(SM):.1f}% of sales it is already lean.</div>"""
slides.append(slide("Executive summary", "NEO corporate overhead: what&rsquo;s in it and why it runs above peers &middot; FY2025, Q3 2026 where noted", body,
                    "All figures from FY2025 10-Ks, the 2026 proxy and earnings releases for NeoGenomics and eight peers, or simple arithmetic on them. "
                    "Like for like = G&amp;A excluding stock pay and amortization. Not investment advice."))

# ================= 1. G&A IN LAYERS =================
rows = [
    ("Reported G&amp;A", 0, GA, NAVY, m(GA), True, False),
    ("&minus; Stock-based pay", GA, GA - SBC_GA, LBLUE, f"&minus;{SBC_GA:.1f}", False, False),
    ("&minus; Depreciation", GA - SBC_GA, GA - SBC_GA - DEP_GA, LBLUE, f"&minus;{DEP_GA:.1f}", False, False),
    ("&minus; Amortization of acquired assets", GA - SBC_GA - DEP_GA, CASH_GA, LBLUE, f"&minus;{AMORT_GA:.1f}", False, False),
    ("= Cash G&amp;A", 0, CASH_GA, BLUE, m(CASH_GA), True, False),
    ("&minus; Patent litigation (Natera)", CASH_GA, CASH_GA - LIT, ORANGE, f"&minus;{LIT:.1f}", False, False),
    ("&minus; Deal costs (Pathline etc.)", CASH_GA - LIT, CASH_GA - LIT - DEAL, ORANGE, f"&minus;{DEAL:.1f}", False, False),
    ("&minus; CEO transition", CASH_GA - LIT - DEAL, CASH_GA - ONE_TIME, ORANGE, f"&minus;{CEO_T:.1f}", False, False),
    ("&minus; Exec cash pay &amp; board fees", CORE + EXEC + BOARD, CORE, GREEN, f"&minus;{EXEC+BOARD:.1f}", False, False),
    ("= Core back office", 0, CORE, NAVY, m(CORE), True, False),
]
body = f"""
<div class="row" style="margin-top:16px">
  <div class="card" style="flex:1.65">
    <h3>From ${GA:.0f}M reported to ${CORE:.0f}M of real back office ($M)</h3>
    {waterfall(rows, 0, 290)}
  </div>
  <div style="flex:1;display:flex;flex-direction:column;gap:14px">
    <div class="card"><h3>Share of sales</h3>
      {hbars([("Reported G&amp;A", pct(GA), NAVY, "%"), ("Cash G&amp;A", pct(CASH_GA), BLUE, "%"),
              ("Cash, ex one-offs", pct(CORE+EXEC+BOARD), BLUE, "%"), ("Core back office", pct(CORE), LBLUE, "%")],
             40, barw=170, labw=165, font=15, gap=6)}
    </div>
    <div class="card"><h3>Where each line comes from</h3>
      <div class="small">Stock pay and depreciation: 10-K tables by expense line (Notes 5 and 9). Cash G&amp;A $205.4M: segment note (Note 17).
      Amortization: the remainder. One-offs: adjusted EBITDA reconciliation. Exec and board cash: 2026 proxy.</div>
    </div>
  </div>
</div>
<div class="callout" style="margin-top:14px"><b>Over a third of &ldquo;overhead&rdquo; (${GA-CORE:.0f}M) is not back-office spending.</b> Cutting staff or vendors
can only reach the ${CORE:.0f}M core ({pct(CORE):.0f}% of sales), plus stock pay through policy.</div>"""
slides.append(slide("G&amp;A, peeled back in layers", f"FY2025 general &amp; administrative costs of ${GA:.1f}M &middot; non-cash, one-off, leadership and the real back office",
                    body, f"Sources: {SRC_NEO} (Note 5 depreciation by line, Note 9 stock pay by line, Note 17 segment expenses, adjusted EBITDA reconciliation); 2026 proxy statement.",
                    tag="Part 1 &middot; Slide 5 deep dive"))

# ================= 2. WHAT THE FILINGS SAY ABOUT THE CORE =================
named = [
    ("Pay &amp; benefits: executive, billing, finance, HR, IT, admin staff", "Largest component (10-K)", "+11.5"),
    ("Software development &amp; other technology", "Named", "+8.0"),
    ("Transaction costs", "Pathline $4.7M in G&amp;A", "+1.4"),
    ("Legal &amp; other professional fees", "Incl. Deloitte $2.8M (audit $2.0M)", "&minus;2.1"),
    ("Equipment maintenance", "Named", "&minus;1.8"),
    ("Travel", "Named", "&minus;1.3"),
    ("Amortization", "In G&amp;A: $12.8M", "&minus;1.0"),
    ("Facilities", "Rent company-wide $9.6M", "&minus;0.5"),
]
trs = "".join(f'<tr><td><b>{a}</b></td><td>{b}</td><td class="n" style="font-weight:700;color:{NAVY if c.startswith("+") else GREEN}">{c}</td></tr>' for a, b, c in named)
body = f"""
<div class="row" style="margin-top:16px">
  <div style="flex:1.6">
    <table class="t" style="font-size:16px">
      <tr><th>What the 10-K says is in G&amp;A</th><th>Dollar detail disclosed</th><th class="n">2025 change $M</th></tr>
      {trs}
      <tr class="hl"><td>Total change in G&amp;A</td><td>named items net +$14.2M; rest named items net to +$12.9Mminus;$0.6M</td><td class="n">+13.6</td></tr>
    </table>
  </div>
  <div style="flex:1;display:flex;flex-direction:column;gap:14px">
    <div class="card topline"><h3>Hard numbers</h3>
      <div class="small" style="font-size:15.5px"><b>Headcount:</b> ~{HEADCOUNT:,} FTEs, up from ~{HEADCOUNT_24:,} (+{100*(HEADCOUNT/HEADCOUNT_24-1):.0f}%) while sales grew 10%.<br>
      <b>People drive it:</b> pay was the largest rise in G&amp;A and in lab costs (+$34.8M together).<br>
      <b>Stock pay:</b> {sbc_ga_share:.0f}% of the company&rsquo;s ${SBC_TOTAL:.1f}M lands in G&amp;A.<br>
      <b>Rent:</b> ${LEASE_COST:.1f}M total operating lease cost, labs and offices combined.</div></div>
    <div class="card" style="border-top:5px solid {ORANGE}"><h3>Not disclosed</h3>
      <div class="small" style="font-size:15.5px">NEO does not report the ${CORE:.0f}M by function (billing vs. IT vs. finance). Splitting it needs internal
      data: G&amp;A by cost center, headcount by department and top vendors.</div></div>
  </div>
</div>"""
slides.append(slide(f"Inside the ${CORE:.0f}M back office", "What the filings disclose about the core, and how it moved in 2025",
                    body, f"Sources: {SRC_NEO} (G&amp;A description and MD&amp;A drivers, Pathline note, leases, human capital); FY2024 10-K (headcount); 2026 proxy (audit fees).",
                    tag="Part 1 &middot; Slide 5 deep dive"))

# ================= 3. TREND + 2025 DRIVERS =================
trend = [("2021", 484.3, 221.3), ("2022", 509.7, 243.4), ("2023", 591.6, 243.1), ("2024", 660.6, 259.7), ("2025", REV, GA)]
def col(top, h, lab, sub, fill):
    return (f'<div style="display:flex;flex-direction:column;align-items:center;justify-content:flex-end;height:290px;width:84px">'
            f'<div style="font-weight:800;font-size:17px;margin-bottom:4px">{top}</div><div style="width:56px;height:{h:.0f}px;{fill};border-radius:3px 3px 0 0"></div>'
            f'<div style="font-size:15px;margin-top:6px">{lab}</div><div style="font-size:13px;color:{GREY}">{sub}</div></div>')
tb = "".join(col(f"{g/r*100:.1f}%", g / r * 100 / 50 * 230, y, f"${g:.0f}M", f"background:{BLUE}") for y, r, g in trend)
tb += col("32.1%", 32.1 / 50 * 230, "Q3 26", "quarter", f"background:{LBLUE}")
tb += col("&lt;30%", 30 / 50 * 230, "2027 goal", "&nbsp;", f"border:2px dashed {BLUE}")
drv = [("Pay &amp; benefits", 11.5), ("Software &amp; technology", 8.0), ("Deal costs", 1.4), ("Facilities", -0.5),
       ("Amortization", -1.0), ("Travel", -1.3), ("Equipment maintenance", -1.8), ("Legal &amp; professional fees", -2.1)]
drows = [(n, 0, v, NAVY if v > 0 else LGREEN, f"{'+' if v>0 else '&minus;'}{abs(v):.1f}", False, False) for n, v in drv]
body = f"""
<div class="row" style="margin-top:16px">
  <div class="card" style="flex:1.15"><h3>G&amp;A as a share of sales</h3>
    <div style="display:flex;gap:6px;align-items:flex-end">{tb}</div>
    <div class="small" style="margin-top:8px">Dollars rose in three of four years ($221M &rarr; ${GA:.0f}M, +24%) but sales rose faster (+50%). The ratio fell because of growth, not cuts.</div>
  </div>
  <div class="card" style="flex:1"><h3>What moved G&amp;A in 2025 ($M, +$13.6M net)</h3>
    <div style="font-size:15px">{waterfall(drows, -4, 13).replace('grid-template-columns: 330px', 'grid-template-columns: 230px')}</div>
    <div class="small" style="margin-top:10px">People and systems added $19.5M; everything NEO cut came to $6.7M. Pathline integration put $4.7M into G&amp;A.</div>
  </div>
</div>"""
slides.append(slide("Overhead fell as a share, not in dollars", "G&amp;A FY2021&ndash;FY2025, Q3 2026, and what changed in 2025",
                    body, "Sources: NeoGenomics 10-Ks FY2021&ndash;FY2025 (via SEC XBRL company facts; FY2025 MD&amp;A G&amp;A drivers); Q3 2026 results. Q3 2026 is a single quarter.",
                    tag="Part 1 &middot; Slide 5 deep dive"))

# ================= 4. CONTROLLABILITY MAP =================
cm = [
    ("Core back office", CORE, "Cash", "Recurring", "Yes: process, systems, sourcing, location", GREEN),
    ("Stock-based pay", SBC_GA, "Non-cash", "Recurring", "Yes, by policy; lifts profit, not cash", ORANGE),
    ("Depreciation", DEP_GA, "Non-cash", "Recurring", "Only through lower capex over time", GREY),
    ("Amortization", AMORT_GA, "Non-cash", "Runs off", "No; set by past deals", GREY),
    ("Litigation, deals, CEO change", ONE_TIME, "Cash", "&ldquo;One-time&rdquo;", "Mostly rolled off ($2.6M Jan&ndash;Sep 2026), but $26M in 2024", ORANGE),
    ("Exec cash pay &amp; board", EXEC + BOARD, "Cash", "Recurring", "Small; governance, not savings", GREY),
]
trs = "".join(f'<tr><td><b>{n}</b></td><td class="n">{v:.1f}</td><td class="n">{pct(v):.1f}%</td><td>{c}</td><td>{r}</td>'
              f'<td style="color:{colr};font-weight:700">{a}</td></tr>' for n, v, c, r, a, colr in cm)
sbc_to_25 = SBC_TOTAL - 0.025 * REV
body = f"""
<div style="margin-top:16px">
<table class="t" style="font-size:17px">
<tr><th>Piece of G&amp;A</th><th class="n">$M</th><th class="n">% sales</th><th>Cash?</th><th>Recurs?</th><th>Can management cut it?</th></tr>
{trs}
<tr class="hl"><td>Total G&amp;A</td><td class="n">{GA:.1f}</td><td class="n">{pct(GA):.1f}%</td><td colspan="3"></td></tr>
</table></div>
<div class="row" style="margin-top:16px">
  <div class="card" style="flex:1;border-top:5px solid {GREEN}"><div class="kpi" style="color:{GREEN};font-size:28px">${CORE:.0f}M cash pool</div>
    <div class="small">Each 10% out of the core = ${CORE/10:.1f}M, {pct(CORE/10):.1f} pts of sales. The &lt;30% goal has to come from here.</div></div>
  <div class="card" style="flex:1;border-top:5px solid {ORANGE}"><div class="kpi" style="color:{DORANGE};font-size:28px">${SBC_TOTAL:.0f}M stock pay</div>
    <div class="small">Holding it to 2.5% of sales would cut ${sbc_to_25:.0f}M of reported cost, no cash.</div></div>
  <div class="card" style="flex:1;border-top:5px solid {GREY}"><div class="kpi" style="color:{GREY};font-size:28px">${DEP_GA+AMORT_GA:.0f}M fixed by the past</div>
    <div class="small">Depreciation and amortization; leave them out of savings targets.</div></div>
</div>"""
slides.append(slide("What management can actually cut", "Each piece of FY2025 G&amp;A by cash impact, recurrence and controllability",
                    body, "Sources: as slide 2; Q3 2026 investor presentation (one-off run-rate); FY2025 10-K (2024 one-offs: $26.1M). Savings figures are arithmetic, not company targets.",
                    tag="Part 1 &middot; Slide 5 deep dive"))

# ================= 5. PEER TABLE =================
def f(v):
    return "&ndash;" if v is None else f"{v:.1f}%"
trs = ""
for n, v in PEERS.items():
    r, sga, sm, ga, sbc, sbcga, am, ar, g = v
    cls = ' class="hl"' if g == "n" else (' class="sub"' if g == "r" else "")
    tagm = " <span style='color:#6B7280;font-weight:400'>(routine)</span>" if g == "r" else ""
    trs += (f'<tr{cls}><td>{n}{tagm}</td><td class="n">{r:,.0f}</td><td class="n">{f(100*sga/r)}</td><td class="n">{f(sm and 100*sm/r)}</td>'
            f'<td class="n">{f(ga and 100*ga/r)}</td><td class="n">{f(100*sbc/r)}</td><td class="n">{ar/r*365:.0f}</td></tr>')
body = f"""
<div class="row" style="margin-top:14px">
  <div style="flex:2.1"><table class="t" style="font-size:15.5px">
    <tr><th>Company (FY2025)</th><th class="n">Sales $M</th><th class="n">SG&amp;A</th><th class="n">Sales &amp; mktg</th><th class="n">G&amp;A</th><th class="n">Stock pay</th><th class="n">Days to collect</th></tr>
    {trs}
    <tr><td colspan="2"><b>Specialty median</b></td><td class="n"><b>{MED_SGA:.1f}%</b></td><td class="n"><b>{MED_SM:.1f}%</b></td><td class="n"><b>{MED_GA:.1f}%</b></td><td class="n"><b>{MED_SBC:.1f}%</b></td><td class="n"><b>{MED_DAYS:.0f}</b></td></tr>
  </table></div>
  <div style="flex:1;display:flex;flex-direction:column;gap:12px">
    <div class="card" style="border-top:5px solid {BLUE}"><h3 style="font-size:17px">vs. Quest &amp; Labcorp</h3><div class="small">NEO is ~3&times; on SG&amp;A. They run a
      high-volume routine-test model on 15&ndash;19&times; the sales.</div></div>
    <div class="card" style="border-top:5px solid {GREEN}"><h3 style="font-size:17px">vs. specialty labs</h3><div class="small">NEO&rsquo;s SG&amp;A is <b>below</b> the median: selling is
      {pct(SM):.1f}% vs. {MED_SM:.1f}%, and stock pay is {pct(SBC_TOTAL):.1f}% vs. {MED_SBC:.1f}%.</div></div>
    <div class="card" style="border-top:5px solid {RED}"><h3 style="font-size:17px">The real outliers</h3><div class="small">G&amp;A at {pct(GA):.1f}%, highest in the group,
      and {DAYS_NEO:.0f} days to collect vs. a {MED_DAYS:.0f}-day median. Only Fulgent is worse on either.</div></div>
  </div>
</div>"""
slides.append(slide("The gap depends on the yardstick", "Overhead as a share of sales, FY2025 &middot; routine labs vs. specialty and oncology labs",
                    body, "Sources: FY2025 10-Ks via SEC XBRL company facts (sales, SG&amp;A, S&amp;M, G&amp;A, stock pay, receivables). Days to collect = year-end receivables &divide; sales &times; 365 "
                    "(Quest reports 48). Myriad G&amp;A includes $34.7M amortization; NEO SG&amp;A is 48.5% ex amortization.",
                    tag="Part 2 &middot; Slide 6 gap analysis"))

# ================= 6. SCATTER =================
pts = [(n, v[0], 100 * v[3] / v[0], v[8]) for n, v in PEERS.items() if v[3] is not None]
W, H, L, T = 760, 380, 70, 20
def sx(r):
    return L + (math.log10(r) - math.log10(250)) / (math.log10(4000) - math.log10(250)) * (W - L - 30)
def sy(p):
    return T + (42 - p) / (42 - 15) * (H - T - 50)
svg = [f'<svg width="{W}" height="{H}" font-family="DM Sans, Inter, sans-serif">']
for p in (20, 25, 30, 35, 40):
    svg.append(f'<line x1="{L}" x2="{W-20}" y1="{sy(p):.1f}" y2="{sy(p):.1f}" stroke="#E3E7EF"/>'
               f'<text x="{L-10}" y="{sy(p)+5:.1f}" font-size="14" text-anchor="end" fill="{GREY}">{p}%</text>')
for r in (300, 500, 1000, 2000, 3000):
    svg.append(f'<text x="{sx(r):.1f}" y="{H-22}" font-size="14" text-anchor="middle" fill="{GREY}">${r:,}M</text>')
svg.append(f'<text x="{(W+L)/2}" y="{H-2}" font-size="14" text-anchor="middle" fill="{GREY}">FY2025 sales (log scale)</text>')
svg.append(f'<line x1="{L}" x2="{W-20}" y1="{sy(MED_GA):.1f}" y2="{sy(MED_GA):.1f}" stroke="{BLUE}" stroke-dasharray="6 5" stroke-width="1.5"/>'
           f'<text x="{sx(1150):.1f}" y="{sy(MED_GA)-8:.1f}" font-size="14" fill="{BLUE}">peer median {MED_GA:.1f}%</text>')
for n, r, ga, g in pts:
    c = RED if g == "n" else NAVY
    svg.append(f'<circle cx="{sx(r):.1f}" cy="{sy(ga):.1f}" r="{11 if g=="n" else 8}" fill="{c}"/>')
    dx, anchor, dy = 16, "start", 5
    if n == "Exact Sciences":
        dx, anchor, dy = 14, "end", 28
    svg.append(f'<text x="{sx(r)+dx:.1f}" y="{sy(ga)+dy:.1f}" font-size="16" font-weight="{800 if g=="n" else 600}" fill="{c}" text-anchor="{anchor}">{n} {ga:.1f}%</text>')
gap_rep = pct(GA) - MED_GA
svg.append(f'<line x1="{sx(REV):.1f}" x2="{sx(REV):.1f}" y1="{sy(pct(GA))+12:.1f}" y2="{sy(MED_GA):.1f}" stroke="{RED}" stroke-width="2" stroke-dasharray="3 3"/>'
           f'<text x="{sx(REV)-8:.1f}" y="{(sy(pct(GA))+sy(MED_GA))/2+4:.1f}" font-size="15" font-weight="700" fill="{RED}" text-anchor="end">+{gap_rep:.1f} pts &asymp; ${gap_rep*REV/100:.0f}M</text>')
svg.append("</svg>")
body = f"""
<div class="row" style="margin-top:16px">
  <div class="card" style="flex:1.7"><h3>G&amp;A as % of sales vs. company size, FY2025</h3>{''.join(svg)}</div>
  <div style="flex:1;display:flex;flex-direction:column;gap:14px">
    <div class="card topline"><h3>Scale doesn&rsquo;t explain it</h3><div class="small">Veracyte and Castle are <b>smaller</b> than NEO and run G&amp;A at
      21&ndash;27%. Myriad, a similar size, is {pct(GA)-31.1:.1f} pts lower even with $34.7M of amortization inside its G&amp;A.</div></div>
    <div class="card" style="border-top:5px solid {ORANGE}"><h3>Fulgent is the warning</h3><div class="small">The other lab grown by acquisition, with a
      pathology-services mix, sits next to NEO at 36.2% (31.7% without a $14.5M liability accrual).</div></div>
    <div class="card" style="border-top:5px solid {GREEN}"><h3>And it&rsquo;s moving</h3><div class="small">Q3 2026 G&amp;A was 32.1% of sales. Still above the
      median, but the gap has roughly halved.</div></div>
  </div>
</div>"""
slides.append(slide("NEO&rsquo;s G&amp;A is high for its size", "Specialty peers that report G&amp;A separately &middot; Quest and Labcorp report only combined SG&amp;A",
                    body, "Sources: FY2025 10-Ks (XBRL company facts; Fulgent 10-K litigation note). G&amp;A shown as reported, including each company&rsquo;s stock pay and any D&amp;A booked there.",
                    tag="Part 2 &middot; Slide 6 gap analysis"))

# ================= 7. BRIDGE TO QUEST (reported only) =================
rows = [("NeoGenomics SG&amp;A, ex amortization", 0, neo_sga, RED, f"{neo_sga:.1f}%", True, False)]
cur = neo_sga
for lab, v, c in [(f"Stock pay ({pct(SBC_GA+SBC_SM):.1f}% vs. Quest {100*88/11035:.1f}%)", sbc_gap, ORANGE),
                  ("&ldquo;One-time&rdquo; items in G&amp;A", one_pts, ORANGE),
                  ("Depreciation booked in NEO&rsquo;s SG&amp;A", dep_pts, ORANGE),
                  ("Recurring cash overhead gap", rem_q, BLUE)]:
    rows.append((lab, cur, cur - v, c, f"&minus;{v:.1f}", False, False)); cur -= v
rows.append(("Quest Diagnostics SG&amp;A", 0, quest_sga, NAVY, f"{quest_sga:.1f}%", True, False))
acct = sbc_gap + one_pts + dep_pts
body = f"""
<div class="row" style="margin-top:14px">
  <div class="card" style="flex:1.6"><h3>From {neo_sga:.1f}% to {quest_sga:.1f}% of sales, in points</h3>
    {waterfall(rows, 0, 52).replace('grid-template-columns: 330px', 'grid-template-columns: 350px')}
    <div class="small" style="margin-top:12px">Inside NEO&rsquo;s recurring cash SG&amp;A of {neo_sga-acct:.1f}%: selling {pct(SM-SBC_SM-DEP_SM):.1f}% and G&amp;A {pct(CORE+EXEC+BOARD):.1f}%.
    Quest reports SG&amp;A as one line, so its side can&rsquo;t be split the same way.</div>
  </div>
  <div style="flex:1;display:flex;flex-direction:column;gap:12px">
    <div class="card" style="border-top:5px solid {ORANGE}"><div class="kpi" style="color:{DORANGE};font-size:26px">{acct:.1f} pts &middot; ${acct*REV/100:.0f}M</div>
      <div class="small"><b>Accounting &amp; one-offs.</b> Real costs, but not a bloated back office. All three from NEO&rsquo;s 10-K.</div></div>
    <div class="card" style="border-top:5px solid {BLUE}"><div class="kpi" style="color:{BLUE};font-size:26px">{rem_q:.1f} pts &middot; ${rem_q*REV/100:.0f}M</div>
      <div class="small"><b>Recurring cash overhead.</b> A sales force Quest barely needs, collections that take {DAYS_NEO:.0f} days vs. {QUEST_DSO},
      fixed corporate costs on 1/15th the sales, and some plain excess.</div></div>
    <div class="card" style="border-top:5px solid {GREEN}"><div class="small"><b>How much of that is excess?</b> Quest can&rsquo;t say. Specialty peers can:
      like for like, NEO&rsquo;s G&amp;A is {GAP_LIKE_EX1:.1f}&ndash;{GAP_LIKE:.1f} pts high (next slide).</div></div>
  </div>
</div>"""
slides.append(slide("Why NEO spends 30 points more than Quest", f"Bridge of the {gap_q:.1f}-point SG&amp;A gap (${gap_q*REV/100:.0f}M a year at NEO&rsquo;s sales), FY2025",
                    body, f"Sources: {SRC_NEO} (stock pay and depreciation by line, one-offs); Quest FY2025 10-K (SG&amp;A $1,967M, stock pay $88M, DSO 48). "
                    "Quest&rsquo;s stock pay is total company and its own one-offs and depreciation in SG&amp;A aren&rsquo;t removed, so the orange bars are upper bounds.",
                    tag="Part 2 &middot; Slide 6 gap analysis"))

# ================= 8. LIKE-FOR-LIKE G&A =================
order = sorted(LIKE.items(), key=lambda kv: -kv[1])
bars = []
for n, v in order:
    c = RED if n == "NeoGenomics" else NAVY
    note = " (incl. $14.5M accrual)" if n == "Fulgent Genetics" else ""
    bars.append((f"<b>{n}</b>" if n == "NeoGenomics" else n + note, v, c, "%"))
bars.insert(1, ("NeoGenomics ex one-offs", NEO_LIKE_EX1, PINK, "%"))
body = f"""
<div class="row" style="margin-top:16px">
  <div class="card" style="flex:1.6"><h3>G&amp;A excluding stock pay and amortization, % of sales</h3>
    {hbars(bars, 34, barw=360, labw=330, font=16, gap=9)}
    <div class="small" style="margin-top:10px">Peer median: {MED_LIKE:.1f}%. Depreciation stays in for everyone (peers don&rsquo;t split it out);
    NEO&rsquo;s is {pct(DEP_GA):.1f} pts.</div>
  </div>
  <div style="flex:1;display:flex;flex-direction:column;gap:14px">
    <div class="card" style="border-top:5px solid {RED}"><div class="kpi" style="color:{RED}">{GAP_LIKE:.1f} pts &asymp; ${GAP_LIKE*REV/100:.0f}M</div>
      <div class="small">NEO vs. the specialty median, like for like.</div></div>
    <div class="card" style="border-top:5px solid {GREEN}"><div class="kpi" style="color:{GREEN}">{GAP_LIKE_EX1:.1f} pts &asymp; ${GAP_LIKE_EX1*REV/100:.0f}M</div>
      <div class="small">Same, after also removing NEO&rsquo;s ${ONE_TIME:.0f}M of 2025 one-offs. This is the recurring cash prize; the v2 deck sized it at ~$24M.</div></div>
  </div>
</div>
<div class="callout" style="margin-top:14px"><b>Target to hold management to:</b> G&amp;A ex stock pay and amortization at ~{MED_LIKE:.0f}% of sales
(from {NEO_LIKE:.1f}%). At 2025 sales that is ${GAP_LIKE_EX1*REV/100:.0f}&ndash;{GAP_LIKE*REV/100:.0f}M a year, and it gets easier if G&amp;A dollars stay flat as sales grow.</div>"""
slides.append(slide(f"Like for like, G&amp;A is {GAP_LIKE_EX1:.0f}&ndash;{GAP_LIKE:.0f} points high", "G&amp;A with stock pay and amortization removed for every company, FY2025",
                    body, "Sources: FY2025 10-Ks: stock pay in G&amp;A (NEO $34.3M, Exact $96.3M, Veracyte $25.1M, Myriad $22.1M, Castle $17.4M, Fulgent $16.5M); Myriad amortization in G&amp;A $34.7M; "
                    "NEO amortization in G&amp;A $12.8M; Fulgent accrual from its litigation note.",
                    tag="Part 2 &middot; Slide 6 gap analysis"))

# ================= 9. ROOT CAUSES =================
causes = [
    ("1 &middot; Four deals, never one company", ORANGE,
     "Clarient (2015), Genoptix (2018), Inivata (2021), Pathline (2025). Overlapping labs, systems and teams. &ldquo;One-time&rdquo; costs every year: $26.1M in 2024, $49.8M in 2025."),
    ("2 &middot; Slow collections", BLUE,
     f"{DAYS_NEO:.0f} days of sales sit in receivables vs. {QUEST_DSO} at Quest and a {MED_DAYS:.0f}-day specialty median. Only Fulgent (96) is worse. The billing staff who chase it sit in G&amp;A."),
    ("3 &middot; Stock pay concentrated in G&amp;A", ORANGE,
     f"Total stock pay is low for a specialty lab ({pct(SBC_TOTAL):.1f}% vs. {MED_SBC:.1f}% median), but {sbc_ga_share:.0f}% of it lands in G&amp;A vs. 38&ndash;63% at peers: it goes to executives and admin, not sales or R&amp;D."),
    ("4 &middot; Leadership churn", RED,
     "CEO changed in 2025 (Smith to Zook) and changes again in January 2027 (Stone). 2025 carried $3.5M of transition costs and $7.7M of pay to two departed executives."),
    ("5 &middot; Systems spend rising", BLUE,
     "Software &amp; technology +$8.0M in 2025, the biggest non-pay increase in G&amp;A. Running old and new platforms side by side costs double until the old ones are switched off."),
    ("6 &middot; People ahead of sales", RED,
     f"Headcount ~{HEADCOUNT_24:,} &rarr; ~{HEADCOUNT:,} (+14%) while sales grew 10%. G&amp;A pay +$11.5M. Plus $11.3M of Natera patent litigation to defend RaDaR."),
]
cards = "".join(f'<div class="card" style="border-top:5px solid {c}"><h3 style="font-size:18px;text-transform:none">{t}</h3><div class="small" style="font-size:15.5px">{d}</div></div>' for t, c, d in causes)
body = f"""
<div class="cards3" style="margin-top:16px">{cards}</div>
<div class="row" style="margin-top:14px;font-size:15px">
  <div style="display:flex;align-items:center;gap:8px"><span style="width:16px;height:16px;background:{ORANGE};display:inline-block;border-radius:3px"></span>Accounting / one-off</div>
  <div style="display:flex;align-items:center;gap:8px"><span style="width:16px;height:16px;background:{BLUE};display:inline-block;border-radius:3px"></span>Operations (fix over 1&ndash;2 years)</div>
  <div style="display:flex;align-items:center;gap:8px"><span style="width:16px;height:16px;background:{RED};display:inline-block;border-radius:3px"></span>Management choices (fix now)</div>
</div>"""
slides.append(slide("Six reasons NEO&rsquo;s overhead runs high", "What the filings show behind the gap",
                    body, "Sources: NeoGenomics FY2025 and FY2024 10-Ks (history, one-offs, drivers, receivables, headcount); 2026 proxy (pay: Smith $4.05M, Harris $3.69M); "
                    "Q3 2026 results (CEO succession); peer FY2025 10-Ks (receivables, stock pay by line).", tag="Part 2 &middot; Slide 6 gap analysis"))

# ================= 10. WHAT TO DO =================
flat = 100 * GA / (REV * 1.10)
acts = [
    ("Bring G&amp;A ex stock pay &amp; amortization to the peer median (~24%)", "Excess, integration", f"${GAP_LIKE_EX1*REV/100:.0f}&ndash;{GAP_LIKE*REV/100:.0f}M", "Cash", "Q3 2026 at 32.1% reported G&amp;A"),
    (f"Collect in {QUEST_DSO} days, not {DAYS_NEO:.0f}: automate prior auth, denials and appeals", "Billing", f"~${cash_free:.0f}M once", "Cash", "v2: ~93 days in 2026, worsening"),
    ("Finish integration: one lab system, one billing platform, close duplicate sites", "Integration", "Part of row 1", "Cash", "2 dry labs closed in 2026"),
    ("Hold stock pay to 2.5% of sales; shift grants away from G&amp;A", "Stock pay", f"${sbc_to_25:.0f}M profit", "Non-cash", "Not started"),
    ("Hold G&amp;A dollars flat while sales grow 10%", "Scale", f"{pct(GA)-flat:.1f} pts in a year", "Both", "Q3 2026 trend supports it"),
    ("Budget for deal and legal costs instead of calling them one-time", "One-offs", "Visibility", "&ndash;", "Rolled off in 2026"),
]
trs = "".join(f'<tr><td><b>{a}</b></td><td>{g}</td><td class="n">{v}</td><td>{c}</td><td>{s}</td></tr>' for a, g, v, c, s in acts)
body = f"""
<div style="margin-top:14px"><table class="t" style="font-size:16px">
<tr><th>Action</th><th>Gap it closes</th><th class="n">Size</th><th>Cash?</th><th>Status</th></tr>{trs}
</table></div>
<div class="row" style="margin-top:14px">
  <div class="callout dark" style="flex:1.6"><b>Prize: ${GAP_LIKE_EX1*REV/100:.0f}&ndash;{GAP_LIKE*REV/100:.0f}M a year of G&amp;A</b> plus ~${cash_free:.0f}M of cash
  from faster collection. That covers half to all of the remaining $49M operating loss.</div>
  <div class="callout" style="flex:1"><b>Don&rsquo;t chase Quest&rsquo;s 18%,</b> and don&rsquo;t cut the sales force: at {pct(SM):.1f}% of sales it is
  well under the {MED_SM:.0f}% specialty median.</div>
</div>"""
slides.append(slide("Closing the gap: what&rsquo;s worth doing", "Actions mapped to the gap they close &middot; sized from reported numbers",
                    body, "Sizes are arithmetic on FY2025 reported figures, not company targets; they overlap, so don&rsquo;t add them up. "
                    f"Cash from collections: {DAYS_NEO-QUEST_DSO:.0f} days &times; ${REV/365:.2f}M of sales a day. Not investment advice.",
                    tag="Part 2 &middot; Slide 6 gap analysis"))

# ================= 11. SOURCES =================
body = f"""
<div class="row" style="margin-top:16px;font-size:14.5px;line-height:1.45">
<div class="card" style="flex:1"><h3>NeoGenomics</h3>
<ul style="margin:0;padding-left:18px">
<li><b>FY2025 10-K</b> (filed 2026-02-17): income statement; MD&amp;A cost drivers; Note 5 depreciation by line (G&amp;A $20.8M); Note 9 stock pay by line (G&amp;A $34.3M, S&amp;M $3.1M);
Note 17 segment expenses (other G&amp;A $205.4M); adjusted EBITDA reconciliation (litigation $11.3M, deals $7.3M, CEO $3.5M); receivables $159.2M; leases; ~2,500 FTEs.</li>
<li><b>FY2024 10-K:</b> ~2,200 FTEs. <b>FY2021&ndash;2023 10-Ks:</b> sales and G&amp;A via SEC XBRL.</li>
<li><b>2026 proxy:</b> executive and board pay, audit fees. <b>Q3 2026 results:</b> G&amp;A 32.1%, CEO succession.</li>
</ul></div>
<div class="card" style="flex:1"><h3>Peers and method</h3>
<ul style="margin:0;padding-left:18px">
<li><b>FY2025 10-Ks</b> for Quest, Labcorp, Exact Sciences, Natera, Myriad, Veracyte, Castle and Fulgent: line items from SEC XBRL company facts; stock pay in G&amp;A,
Myriad amortization, Fulgent accrual and Quest DSO from the 10-K text.</li>
<li><b>Days to collect</b> = year-end receivables &divide; FY sales &times; 365, the same for every company.</li>
<li><b>Like for like G&amp;A</b> = G&amp;A less stock pay in G&amp;A, less amortization booked in G&amp;A.</li>
<li><b>Not public:</b> NEO&rsquo;s G&amp;A by function and Quest&rsquo;s split of SG&amp;A. Those would need internal data.</li>
</ul></div>
</div>"""
slides.append(slide("Sources and method", "Every figure is reported or is arithmetic on reported figures",
                    body, "Prepared November 2026. Full source list with links: data/neo-overhead-sources.md. Not investment advice."))

html = f"""<!doctype html><html><head><meta charset="utf-8"><title>NEO Overhead Deep Dive</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:ital,wght@0,400;0,600;0,700;0,800;1,400&display=swap" rel="stylesheet">
<style>{CSS}</style></head><body>
{''.join(slides)}
</body></html>"""
OUT.write_text(html, encoding="utf-8")
print(f"wrote {OUT} with {len(slides)} slides")

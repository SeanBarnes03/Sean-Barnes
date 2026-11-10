"""Build the NEO overhead deep-dive deck (HTML), styled to match NEO_Cost_Breakdown_Savings_v2.

Run:  python3 build_deck.py           -> writes neo-overhead-deck.html next to this file
Then: node render.js (or the Playwright snippet in README) -> PDF

All numbers live in the dicts below so every slide pulls from one place.
"E" in a label means the figure is our estimate; method is in the slide notes and sources.md.
"""
from pathlib import Path

OUT = Path(__file__).with_name("neo-overhead-deck.html")

# ---------- source numbers (FY2025, $M) ----------
REV = 727.3
GA = 273.3
SM = 92.0
AMORT_TOTAL, AMORT_COR = 31.8, 18.9
AMORT_GA = round(AMORT_TOTAL - AMORT_COR, 1)            # 12.9
SBC_TOTAL = 41.3
SBC_GA = 34.7      # est: 9M-2025 G&A share (27.9/33.3 = 84%) applied to FY total
SBC_SM = 2.9       # est: same method (2.3/33.3)
NONCASH_GA = 67.9  # v2 deck slide 5 (10-K segment note)
DEP_GA = round(NONCASH_GA - SBC_GA - AMORT_GA, 1)        # 20.3 residual
LIT, DEAL, CEO_T = 11.3, 7.3, 3.5
ONE_TIME = round(LIT + DEAL + CEO_T, 1)                  # 22.1
EXEC, BOARD = 6.7, 0.6
CORE = 176.0
assert abs(NONCASH_GA + ONE_TIME + EXEC + BOARD + CORE - GA) < 0.05

def pct(x, base=REV):
    return 100 * x / base

SGA_EX_AMORT = GA + SM - AMORT_GA                         # 352.4 -> 48.5%
CORE_CASH = CORE + EXEC + BOARD                           # 183.3 -> 25.2%

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

# ================= 0. ANSWER PAGE =================
body = f"""
<div class="row" style="margin-top:18px">
  <div class="card" style="flex:1;border-top:5px solid {NAVY}">
    <div class="kpi" style="color:{NAVY}">$273M of G&amp;A = 37.6% of sales</div>
    <div class="small" style="font-size:17px;margin-top:6px">Only <b>$176M</b> is the day-to-day back office (billing, IT, finance, HR, offices, fees). The rest is
    non-cash charges ($68M), &ldquo;one-time&rdquo; items ($22M) and leadership pay ($7M).</div>
  </div>
  <div class="card" style="flex:1;border-top:5px solid {RED}">
    <div class="kpi" style="color:{RED}">30.7 pts behind Quest</div>
    <div class="small" style="font-size:17px;margin-top:6px">SG&amp;A of 48.5% vs. 17.8% is a $223M/yr gap. About a third is accounting and one-offs; about half is
    the cost of being a small, specialty oncology lab. The rest is plain excess.</div>
  </div>
</div>
<div class="row" style="margin-top:16px">
  <div class="card" style="flex:1;border-top:5px solid {ORANGE}">
    <div class="kpi" style="color:{DORANGE}">Wrong yardstick, partly</div>
    <div class="small" style="font-size:17px;margin-top:6px">Against specialty labs (Myriad, Exact, Castle, Fulgent) NEO&rsquo;s total SG&amp;A is <i>low</i>. Its problem is
    G&amp;A alone: 37.6% vs. a 27.4% peer median, the highest of the group.</div>
  </div>
  <div class="card" style="flex:1;border-top:5px solid {GREEN}">
    <div class="kpi" style="color:{GREEN}">Real cash gap: ~4 pts, ~$27M</div>
    <div class="small" style="font-size:17px;margin-top:6px">Strip out stock pay, depreciation, amortization and one-offs and NEO&rsquo;s cash G&amp;A is 25.2% of sales,
    vs. ~21% at Castle. That is the size of the prize, and it matches the ~$24M in the v2 deck.</div>
  </div>
</div>
<div class="callout dark" style="margin-top:16px;display:flex;gap:14px;align-items:center">
  <div style="font-size:22px">&#9737;</div>
  <div><b>Why it&rsquo;s high:</b> four acquisitions never fully folded together, a billing operation that waits ~93 days to get paid
  (Quest: ~48), stock pay at 7&times; the big-lab rate, three CEOs in four years, and a public-company cost base spread over just $727M of sales.</div>
</div>"""
slides.append(slide("NEO&rsquo;s overhead: what&rsquo;s in it and why it&rsquo;s high",
                    "Deep dive on v2 slides 5 and 6 &middot; FY2025, updated with Q3 2026 where noted", body,
                    "Sources: NeoGenomics FY2025 10-K, Q3 2025 10-Q, Q4 2025 and Q3 2026 results; peer FY2025 10-Ks and earnings releases. "
                    "Figures marked EST are our estimates; method on each slide and in the notes page. Not investment advice."))

# ================= 1. G&A IN LAYERS =================
rows = [
    ("Reported G&amp;A", 0, GA, NAVY, f"{GA:.1f}", True, False),
    ("&minus; Stock-based pay " + est(), GA, GA - SBC_GA, LBLUE, f"&minus;{SBC_GA:.1f}", False, True),
    ("&minus; Depreciation " + est(), GA - SBC_GA, GA - SBC_GA - DEP_GA, LBLUE, f"&minus;{DEP_GA:.1f}", False, True),
    ("&minus; Amortization of acquired assets", GA - SBC_GA - DEP_GA, GA - NONCASH_GA, LBLUE, f"&minus;{AMORT_GA:.1f}", False, False),
    ("= Cash G&amp;A", 0, GA - NONCASH_GA, BLUE, f"{GA-NONCASH_GA:.1f}", True, False),
    ("&minus; Patent litigation (Natera)", GA - NONCASH_GA, GA - NONCASH_GA - LIT, ORANGE, f"&minus;{LIT:.1f}", False, False),
    ("&minus; Deal costs (Pathline etc.)", GA - NONCASH_GA - LIT, GA - NONCASH_GA - LIT - DEAL, ORANGE, f"&minus;{DEAL:.1f}", False, False),
    ("&minus; CEO transition", GA - NONCASH_GA - LIT - DEAL, GA - NONCASH_GA - ONE_TIME, ORANGE, f"&minus;{CEO_T:.1f}", False, False),
    ("&minus; Exec cash pay &amp; board fees", CORE + EXEC + BOARD, CORE, GREEN, f"&minus;{EXEC+BOARD:.1f}", False, False),
    ("= Core back office", 0, CORE, NAVY, f"{CORE:.1f}", True, False),
]
body = f"""
<div class="row" style="margin-top:16px">
  <div class="card" style="flex:1.65">
    <h3>From $273M reported to $176M of real back office ($M)</h3>
    {waterfall(rows, 0, 290)}
  </div>
  <div style="flex:1;display:flex;flex-direction:column;gap:14px">
    <div class="card"><h3>Share of sales</h3>
      {hbars([("Reported G&amp;A", pct(GA), NAVY, "%"), ("Cash G&amp;A", pct(GA-NONCASH_GA), BLUE, "%"),
              ("Cash, ex one-offs", pct(CORE_CASH), BLUE, "%"), ("Core back office", pct(CORE), LBLUE, "%")],
             40, barw=170, labw=165, font=15, gap=6)}
    </div>
    <div class="card"><h3>How the split was made</h3>
      <div class="small">Amortization: $31.8M total less $18.9M the 10-K puts in cost of revenue. Stock pay: G&amp;A was 84% of stock pay in
      Jan&ndash;Sep 2025 (10-Q), applied to the $41.3M year. Depreciation: the remainder of the $67.9M non-cash total.</div>
    </div>
  </div>
</div>
<div class="callout" style="margin-top:14px"><b>Over a third of &ldquo;overhead&rdquo; ($97M) is not back-office spending at all.</b> Cutting staff or vendors
can only reach the $176M core (24% of sales), plus stock pay through policy.</div>"""
slides.append(slide("G&amp;A, peeled back in layers", "FY2025 general &amp; administrative costs of $273.3M &middot; what is non-cash, what is one-off, what is the real back office",
                    body, "Sources: NeoGenomics FY2025 10-K (segment note, cost-of-revenue note, G&amp;A description, adjusted EBITDA reconciliation); Q3 2025 10-Q "
                    "(stock pay by line); 2026 proxy. Hatched bars = estimated split.", tag="Part 1 &middot; Slide 5 deep dive"))

# ================= 2. INSIDE THE $176M CORE =================
func = [
    ("Billing &amp; revenue cycle", 55, "45&ndash;62", "Coding, claims, prior authorization, appeals, collections and client services across a broad oncology menu and thousands of payers. Days to collect: ~93."),
    ("IT &amp; software", 45, "38&ndash;52", "IT staff, lab information system, ERP, cloud and licenses. Software &amp; tech rose $8.0M in 2025, the biggest non-pay increase."),
    ("Finance, HR, legal &amp; admin staff", 28, "22&ndash;34", "Accounting, FP&amp;A, tax, SOX, investor relations, HR/recruiting, in-house legal, compliance, procurement."),
    ("Professional fees", 16, "12&ndash;20", "Outside counsel (non-litigation), Deloitte audit ($2.8M), consultants, tax advisers. Down $2.1M in 2025."),
    ("Facilities, insurance &amp; office", 17, "13&ndash;20", "Fort Myers HQ and office space (part of $9.6M rent), D&amp;O and liability insurance, utilities."),
    ("Other admin", 15, "10&ndash;18", "Travel ($1.3M lower in 2025), recruiting, card-processing fees, equipment upkeep, dues and miscellaneous."),
]
assert sum(f[1] for f in func) == 176
trs = "".join(f'<tr><td><b>{n}</b></td><td class="n"><b>~{v}</b></td><td class="n">{r}</td><td class="n">{v/REV*100:.1f}%</td><td>{d}</td></tr>' for n, v, r, d in func)
body = f"""
<div class="row" style="margin-top:16px">
  <div style="flex:2.1">
    <table class="t">
      <tr><th>Function {est()}</th><th class="n">$M</th><th class="n">Range</th><th class="n">% sales</th><th>What&rsquo;s in it</th></tr>
      {trs}
      <tr class="hl"><td>Core back office</td><td class="n">176.0</td><td class="n">reported</td><td class="n">24.2%</td><td>10-K: pay for executive, billing, finance, HR, IT and admin staff, plus fees, facilities and systems</td></tr>
    </table>
  </div>
  <div style="flex:1;display:flex;flex-direction:column;gap:14px">
    <div class="card topline"><h3>Hard anchors</h3>
      <div class="small"><b>People ~60% of the core.</b> Pay &amp; benefits were the largest 2025 increase (+$11.5M) and 62% of lab-plus-overhead growth.<br><br>
      <b>Known:</b> audit $2.8M; rent $9.6M (labs + offices); 401(k) match $8.9M company-wide; headcount ~2,500 (+300 in 2025).</div></div>
    <div class="card" style="border-top:5px solid {ORANGE}"><h3>Why estimate?</h3>
      <div class="small">NEO reports G&amp;A as one line; the 10-K lists what is in it but not how much. Ranges are sized from the 10-K drivers,
      the disclosures at left, and typical cost shares for specialty labs. Use them to size work, not as fact.</div></div>
  </div>
</div>"""
slides.append(slide("Inside the $176M back office", "Indicative split by function, FY2025 &middot; NEO does not disclose this; ranges are our estimates",
                    body, "Sources: FY2025 10-K (G&amp;A description and drivers, leases, 401(k)); 2026 proxy (audit fees); headcount from company profile data "
                    "(Yahoo Finance/Fidelity, FY2025). Functional split estimated; see notes page.", tag="Part 1 &middot; Slide 5 deep dive"))

# ================= 3. TREND + 2025 DRIVERS =================
trend = [("2021", 484.3, 221), ("2022", 509.7, 243), ("2023", 591.6, 243), ("2024", 660.6, 259.7), ("2025", 727.3, 273.3)]
tb = ""
for y, r, g in trend:
    p = g / r * 100
    h = p / 50 * 230
    tb += f'<div style="display:flex;flex-direction:column;align-items:center;justify-content:flex-end;height:290px;width:84px">' \
          f'<div style="font-weight:800;font-size:17px;margin-bottom:4px">{p:.1f}%</div>' \
          f'<div style="width:56px;height:{h:.0f}px;background:{BLUE};border-radius:3px 3px 0 0"></div>' \
          f'<div style="font-size:15px;margin-top:6px">{y}</div><div style="font-size:13px;color:{GREY}">${g:.0f}M</div></div>'
tb += f'<div style="display:flex;flex-direction:column;align-items:center;justify-content:flex-end;height:290px;width:84px">' \
      f'<div style="font-weight:800;font-size:17px;margin-bottom:4px">32.1%</div>' \
      f'<div style="width:56px;height:{32.1/50*230:.0f}px;background:{LBLUE};border-radius:3px 3px 0 0"></div>' \
      f'<div style="font-size:15px;margin-top:6px">Q3 26</div><div style="font-size:13px;color:{GREY}">quarter</div></div>'
tb += f'<div style="display:flex;flex-direction:column;align-items:center;justify-content:flex-end;height:290px;width:84px">' \
      f'<div style="font-weight:800;font-size:17px;margin-bottom:4px">&lt;30%</div>' \
      f'<div style="width:56px;height:{30/50*230:.0f}px;border:2px dashed {BLUE};border-radius:3px 3px 0 0"></div>' \
      f'<div style="font-size:15px;margin-top:6px">2027 goal</div><div style="font-size:13px;color:{GREY}">&nbsp;</div></div>'
drv = [("Pay &amp; benefits", 11.5), ("Software &amp; technology", 8.0), ("Deal costs", 1.4), ("Facilities", -0.5),
       ("Amortization", -1.0), ("Travel", -1.3), ("Equipment maintenance", -1.8), ("Legal &amp; professional fees", -2.1)]
drows = [(n, 0, v, NAVY if v > 0 else LGREEN, f"{'+' if v>0 else '&minus;'}{abs(v):.1f}", False, False) for n, v in drv]
body = f"""
<div class="row" style="margin-top:16px">
  <div class="card" style="flex:1.15"><h3>G&amp;A as a share of sales</h3>
    <div style="display:flex;gap:6px;align-items:flex-end">{tb}</div>
    <div class="small" style="margin-top:8px">Dollars rose in three of four years ($221M &rarr; $273M, +24%) but sales rose faster (+50%). The ratio fell because of growth, not cuts.</div>
  </div>
  <div class="card" style="flex:1"><h3>What moved G&amp;A in 2025 ($M, +$13.6M net)</h3>
    <div style="font-size:15px">{waterfall(drows, -4, 13).replace('grid-template-columns: 330px', 'grid-template-columns: 230px')}</div>
    <div class="small" style="margin-top:10px">People and systems added $19.5M; everything NEO cut came to $6.7M. Pathline integration put $4.7M into G&amp;A.</div>
  </div>
</div>"""
slides.append(slide("Overhead fell as a share, not in dollars", "G&amp;A FY2021&ndash;FY2025, Q3 2026, and what changed in 2025",
                    body, "Sources: NeoGenomics 10-Ks FY2021&ndash;FY2025 (income statement; FY2025 MD&amp;A G&amp;A drivers); Q3 2026 results. Q3 2026 is a single quarter.",
                    tag="Part 1 &middot; Slide 5 deep dive"))

# ================= 4. CONTROLLABILITY MAP =================
cm = [
    ("Core back office", CORE, "Cash", "Recurring", "Yes: process, systems, sourcing, location", GREEN),
    ("Stock-based pay " + est(), SBC_GA, "Non-cash", "Recurring", "Yes, by policy; lifts profit, not cash", ORANGE),
    ("Depreciation " + est(), DEP_GA, "Non-cash", "Recurring", "Only through lower capex over time", GREY),
    ("Amortization", AMORT_GA, "Non-cash", "Runs off", "No; set by past deals", GREY),
    ("Litigation, deals, CEO change", ONE_TIME, "Cash", "&ldquo;One-time&rdquo;", "Mostly rolled off ($2.6M Jan&ndash;Sep 2026), but $26M in 2024", ORANGE),
    ("Exec cash pay &amp; board", EXEC + BOARD, "Cash", "Recurring", "Small; governance, not savings", GREY),
]
trs = "".join(f'<tr><td><b>{n}</b></td><td class="n">{v:.1f}</td><td class="n">{v/REV*100:.1f}%</td><td>{c}</td><td>{r}</td>'
              f'<td style="color:{col};font-weight:700">{a}</td></tr>' for n, v, c, r, a, col in cm)
body = f"""
<div style="margin-top:16px">
<table class="t" style="font-size:17px">
<tr><th>Piece of G&amp;A</th><th class="n">$M</th><th class="n">% sales</th><th>Cash?</th><th>Recurs?</th><th>Can management cut it?</th></tr>
{trs}
<tr class="hl"><td>Total G&amp;A</td><td class="n">{GA:.1f}</td><td class="n">{pct(GA):.1f}%</td><td colspan="3"></td></tr>
</table></div>
<div class="row" style="margin-top:16px">
  <div class="card" style="flex:1;border-top:5px solid {GREEN}"><div class="kpi" style="color:{GREEN};font-size:28px">$176M cash pool</div>
    <div class="small">10% out of the core = $17.6M, 2.4 pts of sales. This is where the &lt;30% goal has to come from.</div></div>
  <div class="card" style="flex:1;border-top:5px solid {ORANGE}"><div class="kpi" style="color:{DORANGE};font-size:28px">$35M stock pay</div>
    <div class="small">Bringing it to 2.5% of sales would add ~$17M of reported profit, no cash.</div></div>
  <div class="card" style="flex:1;border-top:5px solid {GREY}"><div class="kpi" style="color:{GREY};font-size:28px">$33M fixed by the past</div>
    <div class="small">Depreciation and amortization; ignore them when setting savings targets.</div></div>
</div>"""
slides.append(slide("What management can actually cut", "Each piece of FY2025 G&amp;A by cash impact, recurrence and controllability",
                    body, "Sources: as slide 2; Q3 2026 investor presentation (one-off run-rate); FY2024 10-K (2024 one-offs). Savings figures are simple arithmetic, not company targets.",
                    tag="Part 1 &middot; Slide 5 deep dive"))

# ================= 5. PEER TABLE =================
peers = [
    # name, rev, sga%, sm%, ga%, note, group
    ("Labcorp", 13951.7, 15.9, None, None, "SG&amp;A one line", "r"),
    ("Quest Diagnostics", 11035, 17.8, None, None, "SG&amp;A one line", "r"),
    ("Exact Sciences", 3250, 59.7, 32.3, 27.4, "", "s"),
    ("Natera", 2306.1, 51.1, None, None, "SG&amp;A derived from 10-K change", "s"),
    ("Myriad Genetics", 824.5, 65.2, 34.1, 31.1, "G&amp;A incl. amortization", "s"),
    ("NeoGenomics", 727.3, 50.2, 12.6, 37.6, "48.5% ex amortization", "n"),
    ("Veracyte", 517.1, None, None, 21.4, "S&amp;M not retrieved", "s"),
    ("Castle Biosciences", 344.2, 66.6, 40.1, 26.5, "", "s"),
    ("Fulgent Genetics", 322.7, 49.6, 13.4, 36.2, "", "s"),
]
def f(v):
    return "&ndash;" if v is None else f"{v:.1f}%"
trs = ""
for n, r, sga, sm, ga, note, g in peers:
    cls = ' class="hl"' if g == "n" else (' class="sub"' if g == "r" else "")
    tagm = " <span style='color:#6B7280;font-weight:400'>(routine)</span>" if g == "r" else ""
    trs += f'<tr{cls}><td>{n}{tagm}</td><td class="n">{r:,.0f}</td><td class="n">{f(sga)}</td><td class="n">{f(sm)}</td><td class="n">{f(ga)}</td><td>{note}</td></tr>'
body = f"""
<div class="row" style="margin-top:14px">
  <div style="flex:2.2"><table class="t" style="font-size:15.5px" id="peer">
    <tr><th>Company (FY2025)</th><th class="n">Sales $M</th><th class="n">SG&amp;A</th><th class="n">Sales &amp; mktg</th><th class="n">G&amp;A</th><th>Note</th></tr>
    {trs}
    <tr><td colspan="2"><b>Specialty median</b> (where reported)</td><td class="n"><b>59.7%</b></td><td class="n"><b>33.2%</b></td><td class="n"><b>27.4%</b></td><td></td></tr>
  </table></div>
  <div style="flex:1;display:flex;flex-direction:column;gap:12px">
    <div class="card" style="border-top:5px solid {BLUE}"><h3 style="font-size:17px">vs. Quest &amp; Labcorp</h3><div class="small">NEO is ~3&times; on SG&amp;A. But they run a
      high-volume routine-test model with ~15&ndash;19&times; the sales.</div></div>
    <div class="card" style="border-top:5px solid {GREEN}"><h3 style="font-size:17px">vs. specialty labs</h3><div class="small">NEO&rsquo;s total SG&amp;A is <b>below</b> the median: it spends
      far less on selling (12.6% vs. 33%).</div></div>
    <div class="card" style="border-top:5px solid {RED}"><h3 style="font-size:17px">The real outlier</h3><div class="small">G&amp;A: 37.6%, highest in the group, 10.2 pts over the
      specialty median, worth ~$74M a year.</div></div>
  </div>
</div>"""
slides.append(slide("The gap depends on the yardstick", "Overhead as a share of sales, FY2025 &middot; routine labs vs. specialty and oncology labs",
                    body, "Sources: FY2025 10-Ks and Q4/FY2025 earnings releases for each company; Myriad S&amp;M and Veracyte G&amp;A from aggregator data matched to 10-K text; "
                    "Natera SG&amp;A derived from the 10-K&rsquo;s stated $335.9M (39.9%) increase. Exact figures from an untagged 10-K table. Company definitions differ.",
                    tag="Part 2 &middot; Slide 6 gap analysis"))

# ================= 6. SCATTER G&A vs SCALE =================
import math
pts = [(n, r, ga, g) for n, r, sga, sm, ga, note, g in peers if ga is not None]
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
svg.append(f'<line x1="{L}" x2="{W-20}" y1="{sy(27.4):.1f}" y2="{sy(27.4):.1f}" stroke="{BLUE}" stroke-dasharray="6 5" stroke-width="1.5"/>'
           f'<text x="{sx(1150):.1f}" y="{sy(27.4)-8:.1f}" font-size="14" fill="{BLUE}">peer median 27.4%</text>')
for n, r, ga, g in pts:
    col = RED if g == "n" else NAVY
    rad = 11 if g == "n" else 8
    svg.append(f'<circle cx="{sx(r):.1f}" cy="{sy(ga):.1f}" r="{rad}" fill="{col}"/>')
    dx, anchor = (16, "start")
    dy = 5
    if n == "Exact Sciences":
        dx, anchor, dy = (14, "end", 28)
    svg.append(f'<text x="{sx(r)+dx:.1f}" y="{sy(ga)+dy:.1f}" font-size="16" font-weight="{800 if g=="n" else 600}" fill="{col}" text-anchor="{anchor}">{n} {ga:.1f}%</text>')
svg.append(f'<line x1="{sx(727.3):.1f}" x2="{sx(727.3):.1f}" y1="{sy(37.6)+12:.1f}" y2="{sy(27.4):.1f}" stroke="{RED}" stroke-width="2" stroke-dasharray="3 3"/>'
           f'<text x="{sx(727.3)-8:.1f}" y="{(sy(37.6)+sy(27.4))/2+4:.1f}" font-size="15" font-weight="700" fill="{RED}" text-anchor="end">+10.2 pts &asymp; $74M</text>')
svg.append("</svg>")
body = f"""
<div class="row" style="margin-top:16px">
  <div class="card" style="flex:1.7"><h3>G&amp;A as % of sales vs. company size, FY2025</h3>{''.join(svg)}</div>
  <div style="flex:1;display:flex;flex-direction:column;gap:14px">
    <div class="card topline"><h3>Scale doesn&rsquo;t explain it</h3><div class="small">Veracyte and Castle are <b>smaller</b> than NEO and run G&amp;A at
      21&ndash;27%. Myriad, a similar size, is 6.5 pts lower despite carrying amortization in G&amp;A.</div></div>
    <div class="card" style="border-top:5px solid {ORANGE}"><h3>Fulgent is the warning</h3><div class="small">The other lab built by acquisition with a
      lab-services mix (anatomic pathology, precision diagnostics) sits right next to NEO at 36.2%.</div></div>
    <div class="card" style="border-top:5px solid {GREEN}"><h3>And it&rsquo;s moving</h3><div class="small">Q3 2026 G&amp;A was 32.1% of sales. Still above the
      median, but the gap has roughly halved.</div></div>
  </div>
</div>"""
slides.append(slide("NEO&rsquo;s G&amp;A is high for its size", "Specialty peers that report G&amp;A separately &middot; Quest and Labcorp report only combined SG&amp;A",
                    body, "Sources: as previous slide. Peer G&amp;A shown as reported, including each company&rsquo;s own stock pay and any D&amp;A it books there.",
                    tag="Part 2 &middot; Slide 6 gap analysis"))

# ================= 7. BRIDGE TO QUEST =================
q = 17.8
neo = round(pct(SGA_EX_AMORT), 1)  # 48.5
sbc_gap = round(pct(SBC_GA + SBC_SM) - 88 / 11035 * 100, 1)   # 4.4
onet = round(pct(ONE_TIME), 1)     # 3.0
dep = round(pct(DEP_GA), 1)        # 2.8
sell = 8.0; scale = 5.0; bill = 4.0
resid = round(neo - q - sbc_gap - onet - dep - sell - scale - bill, 1)
steps = [("Stock-based pay (5.2% vs. 0.8%)", sbc_gap, ORANGE, False),
         ("&ldquo;One-time&rdquo; items in G&amp;A", onet, ORANGE, False),
         ("Depreciation booked in G&amp;A " + est(), dep, ORANGE, True),
         ("Specialty sales force " + est(), sell, BLUE, True),
         ("Scale: fixed corporate costs " + est(), scale, BLUE, True),
         ("Billing complexity " + est(), bill, BLUE, True),
         ("Unexplained excess", resid, RED, False)]
rows = [("NeoGenomics SG&amp;A, ex amortization", 0, neo, RED, f"{neo:.1f}%", True, False)]
cur = neo
for lab, v, col, h in steps:
    rows.append((lab, cur, cur - v, col, f"&minus;{v:.1f}", False, h))
    cur -= v
rows.append(("Quest Diagnostics SG&amp;A", 0, q, NAVY, f"{q:.1f}%", True, False))
acct = sbc_gap + onet + dep; struct = sell + scale + bill
body = f"""
<div class="row" style="margin-top:14px">
  <div class="card" style="flex:1.7"><h3>From 48.5% to 17.8% of sales, in points</h3>
    {waterfall(rows, 0, 52).replace('grid-template-columns: 330px', 'grid-template-columns: 350px')}
  </div>
  <div style="flex:1;display:flex;flex-direction:column;gap:12px">
    <div class="card" style="border-top:5px solid {ORANGE}"><div class="kpi" style="color:{DORANGE};font-size:26px">{acct:.1f} pts &middot; ${acct*REV/100:.0f}M</div>
      <div class="small"><b>Accounting &amp; one-offs.</b> Real costs, but not &ldquo;overhead&rdquo; in the sense of a bloated back office.</div></div>
    <div class="card" style="border-top:5px solid {BLUE}"><div class="kpi" style="color:{BLUE};font-size:26px">{struct:.0f} pts &middot; ${struct*REV/100:.0f}M</div>
      <div class="small"><b>Business model.</b> A small oncology lab needs reps and a heavy billing desk. Shrinks only with scale.</div></div>
    <div class="card" style="border-top:5px solid {RED}"><div class="kpi" style="color:{RED};font-size:26px">{resid:.1f} pts &middot; ${resid*REV/100:.0f}M</div>
      <div class="small"><b>Excess.</b> What a well-run lab of NEO&rsquo;s size and mix wouldn&rsquo;t spend.</div></div>
  </div>
</div>"""
slides.append(slide("Why NEO spends 30 points more than Quest", f"Bridge of the {neo-q:.1f}-point SG&amp;A gap (${(neo-q)*REV/100:.0f}M a year at NEO&rsquo;s sales), FY2025",
                    body, "Method: stock pay and one-offs from filings (Quest stock pay $88M; Quest&rsquo;s own one-offs ignored, so these are upper bounds). "
                    "Estimates: sales force = NEO S&amp;M 12.6% less ~4.5% assumed for routine labs; scale = ~$36M of public-company core cost (exec, board, audit, SOX, IR, core finance/IT) "
                    "at 5% of NEO&rsquo;s sales vs. &lt;0.5% at Quest; billing = revenue-cycle cost ~7% vs. ~3%, consistent with 93 vs. ~48 days to collect.",
                    tag="Part 2 &middot; Slide 6 gap analysis"))

# ================= 8. NORMALIZED G&A =================
rows = [
    ("NEO G&amp;A, reported", 0, pct(GA), RED, f"{pct(GA):.1f}%", True, False),
    ("&minus; Stock-based pay " + est(), pct(GA), pct(GA - SBC_GA), LBLUE, f"&minus;{pct(SBC_GA):.1f}", False, True),
    ("&minus; Depreciation &amp; amortization", pct(GA - SBC_GA), pct(GA - SBC_GA - DEP_GA - AMORT_GA), LBLUE, f"&minus;{pct(DEP_GA+AMORT_GA):.1f}", False, True),
    ("&minus; &ldquo;One-time&rdquo; items", pct(GA - NONCASH_GA), pct(CORE_CASH), ORANGE, f"&minus;{pct(ONE_TIME):.1f}", False, False),
    ("= NEO cash G&amp;A, recurring", 0, pct(CORE_CASH), NAVY, f"{pct(CORE_CASH):.1f}%", True, False),
    ("Castle G&amp;A ex stock pay", 0, (91.2 - 17.4) / 344.2 * 100, GREEN, f"{(91.2-17.4)/344.2*100:.1f}%", True, False),
    ("Veracyte G&amp;A, reported (incl. stock pay)", 0, 21.4, LGREEN, "21.4%", False, False),
]
gap = pct(CORE_CASH) - (91.2 - 17.4) / 344.2 * 100
body = f"""
<div class="row" style="margin-top:16px">
  <div class="card" style="flex:1.6"><h3>G&amp;A as % of sales, like for like</h3>
    {waterfall(rows, 0, 40).replace('grid-template-columns: 330px', 'grid-template-columns: 360px')}
  </div>
  <div style="flex:1;display:flex;flex-direction:column;gap:14px">
    <div class="card" style="border-top:5px solid {GREEN}"><div class="kpi" style="color:{GREEN}">~{gap:.1f} pts &asymp; ${gap*REV/100:.0f}M</div>
      <div class="small">The recurring cash gap to a lean specialty peer. Same size as the v2 deck&rsquo;s &ldquo;overhead under 30%&rdquo; prize (~$24M).</div></div>
    <div class="card topline"><h3>Read it both ways</h3><div class="small">The 30-point headline gap to Quest is mostly not cash you can take out.
      The 4-point gap is, and unlike the one-offs it comes back every year until fixed.</div></div>
  </div>
</div>
<div class="callout" style="margin-top:14px"><b>Target to hold management to:</b> cash G&amp;A (ex stock pay, D&amp;A, one-offs) at or below 21% of sales.
That is ~$27M at 2025 sales, more as sales grow if the dollars stay flat.</div>"""
slides.append(slide("Strip out the accounting: the cash gap is ~4 points", "NEO G&amp;A normalized to recurring cash cost vs. the cleanest specialty comparisons, FY2025",
                    body, "Sources: as slides 2 and 6; Castle FY2025 10-K (G&amp;A $91.2M, of which stock pay $17.4M). Veracyte includes its stock pay, so its cash ratio is lower still.",
                    tag="Part 2 &middot; Slide 6 gap analysis"))

# ================= 9. ROOT CAUSES =================
causes = [
    ("1 &middot; Four deals, never one company", ORANGE,
     "Clarient (2015), Genoptix (2018), Inivata (2021), Pathline (2025). Six US labs, overlapping systems and teams. Deal and integration costs show up every year: $26M of &ldquo;one-time&rdquo; items in 2024, $50M in 2025."),
    ("2 &middot; A slow, heavy billing machine", BLUE,
     "~93 days to get paid vs. ~48 at Quest, and getting worse (from ~80). Oncology tests need prior auth and appeals across thousands of payers; billing staff sit in G&amp;A."),
    ("3 &middot; Stock pay at 7&times; the big labs", ORANGE,
     "$41.3M, 5.7% of sales vs. 0.8% at Quest and Labcorp; 79% of executive pay is equity. ~$35M of it lands in G&amp;A."),
    ("4 &middot; Leadership churn", RED,
     "Three CEOs since 2022 and a fourth (Warren Stone) from January 2027. 2025 carried $3.5M of transition costs and $7.7M of pay to two departed executives."),
    ("5 &middot; Systems spend rising", BLUE,
     "Software &amp; technology +$8.0M in 2025, the biggest non-pay increase. Running old and new platforms side by side costs double until the old ones are switched off."),
    ("6 &middot; People ahead of sales", RED,
     "Headcount ~2,200 &rarr; ~2,500 (+14%) while sales grew 10%. G&amp;A pay +$11.5M. Plus $11.3M of Natera patent litigation to defend RaDaR."),
]
cards = "".join(f'<div class="card" style="border-top:5px solid {c}"><h3 style="font-size:18px;text-transform:none">{t}</h3><div class="small" style="font-size:15.5px">{d}</div></div>' for t, c, d in causes)
body = f"""
<div class="cards3" style="margin-top:16px">{cards}</div>
<div class="row" style="margin-top:14px;font-size:15px">
  <div style="display:flex;align-items:center;gap:8px"><span style="width:16px;height:16px;background:{ORANGE};display:inline-block;border-radius:3px"></span>Accounting / one-off</div>
  <div style="display:flex;align-items:center;gap:8px"><span style="width:16px;height:16px;background:{BLUE};display:inline-block;border-radius:3px"></span>Business model (fix slowly)</div>
  <div style="display:flex;align-items:center;gap:8px"><span style="width:16px;height:16px;background:{RED};display:inline-block;border-radius:3px"></span>Management choices (fix now)</div>
</div>"""
slides.append(slide("Six reasons NEO&rsquo;s overhead runs high", "What the filings show behind the gap",
                    body, "Sources: FY2025 10-K (history, one-offs, drivers, receivables); FY2024 10-K; 2026 proxy (pay); Q3 2026 results (CEO succession); "
                    "Quest FY2024 10-K (days sales outstanding); headcount from company profile data. Departed-executive pay = Smith $4.05M + Harris $3.69M.",
                    tag="Part 2 &middot; Slide 6 gap analysis"))

# ================= 10. WHAT TO DO =================
acts = [
    ("Finish integration: one lab system, one billing platform, close duplicate sites", "Excess + part of scale", "$10&ndash;15M", "Cash", "In progress (2 dry labs closed 2026)"),
    ("Revenue-cycle overhaul: automate prior auth and denials, cut days to collect toward 60", "Billing complexity", "$6&ndash;10M + ~$65M cash freed", "Cash", "Getting worse"),
    ("Shared-services / offshore for finance, HR and billing back office", "Excess + scale", "$5&ndash;8M", "Cash", "Not started"),
    ("Cap stock pay at ~2.5% of sales", "Stock pay", "~$17M profit", "Non-cash", "Not started"),
    ("Hold G&amp;A dollars flat while sales grow 10%/yr", "Scale", "~3.5 pts/yr", "Both", "Q3 2026 trend supports it"),
    ("Stop calling recurring deal and legal costs &ldquo;one-time&rdquo;; budget for them", "One-offs", "Visibility", "&ndash;", "Rolled off in 2026"),
]
trs = "".join(f'<tr><td><b>{a}</b></td><td>{g}</td><td class="n">{v}</td><td>{c}</td><td>{s}</td></tr>' for a, g, v, c, s in acts)
body = f"""
<div style="margin-top:14px"><table class="t" style="font-size:16px">
<tr><th>Action</th><th>Gap it closes</th><th class="n">Size / yr</th><th>Cash?</th><th>Status</th></tr>{trs}
</table></div>
<div class="row" style="margin-top:14px">
  <div class="callout dark" style="flex:1.6"><b>Realistic prize: $25&ndash;35M a year of cash G&amp;A</b>, taking cash G&amp;A from 25% toward 21% of sales, plus the
  ~3.5 points a year that comes free from holding dollars flat. That covers half to two-thirds of the remaining $49M operating loss.</div>
  <div class="callout" style="flex:1"><b>Don&rsquo;t chase Quest&rsquo;s 18%.</b> NEO&rsquo;s model needs a sales force and a specialist billing desk.
  ~40% total SG&amp;A is a credible medium-term goal.</div>
</div>"""
slides.append(slide("Closing the gap: what&rsquo;s worth doing", "Actions mapped to the gap they close &middot; sized from NEO&rsquo;s own numbers",
                    body, "Sizes are our estimates from FY2025 figures, not company targets; they overlap, so don&rsquo;t add them up. Cash freed from collections: "
                    "~33 days &times; $2.0M of sales a day. Not investment advice.", tag="Part 2 &middot; Slide 6 gap analysis"))

# ================= 11. NOTES =================
body = f"""
<div class="row" style="margin-top:16px;font-size:14.5px;line-height:1.45">
<div class="card" style="flex:1"><h3>Reported (from filings)</h3>
<ul style="margin:0;padding-left:18px">
<li>NEO FY2025: sales $727.3M; G&amp;A $273.3M; S&amp;M $92.0M; amortization $31.8M ($18.9M in cost of revenue); stock pay $41.3M; depreciation $36.1M; litigation $11.3M, deal $7.3M, CEO transition $3.5M (10-K, Q4 2025 release).</li>
<li>G&amp;A drivers 2025: pay +$11.5M, software +$8.0M, deal +$1.4M, legal/professional &minus;$2.1M, equipment &minus;$1.8M, travel &minus;$1.3M, amortization &minus;$1.0M, facilities &minus;$0.5M; Pathline integration $4.7M in G&amp;A (10-K MD&amp;A).</li>
<li>Stock pay by line, Jan&ndash;Sep 2025: G&amp;A $27.9M, S&amp;M $2.3M, R&amp;D $2.0M of $33.3M (Q3 2025 10-Q).</li>
<li>Peers FY2025: Quest sales $11,035M, SG&amp;A ~$1,967M, stock pay $88M; Labcorp $13,951.7M, SG&amp;A $2,216.3M, stock pay ~$105M; Myriad $824.5M, G&amp;A $256.8M; Exact $3,250M, S&amp;M ~$1,050M, G&amp;A ~$888.7M; Fulgent $322.7M, S&amp;M $43.4M, G&amp;A $116.7M; Castle $344.2M, SG&amp;A $229.3M, G&amp;A $91.2M (stock pay $17.4M); Veracyte $517.1M, G&amp;A ~$110.8M; Natera $2,306.1M, SG&amp;A ~$1,178M (derived).</li>
</ul></div>
<div class="card" style="flex:1"><h3>Estimated (our method)</h3>
<ul style="margin:0;padding-left:18px">
<li><b>Stock pay in G&amp;A $34.7M:</b> 84% nine-month G&amp;A share applied to the full-year $41.3M.</li>
<li><b>Depreciation in G&amp;A $20.3M:</b> $67.9M non-cash G&amp;A less stock pay and $12.9M amortization.</li>
<li><b>Functional split of the $176M core:</b> sized from 10-K driver disclosures and typical specialty-lab cost shares; ranges shown.</li>
<li><b>Bridge to Quest:</b> sales-force gap assumes ~4.5% selling cost at routine labs (they don&rsquo;t report it); scale assumes ~$36M of fixed public-company core; billing assumes revenue-cycle cost ~7% vs. ~3%. Residual is what&rsquo;s left.</li>
<li>Headcount (~2,500, +300) is from company-profile data, not the 10-K text.</li>
<li>SEC.gov was not reachable from this session; figures were taken from company IR sites, filing mirrors and aggregators and should be spot-checked against EDGAR before external use.</li>
</ul></div>
</div>"""
slides.append(slide("Notes on sources and method", "What is reported, what is estimated, and how", body, "Prepared November 2026. Not investment advice."))

html = f"""<!doctype html><html><head><meta charset="utf-8"><title>NEO Overhead Deep Dive</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:ital,wght@0,400;0,600;0,700;0,800;1,400&display=swap" rel="stylesheet">
<style>{CSS}</style></head><body>
{''.join(slides)}
</body></html>"""
OUT.write_text(html, encoding="utf-8")
print(f"wrote {OUT} with {len(slides)} slides; NEO SG&A ex amort {neo}%, residual {resid} pts, cash G&A {pct(CORE_CASH):.1f}%")

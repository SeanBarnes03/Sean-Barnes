"""NEO cost-volume-profit slides: metrics table + CVP / high-low charts.

Run:  python3 build_cvp.py  -> cvp-chart.png and neo-cvp.html next to this file
Then: node render.js <abs neo-cvp.html> <abs NEO_CVP_Metrics.pdf> <png dir>

Inputs are reported figures: quarterly net revenue and adjusted EBITDA from NeoGenomics'
earnings releases (8-K Ex. 99.1, Q1 2024 to Q3 2026), FY2025 D&A and stock pay from the 10-K,
revenue per clinical test from the Q4 2025 release, FY2026 guidance from the Q3 2026 release.
Cash cost = revenue - adjusted EBITDA (excludes D&A, stock pay, one-offs, impairments).
"""
from pathlib import Path
import base64, io
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager

HERE = Path(__file__).parent
# reuse palette, CSS and slide() helpers from the main deck without building it
src = (HERE / "build_deck.py").read_text()
exec(src.split("slides = []")[0])

# ---------- data ($M) ----------
Q = [("Q1'24", 156.240, 3.492), ("Q2'24", 164.502, 10.869), ("Q3'24", 167.824, 13.374), ("Q4'24", 172.000, 11.873),
     ("Q1'25", 168.035, 7.070), ("Q2'25", 181.330, 10.675), ("Q3'25", 187.797, 12.232), ("Q4'25", 190.170, 13.380),
     ("Q1'26", 186.672, 9.004), ("Q2'26", 201.656, 14.467), ("Q3'26", 209.254, 18.669)]
COST = [(n, r, r - e) for n, r, e in Q]
FY25 = COST[4:8]
REV25, EBITDA25 = 727.332, 43.357
DA25 = 36.072 + 31.752
SBC25 = 41.316
ONEOFF25 = 3.500 + 7.266 + 11.283 + 27.753          # CEO, deals, litigation, impairment
PRICE = 488.0                                     # revenue per clinical test, Q4 2025
GUIDE_REV, GUIDE_EBITDA = 808.0, 60.0             # FY2026 guidance midpoint / ~$60M

# ---------- high-low on FY2025 quarters ----------
hi = max(FY25, key=lambda x: x[1]); lo = min(FY25, key=lambda x: x[1])
V = (hi[2] - lo[2]) / (hi[1] - lo[1])             # variable cost per $ of sales
FQ = hi[2] - V * hi[1]                            # quarterly fixed cost from the high point
hi_all = max(COST, key=lambda x: x[1]); lo_all = min(COST, key=lambda x: x[1])
V_ALL = (hi_all[2] - lo_all[2]) / (hi_all[1] - lo_all[1])

VC = V * REV25
CM = REV25 - VC
CMR = CM / REV25
FIXED = CM - EBITDA25                             # annual cash fixed costs, ties to reported adj. EBITDA
BE = FIXED / CMR
MOS = REV25 - BE
DOL = CM / EBITDA25
TARGET = (FIXED + GUIDE_EBITDA) / CMR
FIXED_GAAP = FIXED + DA25 + SBC25                 # recurring GAAP fixed (ex one-offs)
BE_GAAP = FIXED_GAAP / CMR
VC_T = V * PRICE
CM_T = PRICE - VC_T
BE_TESTS = FIXED * 1e6 / CM_T
g_rev = 209.254 / 187.797 - 1
g_eb = 18.669 / 12.232 - 1
FIX_IMPLIED_26 = GUIDE_REV * CMR - GUIDE_EBITDA

# ---------- chart (create-viz) ----------
for f in ["/usr/share/fonts/opentype/inter/Inter-Regular.otf", "/usr/share/fonts/opentype/inter/Inter-Bold.otf",
          "/usr/share/fonts/opentype/inter/Inter-SemiBold.otf"]:
    try:
        font_manager.fontManager.addfont(f)
    except Exception:
        pass
plt.rcParams.update({"font.family": "Inter", "font.size": 12, "axes.edgecolor": "#B8C0CF", "axes.labelcolor": "#374151",
                     "xtick.color": "#4B5563", "ytick.color": "#4B5563"})
fig, (a1, a2) = plt.subplots(1, 2, figsize=(12.4, 4.15), gridspec_kw={"width_ratios": [1.25, 1]})

xs = [0, 1100]
a1.plot(xs, xs, color=GREEN, lw=2.6, label="Sales")
a1.plot(xs, [FIXED + V * x for x in xs], color=BLUE, lw=2.6, label=f"Cash cost: ${FIXED:.0f}M fixed + {V*100:.1f}% of sales")
a1.plot(xs, [FIXED_GAAP + V * x for x in xs], color=RED, lw=2, ls="--", label=f"+ D&A and stock pay (${FIXED_GAAP:.0f}M fixed)")
for x, lab, col, dy in [(BE, f"Cash break-even\n${BE:.0f}M", BLUE, -230), (BE_GAAP, f"GAAP break-even\n${BE_GAAP:.0f}M", RED, -330)]:
    a1.scatter([x], [x], s=70, color=col, zorder=5)
    a1.annotate(lab, (x, x), xytext=(x + 15, x + dy), fontsize=11, color=col, fontweight="bold",
                arrowprops=dict(arrowstyle="-", color=col, lw=1))
a1.axvline(REV25, color=NAVY, lw=1.2, ls=":")
a1.text(REV25 - 8, 30, f"FY2025\n${REV25:.0f}M", ha="right", va="bottom", fontsize=11, color=NAVY, fontweight="bold")
a1.axvline(GUIDE_REV, color=GREY, lw=1.2, ls=":")
a1.text(GUIDE_REV + 8, 30, f"FY2026 guide\n${GUIDE_REV:.0f}M", ha="left", va="bottom", fontsize=11, color=GREY)
a1.fill_between([BE, REV25], [BE, REV25], [FIXED + V * BE, FIXED + V * REV25], color=GREEN, alpha=0.12)
a1.set_xlim(0, 1100); a1.set_ylim(0, 1100)
a1.set_xlabel("Annual sales ($M)"); a1.set_ylabel("$M")
a1.set_title(f"FY2025: \\${REV25-BE:.0f}M past cash break-even, \\${BE_GAAP-REV25:.0f}M short of GAAP", loc="left", fontsize=13.5, fontweight="bold", color=NAVY)
a1.legend(loc="upper left", frameon=False, fontsize=10.5)

rx = [r for _, r, _ in COST]; cy = [c for *_, c in COST]
cols = [ORANGE if n.endswith("25") else LBLUE for n, *_ in COST]
a2.scatter(rx, cy, s=55, c=cols, zorder=4, edgecolor="white", lw=0.8)
for n, r, c in COST:
    if n in (hi[0], lo[0], "Q1'24", "Q3'26"):
        a2.annotate(n, (r, c), xytext=(6, -14 if n != "Q3'26" else 6), textcoords="offset points", fontsize=10.5, color=NAVY)
lx = [150, 215]
a2.plot(lx, [FQ + V * x for x in lx], color=DORANGE, lw=2.2, label=f"FY2025 high-low: {V*100:.1f}% variable")
a2.plot([lo_all[1], hi_all[1]], [lo_all[2], hi_all[2]], color=GREY, lw=1.2, ls="--", label=f"Q1'24–Q3'26 high-low: {V_ALL*100:.1f}%")
a2.set_xlabel("Quarterly sales ($M)"); a2.set_ylabel("Quarterly cash cost ($M)")
a2.set_title("71% of each extra sales dollar becomes cost", loc="left", fontsize=13.5, fontweight="bold", color=NAVY)
a2.legend(loc="upper left", frameon=False, fontsize=10.5)
for a in (a1, a2):
    a.spines["top"].set_visible(False); a.spines["right"].set_visible(False)
    a.grid(axis="y", color="#E5E7EB", lw=0.8); a.set_axisbelow(True)
fig.tight_layout()
fig.savefig(HERE / "cvp-chart.png", dpi=200, bbox_inches="tight")
buf = io.BytesIO(); fig.savefig(buf, format="png", dpi=200, bbox_inches="tight")
IMG = base64.b64encode(buf.getvalue()).decode()

# ---------- slide 1: metrics table ----------
M = lambda x: f"${x:,.0f}M"
rows = [
    ("CM per unit", f"${CM_T:.0f} / test", f"${PRICE:.0f} revenue per test &minus; ${VC_T:.0f} variable cost ({V*100:.1f}%)",
     "Each extra test adds ~$139 toward fixed costs. Growth in higher-priced NGS tests raises it; reimbursement cuts shrink it."),
    ("CM ratio", f"{CMR*100:.1f}%", f"{M(CM)} CM &divide; {M(REV25)} sales",
     "Only 28.5&cent; of each new sales dollar is left to cover overhead. Lab supplies and pay set it, so lab cost cuts move it fastest."),
    ("Profit (adj. EBITDA)", M(EBITDA25), f"{M(CM)} CM &minus; {M(FIXED)} fixed cash costs",
     "The cash-profit line management guides to. GAAP adds $68M D&amp;A, $41M stock pay and $50M one-offs: a $116M operating loss."),
    ("Break-even (units)", f"{BE_TESTS/1e6:.2f}M tests", f"{M(FIXED)} &divide; ${CM_T:.0f}",
     "~295K tests a quarter covers cash fixed costs. Q3 2026 ran at ~368K clinical tests, so test volume is above it."),
    ("Break-even ($)", f"{M(BE)} cash<br>{M(BE_GAAP)} GAAP", f"{M(FIXED)} &divide; {CMR*100:.1f}% (GAAP: {M(FIXED_GAAP)} &divide; {CMR*100:.1f}%)",
     f"Cash break-even was passed around 2023. GAAP profit needs ~${BE_GAAP:.0f}M of sales: {(BE_GAAP/REV25-1)*100:.0f}% more than 2025."),
    ("Target profit ($)", M(TARGET), f"({M(FIXED)} + $60M target) &divide; {CMR*100:.1f}%",
     f"Sales needed for the ~$60M 2026 adj. EBITDA guide. Guided sales of ~$808M imply fixed costs creep to ~{M(FIX_IMPLIED_26)}."),
    ("Margin of safety ($)", f"{M(MOS)} ({MOS/REV25*100:.0f}%)", f"{M(REV25)} &minus; {M(BE)}",
     f"Sales could fall {MOS/REV25*100:.0f}% before cash profit hits zero. On a GAAP basis the margin is &minus;${BE_GAAP-REV25:.0f}M."),
    ("Operating leverage", f"{DOL:.1f}&times;", f"{M(CM)} CM &divide; {M(EBITDA25)} adj. EBITDA",
     "High fixed costs make profit swing ~5&times; faster than sales, both ways. It is why growth fixes margins quickly."),
    ("% change in profit", f"+{g_rev*DOL*100:.0f}% predicted", f"Q3 2026 sales +{g_rev*100:.1f}% &times; {DOL:.1f}",
     f"Actual Q3 2026 adj. EBITDA grew +{g_eb*100:.0f}%. The model holds: 11% growth delivered half again as much profit."),
    ("High-low variable rate", f"{V*100:.1f}% of sales", f"({hi[2]:.1f} &minus; {lo[2]:.1f}) &divide; ({hi[1]:.1f} &minus; {lo[1]:.1f}): {hi[0]} vs. {lo[0]} cash cost",
     f"Splits costs without internal data. Over Q1'24&ndash;Q3'26 it gives {V_ALL*100:.1f}%, so the split is stable."),
    ("High-low fixed cost", f"{M(FQ)}/qtr", f"{hi[2]:.1f} &minus; ({V*100:.1f}% &times; {hi[1]:.1f})",
     "~$164M a year of cash costs that don't move with sales. Every $1M cut lowers break-even sales by $3.5M."),
]
trs = "".join(f'<tr><td><b>{a}</b></td><td class="n" style="font-weight:800;color:{NAVY}">{b}</td><td style="color:#4B5563">{c}</td><td>{d}</td></tr>' for a, b, c, d in rows)
body1 = f"""
<div style="margin-top:12px">
<table class="t" style="font-size:12.6px;line-height:1.28">
<tr><th style="width:150px">Metric</th><th class="n" style="width:125px">NEO FY2025</th><th style="width:330px">Calculation</th><th>Why it matters for NeoGenomics</th></tr>
{trs}
</table></div>"""
s1 = slide("Appendix: CVP metric detail", "FY2025, cash basis (adjusted EBITDA) unless noted &middot; variable/fixed split by the high-low method on quarterly results",
           body1, "Sources: NeoGenomics quarterly earnings releases Q1 2024&ndash;Q3 2026 (revenue, adj. EBITDA, revenue per test, 2026 guidance); FY2025 10-K (D&amp;A, stock pay, one-offs). "
           "Cash cost = sales &minus; adj. EBITDA. Unit figures apply the company-wide variable rate to revenue per clinical test.", tag="CVP briefing")
s1 = s1.replace('<div class="src">', '<div class="src" style="bottom:12px;font-size:12.5px">')

# ---------- slide 2: charts ----------
body2 = f"""
<div class="card" style="margin-top:12px;padding:8px 16px"><img src="data:image/png;base64,{IMG}" style="width:100%;display:block"></div>
<div class="row" style="margin-top:12px">
  <div class="callout" style="flex:1;font-size:15px;padding:10px 18px"><b>Why overhead matters here:</b> with a {CMR*100:.1f}% CM ratio, each $1M of fixed cost needs $3.5M of sales
  to cover it. Cutting the ~$28&ndash;50M G&amp;A gap would lower GAAP break-even by ~$100&ndash;175M of sales.</div>
  <div class="callout dark" style="flex:1;font-size:15px;padding:10px 18px"><b>Two levers, both needed:</b> grow sales (each +10% lifts adj. EBITDA ~{DOL*10:.0f}%) and raise the
  CM ratio through lab supply and test-mix gains. Sales growth alone needs ~$960M to reach GAAP profit.</div>
</div>"""
s2 = slide("Where NEO sits on the cost-volume-profit chart", "FY2025 annual CVP (left) and the quarterly cost data behind the split (right)",
           body2, "Sources: as the appendix. Orange dots = FY2025 quarters used for the high-low split; light blue = other quarters. GAAP line excludes one-offs and impairments.",
           tag="CVP briefing")


def exec_summary(answer, messages, decisions, kpis):
    """answer: str; messages: [(headline, evidence, slide_ref)]; decisions: [str]; kpis: [(value, label, color)]."""
    msg = "".join(
        f'<div style="display:flex;gap:12px;padding:7px 0;border-bottom:1px solid #E5E7EB">'
        f'<div style="flex:0 0 30px;height:30px;border-radius:15px;background:{NAVY};color:#fff;font-weight:800;display:flex;align-items:center;justify-content:center;font-size:15px">{i}</div>'
        f'<div style="flex:1;font-size:15px;line-height:1.35"><b style="color:{NAVY}">{h}</b> {e}</div>'
        f'<div style="flex:0 0 62px;text-align:right;font-size:12.5px;color:{GREY};padding-top:3px">{r}</div></div>'
        for i, (h, e, r) in enumerate(messages, 1))
    dec = "".join(f'<li style="margin-bottom:7px">{d}</li>' for d in decisions)
    kp = "".join(f'<div class="card" style="flex:1;border-top:5px solid {c};text-align:center;padding:8px 6px">'
                 f'<div class="kpi" style="color:{c};font-size:23px">{v}</div><div class="small" style="font-size:12.5px">{l}</div></div>' for v, l, c in kpis)
    return f"""
<div class="callout dark" style="margin-top:12px;font-size:18px;padding:12px 22px"><b>The answer:</b> {answer}</div>
<div class="row" style="margin-top:12px">
  <div class="card" style="flex:1.65;padding:10px 18px"><h3 style="margin-bottom:2px">Key messages</h3>{msg}</div>
  <div style="flex:1;display:flex;flex-direction:column;gap:12px">
    <div class="card" style="border-top:5px solid {ORANGE};padding:12px 18px"><h3 style="margin-bottom:6px">Decisions needed</h3>
      <ol class="small" style="font-size:14.5px;margin:0;padding-left:20px;line-height:1.38">{dec}</ol></div>
    <div class="row" style="gap:10px">{kp}</div>
  </div>
</div>"""

# ---------- slide 0: executive summary ----------
GAAP_CUT_26 = FIXED_GAAP - GUIDE_REV * CMR
body0 = exec_summary(
    f"growth is lifting cash profit fast, but GAAP profit needs ~${BE_GAAP:.0f}M of sales or ~${GAAP_CUT_26:.0f}M less fixed cost. Overhead is the cheapest lever.",
    [("Each sales dollar keeps 28.5&cent;.", f"Contribution margin is ${CM_T:.0f} on a ${PRICE:.0f} test; the other {V*100:.1f}% is variable cost (lab supplies, pay, shipping).", "Appendix"),
     ("Cash break-even is behind us.", f"${BE:.0f}M of sales covers ${FIXED:.0f}M of cash fixed costs; 2025 sales were {MOS/REV25*100:.0f}% above it.", "Slide 2"),
     ("GAAP profit is far off.", f"With D&amp;A and stock pay, break-even is ${BE_GAAP:.0f}M: {(BE_GAAP/REV25-1)*100:.0f}% above 2025. At 2026 guided sales (~${GUIDE_REV:.0f}M) it needs ~${GAAP_CUT_26:.0f}M less fixed cost.", "Slide 2"),
     ("Growth pays back about 5&times;.", f"Operating leverage {DOL:.1f}&times;: +10% sales &asymp; +{DOL*10:.0f}% adj. EBITDA. Q3 2026 proved it: sales +{g_rev*100:.0f}%, adj. EBITDA +{g_eb*100:.0f}%.", "Appendix"),
     ("Fixed costs are creeping.", f"2026 guidance implies cash fixed costs of ~${FIX_IMPLIED_26:.0f}M, up ~${FIX_IMPLIED_26-FIXED:.0f}M: part of the growth gain is leaking into overhead.", "Appendix")],
    [f"<b>Cap cash fixed costs</b> at ~${FIXED:.0f}M while sales grow, to keep the {DOL:.1f}&times; leverage.",
     f"<b>Lift the CM ratio</b> through lab supplies and test mix: each +1 pt is ~${GUIDE_REV/100:.0f}M a year at 2026 sales.",
     f"<b>Set a dated path to GAAP profit</b> combining the G&amp;A gap ($28&ndash;50M) and stock pay with growth; each $1M of fixed cost cut lowers break-even sales by ${1/CMR:.1f}M."],
    [(f"{CMR*100:.1f}%", "CM ratio", NAVY), (f"${BE:.0f}M", f"Cash break-even (GAAP ${BE_GAAP:.0f}M)", RED), (f"{DOL:.1f}&times;", "Operating leverage", DORANGE)])
s0 = slide("Executive summary", "NeoGenomics cost-volume-profit view, FY2025 &middot; what it means for growth, overhead and the path to GAAP profit", body0,
           "Sources: NeoGenomics quarterly earnings releases Q1 2024&ndash;Q3 2026 and FY2025 10-K. Cash basis = adjusted EBITDA; costs split into variable and fixed by the high-low method on quarterly results. "
           "Not investment advice.")

html = f"""<!doctype html><html><head><meta charset="utf-8"><title>NEO CVP Executive Brief</title>
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:ital,wght@0,400;0,600;0,700;0,800;1,400&display=swap" rel="stylesheet">
<style>{CSS}</style></head><body>{s0}{s2}{s1}</body></html>"""
(HERE / "neo-cvp.html").write_text(html, encoding="utf-8")
print(f"V={V:.4f} F={FIXED:.1f} CM={CM:.1f} CMR={CMR:.4f} BE={BE:.1f} BE_GAAP={BE_GAAP:.1f} MOS={MOS:.1f} DOL={DOL:.2f} "
      f"target={TARGET:.1f} CMtest={CM_T:.1f} BEtests={BE_TESTS:,.0f} FQ={FQ:.2f} V_all={V_ALL:.4f} fix26={FIX_IMPLIED_26:.1f}")

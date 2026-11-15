"""NEO pharma (non-clinical) executive briefing: charts + slides.

Run:  python3 build_pharma.py  -> pharma-*.png and neo-pharma.html next to this file
Then: node render.js <abs neo-pharma.html> <abs NEO_Pharma_Executive_Briefing.pdf> <png dir>

Pharma revenue is not reported after Q3 2024. It is rebuilt as total revenue minus clinical
revenue, where clinical = clinical tests x average revenue per clinical test (both reported in
each quarterly earnings release). Check: for Q1-Q3 2024, when NEO still reported Advanced
Diagnostics, the rebuild lands within $0.2M of the reported figure.
"""
from pathlib import Path
import base64, io
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager

HERE = Path(__file__).parent
exec((HERE / "build_deck.py").read_text().split("slides = []")[0])   # palette, CSS, slide()

# ---------- data (earnings releases, 8-K Ex. 99.1) ----------
Q = [  # quarter, clinical tests, avg revenue per clinical test ($), total revenue ($M)
    ("Q1'24", 300827, 447, 156.240), ("Q2'24", 311670, 454, 164.502), ("Q3'24", 314564, 463, 167.824),
    ("Q4'24", 321679, 465, 172.000), ("Q1'25", 326163, 459, 168.035), ("Q2'25", 356630, 461, 181.330),
    ("Q3'25", 360774, 476, 187.797), ("Q4'25", 356136, 488, 190.170), ("Q1'26", 345679, 495, 186.672),
    ("Q2'26", 363498, 515, 201.656), ("Q3'26", 367279, 530, 209.254)]
QD = [(q, n * a / 1e6, r - n * a / 1e6, r) for q, n, a, r in Q]          # quarter, clinical, pharma, total
REPORTED_AD = {"Q1'24": 21.705, "Q2'24": 23.114, "Q3'24": 22.041}
Y = {"FY2023": (1165079, 425, 591.643), "FY2024": (1248740, 457, 660.566), "FY2025": (1399703, 471, 727.332)}
YD = {k: (n * a / 1e6, r - n * a / 1e6, r) for k, (n, a, r) in Y.items()}
LTM_PH = sum(p for _, _, p, _ in QD[-4:]); LTM_TOT = sum(t for *_, t in QD[-4:])
RUN = sum(p for _, _, p, _ in QD[-2:]) * 2                                # annualized last two quarters
c24, p24, t24 = YD["FY2024"]; c25, p25, t25 = YD["FY2025"]; c23, p23, t23 = YD["FY2023"]
DRAG = (t25 - t24) / t24 * 100 - (c25 - c24 + (p25 - p24) * 0) / t24 * 100  # growth points lost to pharma
CMR = 0.285
WRITE = [("InVisionFirst-Lung write-off\n(Inivata, 2025)", 11.4), ("Trapelo write-down\n(sold for $2.5M, 2025)", 15.9),
         ("Restructuring incl. intl.\nsite closures (2024)", 6.658)]
yoy = {QD[i][0]: QD[i][2] / QD[i - 4][2] - 1 for i in range(4, len(QD))}

# ---------- chart style ----------
for f in ["/usr/share/fonts/opentype/inter/Inter-Regular.otf", "/usr/share/fonts/opentype/inter/Inter-Bold.otf",
          "/usr/share/fonts/opentype/inter/Inter-SemiBold.otf"]:
    try:
        font_manager.fontManager.addfont(f)
    except Exception:
        pass
plt.rcParams.update({"font.family": "Inter", "font.size": 12, "axes.edgecolor": "#B8C0CF", "axes.labelcolor": "#374151",
                     "xtick.color": "#4B5563", "ytick.color": "#4B5563"})

def tidy(a):
    a.spines["top"].set_visible(False); a.spines["right"].set_visible(False)
    a.grid(axis="y", color="#E5E7EB", lw=0.8); a.set_axisbelow(True)

def png(fig, name):
    fig.savefig(HERE / name, dpi=200, bbox_inches="tight")
    b = io.BytesIO(); fig.savefig(b, format="png", dpi=200, bbox_inches="tight"); plt.close(fig)
    return base64.b64encode(b.getvalue()).decode()

# Chart 1: quarterly pharma revenue + share of total
fig, (a1, a2) = plt.subplots(1, 2, figsize=(12.4, 4.0), gridspec_kw={"width_ratios": [1.55, 1]})
xs = range(len(QD))
cols = [LBLUE if q.endswith("24") else ORANGE for q, *_ in QD]
bars = a1.bar(xs, [p for _, _, p, _ in QD], color=cols, width=0.68)
for i, (q, c, p, t) in enumerate(QD):
    a1.text(i, p + 0.4, f"${p:.1f}M", ha="center", fontsize=10, fontweight="bold", color=NAVY)
    if q in yoy:
        a1.text(i, p / 2, f"{yoy[q]*100:+.0f}%", ha="center", fontsize=10, color="white", fontweight="bold")
a1.set_xticks(list(xs)); a1.set_xticklabels([q for q, *_ in QD], fontsize=10.5)
a1.set_ylim(0, 27); a1.set_ylabel("Pharma revenue ($M)")
a1.set_title("Pharma revenue: down a third in two years; falls are slowing", loc="left", fontsize=13.5, fontweight="bold", color=NAVY)
a1.text(0.99, 0.95, "white = change vs. same quarter last year", transform=a1.transAxes, ha="right", fontsize=9.5, color=GREY)
tidy(a1)
shares = [p / t * 100 for _, _, p, t in QD]
a2.plot(list(xs), shares, color=RED, lw=2.6, marker="o", ms=5)
for i in (0, len(QD) - 1):
    a2.annotate(f"{shares[i]:.1f}%", (i, shares[i]), xytext=(0, 9), textcoords="offset points", ha="center", fontsize=11, fontweight="bold", color=RED)
a2.set_xticks([0, 4, 8, 10]); a2.set_xticklabels(["Q1'24", "Q1'25", "Q1'26", "Q3'26"], fontsize=10.5)
a2.set_ylim(0, 17); a2.set_ylabel("% of total revenue")
a2.set_title("Share of NEO revenue halved", loc="left", fontsize=13.5, fontweight="bold", color=NAVY)
tidy(a2); fig.tight_layout()
IMG1 = png(fig, "pharma-trend.png")

# Chart 2: FY2025 growth bridge + write-downs
fig, (a1, a2) = plt.subplots(1, 2, figsize=(12.4, 3.9), gridspec_kw={"width_ratios": [1.2, 1]})
steps = [("FY2024\nrevenue", 0, t24, NAVY), ("Clinical\ngrowth", t24, t24 + (c25 - c24), GREEN),
         ("Pharma\ndecline", t24 + (c25 - c24), t25, RED), ("FY2025\nrevenue", 0, t25, NAVY)]
for i, (lab, s, e, col) in enumerate(steps):
    lo_, hi_ = sorted((s, e))
    a1.bar(i, hi_ - lo_, bottom=lo_, color=col, width=0.62)
    v = e - s if s else e
    a1.text(i, hi_ + 6, (f"{v:+.1f}" if s else f"${v:.1f}M"), ha="center", fontsize=11.5, fontweight="bold", color=col)
a1.set_xticks(range(4)); a1.set_xticklabels([s[0] for s in steps], fontsize=10.5)
a1.set_ylim(600, 780); a1.set_ylabel(r"\$M (axis starts at \$600M)")
a1.set_title(f"Pharma cut 2025 growth from {(c25-c24)/t24*100:.1f}% to {(t25-t24)/t24*100:.1f}%", loc="left", fontsize=13.5, fontweight="bold", color=NAVY)
tidy(a1)
labs = [w[0] for w in WRITE]; vals = [w[1] for w in WRITE]
a2.barh(range(3), vals, color=[ORANGE, RED, LBLUE], height=0.58)
for i, v in enumerate(vals):
    a2.text(v + 0.3, i, f"${v:.1f}M", va="center", fontsize=11.5, fontweight="bold", color=NAVY)
a2.set_yticks(range(3)); a2.set_yticklabels(labs, fontsize=10.5); a2.invert_yaxis(); a2.set_xlim(0, 20)
a2.set_xlabel("$M")
a2.set_title(f"${sum(vals):.0f}M of charges on non-core assets", loc="left", fontsize=13.5, fontweight="bold", color=NAVY)
a2.spines["top"].set_visible(False); a2.spines["right"].set_visible(False); a2.grid(axis="x", color="#E5E7EB", lw=0.8); a2.set_axisbelow(True)
fig.tight_layout()
IMG2 = png(fig, "pharma-cost.png")

# Chart 3: exit economics
fig, a = plt.subplots(figsize=(7.4, 4.1))
x = [0, 45]
for cm, col, ls in [(0.285, BLUE, "-"), (0.40, DORANGE, "--")]:
    lost = RUN * cm
    a.plot(x, [v - lost for v in x], color=col, lw=2.4, ls=ls, label=f"Pharma CM {cm*100:.1f}%: break-even at ${lost:.0f}M")
    a.scatter([lost], [0], color=col, s=55, zorder=5)
a.axhline(0, color="#6B7280", lw=1)
a.fill_between(x, 0, 30, color=GREEN, alpha=0.07); a.fill_between(x, -30, 0, color=RED, alpha=0.06)
a.text(1, 22, "Exit adds EBITDA", color=GREEN, fontsize=11.5, fontweight="bold")
a.text(1, -26, "Exit destroys EBITDA", color=RED, fontsize=11.5, fontweight="bold")
a.set_xlim(0, 45); a.set_ylim(-30, 30)
a.set_xlabel("Fixed costs that would disappear on exit ($M / yr)"); a.set_ylabel("Change in adj. EBITDA ($M / yr)")
a.set_title("Exit only pays if it removes > $17–23M of cost", loc="left", fontsize=13.5, fontweight="bold", color=NAVY)
a.legend(loc="lower right", frameon=False, fontsize=10.5); tidy(a); fig.tight_layout()
IMG3 = png(fig, "pharma-exit.png")

def img(b64, w="100%"):
    return f'<img src="data:image/png;base64,{b64}" style="width:{w};display:block">'

S = []
# ---------- 1. Executive summary ----------
body = f"""
<div class="row" style="margin-top:14px">
  <div class="card" style="flex:1;border-top:5px solid {RED};padding:14px 20px">
    <h3 style="margin-bottom:6px">Situation</h3>
    <ul class="small" style="font-size:15.5px;margin:0;padding-left:18px;line-height:1.45">
      <li>Pharma revenue fell from <b>${p23:.0f}M (2023) to ${LTM_PH:.0f}M</b> over the last 12 months; now <b>{QD[-1][2]/QD[-1][3]*100:.0f}% of sales</b>, from 16%.</li>
      <li>The fall is slowing (&minus;27% &rarr; {yoy["Q3'26"]*100:.0f}% year on year) and has held at ~$14.5M a quarter for two quarters. Not yet a bottom.</li>
      <li>It cost <b>{(c25-c24)/t24*100-(t25-t24)/t24*100:.1f} pts of 2025 growth</b> and sits beside ~<b>${sum(vals):.0f}M</b> of write-downs and restructuring on non-core assets. Its P&amp;L is not reported.</li>
    </ul>
  </div>
  <div class="card" style="flex:1;border-top:5px solid {GREEN};padding:14px 20px">
    <h3 style="margin-bottom:6px">Why it may still be worth keeping</h3>
    <ul class="small" style="font-size:15.5px;margin:0;padding-left:18px;line-height:1.45">
      <li><b>Trial work feeds future clinical tests</b>, NEO&rsquo;s 15% growth engine.</li>
      <li><b>RaDaR needs pharma trials</b> to build evidence for reimbursement.</li>
      <li><b>It shares labs NEO pays for anyway:</b> ~${RUN*CMR:.0f}M a year toward fixed costs at the company margin.</li>
      <li>Data licensing at near-zero extra cost; no insurer risk; selling now means selling at the bottom.</li>
    </ul>
  </div>
</div>
<div class="row" style="margin-top:14px">
  <div class="card" style="flex:1;border-top:5px solid {NAVY};text-align:center;padding:12px"><div class="kpi" style="color:{NAVY};font-size:28px">${RUN:.0f}M</div>
    <div class="small">Current annual run-rate</div></div>
  <div class="card" style="flex:1;border-top:5px solid {BLUE};text-align:center;padding:12px"><div class="kpi" style="color:{BLUE};font-size:28px">${RUN*CMR:.0f}&ndash;{RUN*0.40:.0f}M</div>
    <div class="small">Costs exit must remove to break even</div></div>
  <div class="card" style="flex:1;border-top:5px solid {ORANGE};text-align:center;padding:12px"><div class="kpi" style="color:{DORANGE};font-size:28px">Q1 2027</div>
    <div class="small">Decision gate: keep core or exit</div></div>
</div>
<div class="callout dark" style="margin-top:14px"><b>Recommendation: keep and resize, with a deadline.</b> Keep the parts that feed clinical growth (trial testing, RaDaR, data),
cut the cost base to fit ~${RUN:.0f}M of revenue, and report pharma as its own P&amp;L from Q1 2027. If revenue has not stabilized and the unit does not cover its
avoidable costs by Q1 2027 results, sell or close it.</div>"""
S.append(slide("Pharma: keep, resize, and set a deadline", "Executive summary &middot; NeoGenomics pharma / non-clinical business", body,
               "Sources: NeoGenomics quarterly earnings releases Q1 2024&ndash;Q3 2026 and FY2025 10-K. Pharma revenue rebuilt as total minus clinical (tests &times; revenue per test); "
               "validated to within $0.2M of reported Advanced Diagnostics revenue for Q1&ndash;Q3 2024. Not investment advice."))

# ---------- 2. Shrinking ----------
body = f"""
<div class="card" style="margin-top:14px;padding:10px 16px">{img(IMG1)}</div>
<div class="row" style="margin-top:12px">
  <div class="card" style="flex:1;border-top:5px solid {RED}"><div class="kpi" style="color:{RED};font-size:26px">&minus;${p23-LTM_PH:.0f}M</div>
    <div class="small">Lost since 2023 (${p23:.1f}M &rarr; ${LTM_PH:.1f}M last 12 months), &minus;{(1-LTM_PH/p23)*100:.0f}%.</div></div>
  <div class="card" style="flex:1;border-top:5px solid {ORANGE}"><div class="kpi" style="color:{DORANGE};font-size:26px">&minus;27% &rarr; {yoy["Q3'26"]*100:.0f}%</div>
    <div class="small">Year-on-year declines narrowing as the comparison base shrinks.</div></div>
  <div class="card" style="flex:1;border-top:5px solid {BLUE}"><div class="kpi" style="color:{BLUE};font-size:26px">Management: &ldquo;macro&rdquo;</div>
    <div class="small">Biotech funding, site closures, lower RaDaR. Q2 2025: pressure &ldquo;beyond our initial assumptions.&rdquo;</div></div>
</div>"""
S.append(slide("Pharma is a third smaller and still shrinking", "Quarterly pharma (non-clinical) revenue and share of NEO revenue, Q1 2024&ndash;Q3 2026",
               body, "Sources: quarterly earnings releases (tests, revenue per test, total revenue; management commentary in Q3 2024, Q2 2025 and Q4 2025 releases). "
               "Blue bars = 2024; orange = 2025&ndash;26.", tag="Pharma briefing"))

# ---------- 3. Cost ----------
body = f"""
<div class="card" style="margin-top:14px;padding:10px 16px">{img(IMG2)}</div>
<div class="row" style="margin-top:12px">
  <div class="callout" style="flex:1;font-size:15.5px;padding:12px 18px"><b>Hidden by the headline:</b> clinical grew {(c25-c24)/c24*100:.1f}% in 2025. Reported growth of
  {(t25-t24)/t24*100:.1f}% understates the core business, and the market prices the blend.</div>
  <div class="callout" style="flex:1;font-size:15.5px;padding:12px 18px"><b>Goodwill at risk:</b> in Q3 2025 the non-clinical reporting unit needed a full valuation test.
  It passed, but the auditor flagged it as a critical audit matter. Another year of decline could force a write-down.</div>
</div>"""
S.append(slide("The decline has already cost growth and capital", "FY2025 revenue bridge (left) and charges on non-core assets, 2024&ndash;25 (right)",
               body, "Sources: FY2025 10-K (impairments, Trapelo sale, goodwill critical audit matter, restructuring); Q4 2025 earnings release. "
               "These charges are on non-core assets, not all of them pharma: Trapelo was clinical decision-support software, and the 2024 restructuring covered other actions too.", tag="Pharma briefing"))

# ---------- 4. Case to keep ----------
reasons = [
    ("1 &middot; Trial work feeds clinical tests", GREEN, "Tests run in drug trials can become routine clinical tests once the drug is approved. NGS, NEO&rsquo;s growth engine, grew 22&ndash;29%.", "Holds if: clinical revenue can be traced to tests that started as trial work."),
    ("2 &middot; RaDaR needs pharma", GREEN, "NEO spent $11.3M defending RaDaR in 2025. Sponsor-paid trials build the evidence needed for reimbursement.", "Holds if: there is a funded trial pipeline and a reimbursement timeline."),
    ("3 &middot; Shares labs NEO pays for anyway", BLUE, f"~${RUN:.0f}M of revenue at the company&rsquo;s 28.5% CM covers ~${RUN*CMR:.0f}M of fixed cost. Exit leaves shared labs, IT and G&amp;A behind.", "Holds if: pharma covers the costs that would disappear without it."),
    ("4 &middot; Data at near-zero extra cost", BLUE, "Anonymized data from ~1.4M clinical tests a year is licensed to drug companies. It grows without new lab capacity.", "Holds if: data revenue grows; it depends on pharma relationships."),
    ("5 &middot; Not dependent on insurers", ORANGE, "Contract billing with drug companies: no denials or Medicare price cuts, unlike clinical revenue.", "Holds if: collections are faster than clinical&rsquo;s ~80 days (not disclosed)."),
    ("6 &middot; Don&rsquo;t sell at the bottom", ORANGE, "Trapelo fetched $2.5M after a $15.9M write-down. A sale now could also lock in a goodwill loss.", "Holds if: revenue is near the bottom, which the next two quarters will show."),
]
cards = "".join(f'<div class="card" style="border-top:5px solid {c}"><h3 style="font-size:17px;text-transform:none;margin-bottom:6px">{t}</h3>'
                f'<div class="small" style="font-size:14.5px">{d}</div><div class="small" style="font-size:13.5px;margin-top:6px;color:{NAVY}"><b>{h}</b></div></div>' for t, c, d, h in reasons)
body = f"""<div class="cards3" style="margin-top:14px">{cards}</div>
<div class="row" style="margin-top:12px;font-size:14.5px">
  <div style="display:flex;align-items:center;gap:8px"><span style="width:16px;height:16px;background:{GREEN};display:inline-block;border-radius:3px"></span>Feeds clinical growth</div>
  <div style="display:flex;align-items:center;gap:8px"><span style="width:16px;height:16px;background:{BLUE};display:inline-block;border-radius:3px"></span>Cost and asset economics</div>
  <div style="display:flex;align-items:center;gap:8px"><span style="width:16px;height:16px;background:{ORANGE};display:inline-block;border-radius:3px"></span>Risk and timing</div>
</div>"""
S.append(slide("The case for keeping pharma", "Six reasons, each with the condition that has to be true", body,
             "Sources: FY2025 10-K (RaDaR litigation, data solutions, Trapelo sale, billing terms); quarterly releases (NGS growth); CVP analysis (28.5% CM ratio, company-wide). "
             "Pharma&rsquo;s own margin and collection time are not disclosed.", tag="Pharma briefing"))

# ---------- 5. Exit economics + gate ----------
gate = [("Pharma P&amp;L with costs split into avoidable vs. shared", "Contribution after avoidable costs &gt; 0"),
        ("Backlog and new orders vs. revenue billed", "Orders &ge; revenue for two quarters"),
        ("Clinical revenue from tests first run in trials", "Measurable and growing"),
        ("RaDaR trial pipeline and reimbursement path", "Funded studies with dates"),
        ("Revenue run-rate", f"Holds at &ge; ~${RUN:.0f}M")]
trs = "".join(f"<tr><td>{a}</td><td><b>{b}</b></td></tr>" for a, b in gate)
body = f"""
<div class="row" style="margin-top:14px">
  <div class="card" style="flex:1.05;padding:10px 14px">{img(IMG3)}</div>
  <div style="flex:1;display:flex;flex-direction:column;gap:12px">
    <table class="t" style="font-size:14.5px"><tr><th>Ask for (from Q1 2027)</th><th>Keep if</th></tr>{trs}</table>
    <div class="callout dark" style="font-size:15px;padding:12px 16px"><b>At the Q1 2027 gate:</b> all five met &rarr; keep and invest in the clinical-linked core.
    Some met &rarr; keep the core, cut the rest. None met &rarr; sell or close, as with Trapelo.</div>
  </div>
</div>
<div class="callout" style="margin-top:12px;font-size:15.5px"><b>Why not exit now:</b> at ${RUN:.0f}M of revenue, exit only adds EBITDA if it removes more than
${RUN*CMR:.0f}&ndash;{RUN*0.40:.0f}M of costs a year. Much of the cost is shared labs and G&amp;A that stay, so cut costs first and judge the remaining unit.</div>"""
S.append(slide("When to exit: the numbers have to say so", "Exit economics at the current run-rate (left) and the Q1 2027 decision gate (right)",
               body, f"Exit impact = avoidable fixed costs &minus; contribution lost (run-rate ${RUN:.0f}M &times; CM ratio). 28.5% is NEO&rsquo;s company-wide ratio; 40% shows a higher-margin case. "
               "Pharma&rsquo;s actual margin is not disclosed. Not investment advice.", tag="Pharma briefing"))

# ---------- 6. Sources ----------
vtab = "".join(f"<tr><td>{q}</td><td class='n'>{REPORTED_AD[q]:.1f}</td><td class='n'>{p:.1f}</td></tr>" for q, c, p, t in QD if q in REPORTED_AD)
ytab = "".join(f"<tr><td>{k}</td><td class='n'>{c:.1f}</td><td class='n'>{p:.1f}</td><td class='n'>{t:.1f}</td><td class='n'>{p/t*100:.1f}%</td></tr>" for k, (c, p, t) in YD.items())
ytab += f"<tr class='hl'><td>LTM Q3 2026</td><td class='n'>{LTM_TOT-LTM_PH:.1f}</td><td class='n'>{LTM_PH:.1f}</td><td class='n'>{LTM_TOT:.1f}</td><td class='n'>{LTM_PH/LTM_TOT*100:.1f}%</td></tr>"
body = f"""
<div class="row" style="margin-top:14px">
  <div style="flex:1.3"><table class="t" style="font-size:15px"><tr><th>$M</th><th class="n">Clinical</th><th class="n">Pharma</th><th class="n">Total</th><th class="n">Pharma share</th></tr>{ytab}</table>
    <div class="small" style="margin-top:10px">Clinical = clinical tests &times; average revenue per clinical test, as reported in each release. Pharma = total revenue &minus; clinical.</div></div>
  <div style="flex:1"><table class="t" style="font-size:15px"><tr><th>Check</th><th class="n">Reported</th><th class="n">Rebuilt</th></tr>{vtab}</table>
    <div class="small" style="margin-top:10px">Advanced Diagnostics revenue as reported in the 2024 releases vs. this method. Differences come from revenue per test rounded to whole dollars.</div></div>
</div>
<div class="card" style="margin-top:14px"><div class="small" style="font-size:14.5px"><b>Filings used:</b> NeoGenomics 8-K earnings releases (Ex. 99.1), Q1 2024&ndash;Q3 2026; FY2025 10-K
(Notes 3 and 7: Trapelo sale and impairments; goodwill and critical audit matter; restructuring; data solutions and pharma services revenue recognition). All from SEC EDGAR.
<b>Not disclosed:</b> pharma margin, costs, backlog, headcount, collection time and goodwill by reporting unit.</div></div>"""
S.append(slide("Sources and method", "How pharma revenue was rebuilt, and the check against reported figures", body, "Prepared November 2026. Not investment advice."))

html = f"""<!doctype html><html><head><meta charset="utf-8"><title>NEO Pharma Briefing</title>
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:ital,wght@0,400;0,600;0,700;0,800;1,400&display=swap" rel="stylesheet">
<style>{CSS}</style></head><body>{''.join(S)}</body></html>"""
(HERE / "neo-pharma.html").write_text(html, encoding="utf-8")
print(f"pharma FY23 {p23:.1f} FY24 {p24:.1f} FY25 {p25:.1f} LTM {LTM_PH:.1f} run {RUN:.1f}; clinical growth {(c25-c24)/c24*100:.1f}% "
      f"(pts of total {(c25-c24)/t24*100:.1f}) total {(t25-t24)/t24*100:.1f}%; writes {sum(vals):.1f}; yoy Q3'26 {yoy[chr(81)+'3'+chr(39)+'26']*100:.1f}")

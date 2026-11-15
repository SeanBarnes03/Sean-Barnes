"""NEO non-clinical (pharma) executive briefing, v2: charts + slides.

Run:  python3 build_pharma.py  -> pharma-*.png and neo-pharma.html next to this file
Then: node render.js <abs neo-pharma.html> <abs NEO_Pharma_Executive_Briefing.pdf> <png dir>

v2 answers the red-team review of v1: renamed to non-clinical, peer check against Labcorp,
organic clinical growth, sequential trend first, contract termination risk, exit hurdle as a
range including one-time costs, options beyond keep/exit, and the $34M of non-core charges taken
out of the pharma story.

Non-clinical revenue is not reported after Q3 2024. It is rebuilt as total revenue minus clinical
revenue, where clinical = clinical tests x average revenue per clinical test (both reported in
each quarterly earnings release). Check: Q1-Q3 2024, when NEO still reported Advanced
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

# ---------- data: NEO quarterly earnings releases (8-K Ex. 99.1) ----------
Q = [  # quarter, clinical tests, avg revenue per clinical test ($), total revenue ($M)
    ("Q1'24", 300827, 447, 156.240), ("Q2'24", 311670, 454, 164.502), ("Q3'24", 314564, 463, 167.824),
    ("Q4'24", 321679, 465, 172.000), ("Q1'25", 326163, 459, 168.035), ("Q2'25", 356630, 461, 181.330),
    ("Q3'25", 360774, 476, 187.797), ("Q4'25", 356136, 488, 190.170), ("Q1'26", 345679, 495, 186.672),
    ("Q2'26", 363498, 515, 201.656), ("Q3'26", 367279, 530, 209.254)]
QD = [(q, n * a / 1e6, r - n * a / 1e6, r) for q, n, a, r in Q]          # quarter, clinical, non-clinical, total
REPORTED_AD = {"Q1'24": 21.705, "Q2'24": 23.114, "Q3'24": 22.041}
Y = {"FY2023": (1165079, 425, 591.643), "FY2024": (1248740, 457, 660.566), "FY2025": (1399703, 471, 727.332)}
YD = {k: (n * a / 1e6, r - n * a / 1e6, r) for k, (n, a, r) in Y.items()}
c23, p23, t23 = YD["FY2023"]; c24, p24, t24 = YD["FY2024"]; c25, p25, t25 = YD["FY2025"]
C25_EXPATH = 1358969 * 476 / 1e6                      # FY2025 clinical excluding Pathline (Q4 2025 release)
PATHLINE = c25 - C25_EXPATH
ORG = C25_EXPATH - c24
LTM = sum(p for _, _, p, _ in QD[-4:]); LTM_TOT = sum(t for *_, t in QD[-4:])
RUN2 = sum(p for _, _, p, _ in QD[-2:]) * 2
yoy = {QD[i][0]: QD[i][2] / QD[i - 4][2] - 1 for i in range(4, len(QD))}
SEQ = QD[-1][2] / QD[7][2] - 1                         # Q4'25 -> Q3'26
NC_CHG25 = p25 / p24 - 1
LH_BLS, LH_BLS_ORG = 6.0, 4.0                         # Labcorp FY2025 10-K: BLS revenue +6.0%, organic +4.0%

# ---------- chart style ----------
for f in ["/usr/share/fonts/opentype/inter/Inter-Regular.otf", "/usr/share/fonts/opentype/inter/Inter-Bold.otf",
          "/usr/share/fonts/opentype/inter/Inter-SemiBold.otf"]:
    try:
        font_manager.fontManager.addfont(f)
    except Exception:
        pass
plt.rcParams.update({"font.family": "Inter", "font.size": 12, "axes.edgecolor": "#B8C0CF", "axes.labelcolor": "#374151",
                     "xtick.color": "#4B5563", "ytick.color": "#4B5563"})

def tidy(a, axis="y"):
    a.spines["top"].set_visible(False); a.spines["right"].set_visible(False)
    a.grid(axis=axis, color="#E5E7EB", lw=0.8); a.set_axisbelow(True)

def png(fig, name):
    fig.savefig(HERE / name, dpi=200, bbox_inches="tight")
    b = io.BytesIO(); fig.savefig(b, format="png", dpi=200, bbox_inches="tight"); plt.close(fig)
    return base64.b64encode(b.getvalue()).decode()

def ttl(a, t):
    a.set_title(t, loc="left", fontsize=13.5, fontweight="bold", color=NAVY)

# Chart 1: quarterly non-clinical revenue, sequential first
fig, (a1, a2) = plt.subplots(1, 2, figsize=(12.4, 4.0), gridspec_kw={"width_ratios": [1.55, 1]})
xs = list(range(len(QD)))
a1.bar(xs, [p for _, _, p, _ in QD], color=[LBLUE if q.endswith("24") else ORANGE for q, *_ in QD], width=0.68)
for i, (q, c, p, t) in enumerate(QD):
    a1.text(i, p + 0.4, f"${p:.1f}M", ha="center", fontsize=10, fontweight="bold", color=NAVY)
a1.annotate("", xy=(10, QD[-1][2] + 2.3), xytext=(7, QD[7][2] + 2.3), arrowprops=dict(arrowstyle="->", color=RED, lw=1.8))
a1.text(8.5, QD[7][2] + 3.1, f"{SEQ*100:.0f}% in 3 quarters", ha="center", fontsize=11, fontweight="bold", color=RED)
a1.axvline(7.5, color=GREY, lw=1, ls=":")
a1.text(7.55, 25.6, "Trapelo sold\n31 Dec 2025", fontsize=9.5, color=GREY, va="top")
a1.set_xticks(xs); a1.set_xticklabels([q for q, *_ in QD], fontsize=10.5)
a1.set_ylim(0, 27); a1.set_ylabel("Non-clinical revenue ($M)")
ttl(a1, "Still falling quarter to quarter")
tidy(a1)
yq = list(yoy.keys()); yv = [yoy[k] * 100 for k in yq]
a2.bar(range(len(yq)), yv, color=[RED if v < -20 else ORANGE for v in yv], width=0.62)
for i, v in enumerate(yv):
    a2.text(i, v - 2.2, f"{v:.0f}%", ha="center", fontsize=10, fontweight="bold", color=NAVY)
a2.set_xticks(range(len(yq))); a2.set_xticklabels(yq, fontsize=10)
a2.set_ylim(-34, 3); a2.axhline(0, color=GREY, lw=1); a2.set_ylabel("Change vs. same quarter last year (%)")
ttl(a2, "Year-on-year easing = smaller base")
tidy(a2); fig.tight_layout()
IMG1 = png(fig, "pharma-trend.png")

# Chart 2: peer check + growth bridge
fig, (a1, a2) = plt.subplots(1, 2, figsize=(12.4, 3.35), gridspec_kw={"width_ratios": [1, 1.25]})
labs = ["Labcorp pharma services\n(BLS), organic", "Labcorp pharma services\n(BLS), reported", "NEO non-clinical"]
vals = [LH_BLS_ORG, LH_BLS, NC_CHG25 * 100]
a1.barh(range(3), vals, color=[NAVY, LBLUE, RED], height=0.56)
for i, v in enumerate(vals):
    a1.text(v + (0.8 if v > 0 else -0.8), i, f"{v:+.1f}%", va="center", ha="left" if v > 0 else "right", fontsize=12, fontweight="bold", color=NAVY)
a1.set_yticks(range(3)); a1.set_yticklabels(labs, fontsize=10.5); a1.invert_yaxis()
a1.axvline(0, color=GREY, lw=1); a1.set_xlim(-32, 12); a1.set_xlabel("FY2025 revenue change (%)")
ttl(a1, f"A {LH_BLS_ORG - NC_CHG25*100:.0f}-point gap to a peer")
tidy(a1, "x")
steps = [("FY2024", 0, t24, NAVY), ("Clinical,\norganic", t24, t24 + ORG, GREEN), ("Pathline\n(acquired)", t24 + ORG, t24 + ORG + PATHLINE, LGREEN),
         ("Non-clinical", t24 + ORG + PATHLINE, t25, RED), ("FY2025", 0, t25, NAVY)]
for i, (lab, s, e, col) in enumerate(steps):
    lo_, hi_ = sorted((s, e))
    a2.bar(i, hi_ - lo_, bottom=lo_, color=col, width=0.62)
    a2.text(i, hi_ + 5, (f"{e-s:+.1f}" if s else f"${e:.1f}M"), ha="center", fontsize=11.5, fontweight="bold", color=NAVY)
a2.set_xticks(range(5)); a2.set_xticklabels([s[0] for s in steps], fontsize=10.5)
a2.set_ylim(600, 780); a2.set_ylabel(r"\$M (axis starts at \$600M)")
ttl(a2, f"Growth: {(t25-t24)/t24*100:.1f}% reported, {ORG/c24*100:.1f}% organic clinical")
tidy(a2); fig.tight_layout()
IMG2 = png(fig, "pharma-cost.png")

# Chart 3: exit hurdle as a range
fig, a = plt.subplots(figsize=(7.4, 4.15))
x = [0, 45]
CMS = [(0.15, GREEN, ":"), (0.285, BLUE, "-"), (0.50, DORANGE, "--")]
for cm, col, ls in CMS:
    lost = LTM * cm
    a.plot(x, [v - lost for v in x], color=col, lw=2.4, ls=ls, label=f"Margin {cm*100:.1f}%: hurdle ${lost:.0f}M")
    a.scatter([lost], [0], color=col, s=50, zorder=5)
a.axhline(0, color="#6B7280", lw=1)
a.fill_between(x, 0, 32, color=GREEN, alpha=0.07); a.fill_between(x, -32, 0, color=RED, alpha=0.06)
a.text(1, 25, "Exit adds EBITDA (recurring)", color=GREEN, fontsize=11, fontweight="bold")
a.text(1, -29, "Exit destroys EBITDA", color=RED, fontsize=11, fontweight="bold")
a.set_xlim(0, 45); a.set_ylim(-32, 32)
a.set_xlabel("Fixed costs that leave with the business ($M / yr)"); a.set_ylabel("Change in adj. EBITDA ($M / yr)")
ttl(a, f"Exit hurdle: ${LTM*0.15:.0f}–{LTM*0.50:.0f}M, set by an unknown margin")
a.legend(loc="lower right", frameon=False, fontsize=10.5); tidy(a); fig.tight_layout()
IMG3 = png(fig, "pharma-exit.png")

def img(b64):
    return f'<img src="data:image/png;base64,{b64}" style="width:100%;display:block">'

TAG = "Non-clinical briefing"
S = []
# ---------- 1. Executive summary ----------
body = f"""
<div class="row" style="margin-top:12px">
  <div class="card" style="flex:1;border-top:5px solid {RED};padding:12px 18px">
    <h3 style="margin-bottom:6px">What the filings show</h3>
    <ul class="small" style="font-size:14.8px;margin:0;padding-left:18px;line-height:1.42">
      <li><b>Non-clinical revenue</b> (pharma services, data, UK lab, Trapelo until sold) fell from <b>${p23:.0f}M (2023) to ${LTM:.0f}M</b> over the last 12 months.</li>
      <li><b>Still falling:</b> {SEQ*100:.0f}% from Q4&rsquo;25 to Q3&rsquo;26. Smaller year-on-year declines mostly reflect a smaller base.</li>
      <li><b>Not just the market:</b> Labcorp&rsquo;s pharma services grew {LH_BLS_ORG:.0f}% organically in 2025; NEO&rsquo;s non-clinical fell {abs(NC_CHG25)*100:.0f}%.</li>
      <li><b>Fragile revenue:</b> most pharma contracts can be ended by the client immediately or on notice.</li>
    </ul>
  </div>
  <div class="card" style="flex:1;border-top:5px solid {GREEN};padding:12px 18px">
    <h3 style="margin-bottom:6px">What has to be proven to keep it</h3>
    <ul class="small" style="font-size:14.8px;margin:0;padding-left:18px;line-height:1.42">
      <li>Trial work turns into <b>clinical revenue</b> (no public evidence yet).</li>
      <li><b>RaDaR</b> has a funded trial path to reimbursement.</li>
      <li>The unit <b>covers the costs that would leave with it</b>: ${LTM*0.15:.0f}&ndash;{LTM*0.50:.0f}M, depending on its margin.</li>
      <li>Revenue has <b>stopped falling</b>: orders &ge; revenue billed for two quarters.</li>
    </ul>
  </div>
</div>
<div class="row" style="margin-top:12px">
  <div class="card" style="flex:1;border-top:5px solid {NAVY};text-align:center;padding:10px"><div class="kpi" style="color:{NAVY};font-size:26px">${LTM:.0f}M</div>
    <div class="small">Last 12 months, {QD[-1][2]/QD[-1][3]*100:.0f}% of Q3&rsquo;26 sales</div></div>
  <div class="card" style="flex:1;border-top:5px solid {RED};text-align:center;padding:10px"><div class="kpi" style="color:{RED};font-size:26px">{LH_BLS_ORG - NC_CHG25*100:.0f} pts</div>
    <div class="small">2025 growth gap to Labcorp pharma services</div></div>
  <div class="card" style="flex:1;border-top:5px solid {ORANGE};text-align:center;padding:10px"><div class="kpi" style="color:{DORANGE};font-size:26px">Q1 2027</div>
    <div class="small">Decision gate on the four tests above</div></div>
</div>
<div class="callout dark" style="margin-top:12px;font-size:16.5px"><b>Recommendation: resize now, decide at Q1 2027.</b> Cut costs that don&rsquo;t serve trial-to-clinical
work or RaDaR, and test partnering RaDaR or selling the UK lab. Finance to deliver a non-clinical P&amp;L split into avoidable and shared costs, plus backlog, by Q1 2027.
If the four tests fail, sell or close it.</div>"""
S.append(slide("Non-clinical: resize now, decide by Q1 2027", "Executive summary &middot; NeoGenomics pharma services and other non-clinical revenue", body,
               "Built from public filings only: NEO earnings releases Q1 2024&ndash;Q3 2026, FY2025 10-K; Labcorp FY2025 10-K. Non-clinical = total revenue &minus; clinical tests &times; revenue per test; "
               "within $0.2M of reported figures for Q1&ndash;Q3 2024. Not investment advice."))

# ---------- 2. Shrinking ----------
body = f"""
<div class="card" style="margin-top:12px;padding:10px 16px">{img(IMG1)}</div>
<div class="row" style="margin-top:12px">
  <div class="card" style="flex:1;border-top:5px solid {RED}"><div class="kpi" style="color:{RED};font-size:24px">{SEQ*100:.0f}% since Q4&rsquo;25</div>
    <div class="small">${QD[7][2]:.1f}M &rarr; ${QD[-1][2]:.1f}M. Part of this is Trapelo leaving; its revenue isn&rsquo;t disclosed.</div></div>
  <div class="card" style="flex:1;border-top:5px solid {ORANGE}"><div class="kpi" style="color:{DORANGE};font-size:24px">&minus;{(1-LTM/p23)*100:.0f}% since 2023</div>
    <div class="small">${p23:.1f}M &rarr; ${LTM:.1f}M last 12 months. Share of sales {p23/t23*100:.0f}% &rarr; {LTM/LTM_TOT*100:.0f}%.</div></div>
  <div class="card" style="flex:1;border-top:5px solid {GREY}"><div class="kpi" style="color:{GREY};font-size:24px">No bottom yet</div>
    <div class="small">Two quarters near $14.5M is too short a record, with a divestiture in between.</div></div>
</div>"""
S.append(slide("Non-clinical is still shrinking", "Quarterly non-clinical revenue (left) and year-on-year change (right), Q1 2024&ndash;Q3 2026",
               body, "Sources: NEO quarterly earnings releases; FY2025 10-K (Trapelo sale completed 31 Dec 2025). Non-clinical includes pharma services, oncology data licensing, "
               "UK laboratory work and Trapelo until sold; the mix is not disclosed.", tag=TAG))

# ---------- 3. Not just macro ----------
drivers = [("Market (pharma and biotech spending)", "Management&rsquo;s explanation", "Weak: a large peer grew"),
           ("International site closures (2024)", "Q3 2024 release", "Deliberate, not demand"),
           ("Lower RaDaR revenue", "Q3 2024 release", "Product-specific"),
           ("Trapelo sold (31 Dec 2025)", "FY2025 10-K", "Divestiture; affects 2026 only"),
           ("Share loss or pricing", "Not disclosed", "Untested")]
trs = "".join(f"<tr><td><b>{a}</b></td><td>{b}</td><td>{c}</td></tr>" for a, b, c in drivers)
body = f"""
<div class="card" style="margin-top:12px;padding:10px 16px">{img(IMG2)}</div>
<div class="row" style="margin-top:12px">
  <div style="flex:1.25"><table class="t" style="font-size:12.5px;line-height:1.15"><tr><th>Possible driver of the decline</th><th>Source</th><th>What it means</th></tr>{trs}</table></div>
  <div class="callout" style="flex:1;font-size:14.5px;padding:10px 16px"><b>Why it matters:</b> a market downturn recovers on its own; share loss and deliberate exits don&rsquo;t.
  The case for waiting depends on which it is, and NEO doesn&rsquo;t size any of the drivers. Clinical grew {ORG/c24*100:.1f}% organically; Pathline added {PATHLINE/c24*100:.1f} pts more.</div>
</div>"""
S.append(slide("The decline isn&rsquo;t just the market", "FY2025: NEO non-clinical vs. Labcorp pharma services (left); NEO revenue bridge (right)",
               body, f"Sources: Labcorp FY2025 10-K (Biopharma Laboratory Services revenue ${3098.2:,.1f}M, +6.0%, organic +4.0%; a far broader business, so a direction, not a precise benchmark); "
               "NEO Q4 2025 release (clinical tests and revenue per test excluding Pathline); NEO releases Q3 2024 and Q2 2025 (management commentary).", tag=TAG))

# ---------- 4. Hypotheses to test ----------
hyps = [("Trial work feeds clinical tests", "No public evidence. NGS growth (22&ndash;29%) is clinical and not linked to trial work in any filing.",
         "Clinical revenue from tests first run in trials, by year", "Med. affairs + finance"),
        ("RaDaR needs pharma trials", "RaDaR revenue was already falling here. 2025 litigation costs ($11.3M) included a settlement payment.",
         "Funded RaDaR studies, dates and reimbursement path", "R&amp;D + market access"),
        ("It covers costs that would leave with it", "Margin not disclosed; the company-wide 28.5% is driven by clinical.",
         "P&amp;L split into avoidable vs. shared costs", "Finance"),
        ("Data licensing grows at little extra cost", "Data revenue is not disclosed.", "Data revenue, contracts and renewal rate", "Data business lead"),
        ("It lowers dependence on insurers", "True for billing, but most contracts can be ended immediately or on notice.",
         "Backlog, cancellations, top-client concentration", "Pharma services lead"),
        ("Waiting will get a better price", "Assumes recovery the peer gap doesn&rsquo;t support. Trapelo sold for $2.5M plus up to $5M contingent.",
         "Indicative valuation of the whole unit and its parts", "Corp. development")]
trs = "".join(f"<tr><td><b>{a}</b></td><td>{b}</td><td>{c}</td><td>{d}</td></tr>" for a, b, c, d in hyps)
body = f"""
<div style="margin-top:12px"><table class="t" style="font-size:14px;line-height:1.3">
<tr><th style="width:230px">Reason to keep</th><th>What public data says</th><th style="width:260px">Test (data to bring by Q1 2027)</th><th style="width:150px">Owner</th></tr>{trs}</table></div>
<div class="callout dark" style="margin-top:12px;font-size:15.5px"><b>None of these is proven.</b> They are the reasons a keep decision would rest on. Each needs internal
data that leadership already has or can produce, so the gate can be met on time.</div>"""
S.append(slide("The case for keeping it: hypotheses, not facts", "Six reasons to keep the business, what the filings say, and how to test each",
               body, "Sources: NEO FY2025 10-K (revenue recognition: contracts terminable by clients; IP litigation costs; Trapelo sale terms); quarterly releases. "
               "Owners are suggested functions, not NEO&rsquo;s actual structure.", tag=TAG))

# ---------- 5. Options ----------
opts = [("A &middot; Keep as is", "Avoids exit costs and a possible goodwill loss", "Decline continues; fixed costs stay", "Only if all four tests pass", GREY),
        ("B &middot; Resize to the clinical-linked core", "Keeps trial work, RaDaR and data; cuts the rest", "Needs the P&amp;L to know what to cut", "Do now", GREEN),
        ("C &middot; Partner or license RaDaR", "Brings in trial funding; reduces NEO&rsquo;s spend", "Gives up part of the upside", "Test now", BLUE),
        ("D &middot; Sell or close the UK lab", "Removes a site and its fixed costs", "Loses ex-US trial capability", "Test now", BLUE),
        ("E &middot; Sell or close the whole unit", "Simplifies NEO; ends the drag", "One-time costs; goodwill write-off; low price now", "If tests fail at Q1 2027", RED)]
trs = "".join(f'<tr><td style="border-left:5px solid {c}"><b>{a}</b></td><td>{b}</td><td>{d}</td><td><b>{e}</b></td></tr>' for a, b, d, e, c in opts)
body = f"""
<div style="margin-top:12px"><table class="t" style="font-size:15px">
<tr><th style="width:290px">Option</th><th>For</th><th>Against</th><th style="width:200px">When</th></tr>{trs}</table></div>
<div class="callout" style="margin-top:12px;font-size:15.5px"><b>Recommended path: B now, C and D tested in parallel, E held as the fallback.</b> This doesn&rsquo;t depend on the
market recovering. It cuts what doesn&rsquo;t earn its keep and keeps the parts that might feed clinical growth.</div>"""
S.append(slide("Five options, not two", "Choices beyond keep or exit", body,
               "Option assessment is qualitative, based on public filings. Exit costs, UK lab economics and RaDaR partnering value are not disclosed.", tag=TAG))

# ---------- 6. Exit economics + gate ----------
gate = [("Non-clinical P&amp;L, avoidable vs. shared costs", "Contribution after avoidable costs &gt; 0"),
        ("Backlog and new orders vs. revenue billed", "Orders &ge; revenue for two quarters"),
        ("Clinical revenue from tests first run in trials", "Measurable and growing"),
        ("RaDaR studies and reimbursement path", "Funded, with dates")]
trs = "".join(f"<tr><td>{a}</td><td><b>{b}</b></td></tr>" for a, b in gate)
body = f"""
<div class="row" style="margin-top:12px">
  <div class="card" style="flex:1.05;padding:10px 14px">{img(IMG3)}</div>
  <div style="flex:1;display:flex;flex-direction:column;gap:10px">
    <table class="t" style="font-size:14px"><tr><th>Bring to the Q1 2027 gate</th><th>Keep if</th></tr>{trs}</table>
    <div class="callout" style="font-size:14px;padding:10px 14px"><b>Not in the chart, and all against exit:</b> severance, the Cambridge lease, contract wind-down, a likely
    goodwill write-off, and any clinical revenue that depends on pharma relationships.</div>
    <div class="callout dark" style="font-size:14px;padding:10px 14px"><b>Gate:</b> all four pass &rarr; keep and invest in the core. Some pass &rarr; option B plus C/D.
    None pass &rarr; option E.</div>
  </div>
</div>"""
S.append(slide("Exit only pays above an unseen hurdle", "Recurring exit economics at last-12-month revenue (left) and the Q1 2027 gate (right)",
               body, f"Exit impact = fixed costs that leave &minus; contribution lost (${LTM:.0f}M last-12-month revenue &times; margin). Margins of 15%, 28.5% (NEO company-wide) and 50% span plausible cases; "
               f"the unit&rsquo;s actual margin is not disclosed. At the Q2&ndash;Q3 2026 run-rate (${RUN2:.0f}M) each hurdle is ~$1M lower. Not investment advice.", tag=TAG))

# ---------- 7. Risks to this brief ----------
risks = [("Non-clinical &ne; pharma", "The residual includes data, UK lab work and Trapelo. Their mix is not disclosed."),
         ("Peer comparison is rough", "Labcorp&rsquo;s pharma services is ~50&times; larger and broader (early development, central labs)."),
         ("Exit margin unknown", "Every exit number depends on a margin estimate; the range runs from $9M to $30M."),
         ("Goodwill risk is unsized", "Both reporting units were tested in Q3 2025, likely for a company-wide reason. Goodwill by unit is not disclosed."),
         ("Public data only", "Leadership holds the unit P&amp;L, backlog and RaDaR plans. They can confirm or overturn this brief.")]
trs = "".join(f"<tr><td style='width:260px'><b>{a}</b></td><td>{b}</td></tr>" for a, b in risks)
yt = "".join(f"<tr><td>{k}</td><td class='n'>{c:.1f}</td><td class='n'>{p:.1f}</td><td class='n'>{t:.1f}</td></tr>" for k, (c, p, t) in YD.items())
yt += f"<tr class='hl'><td>Last 12 mo. to Q3&rsquo;26</td><td class='n'>{LTM_TOT-LTM:.1f}</td><td class='n'>{LTM:.1f}</td><td class='n'>{LTM_TOT:.1f}</td></tr>"
vt = "".join(f"<tr><td>{q}</td><td class='n'>{REPORTED_AD[q]:.1f}</td><td class='n'>{p:.1f}</td></tr>" for q, c, p, t in QD if q in REPORTED_AD)
body = f"""
<div class="row" style="margin-top:12px">
  <div style="flex:1.25"><table class="t" style="font-size:14px"><tr><th>Limitation</th><th>Effect</th></tr>{trs}</table></div>
  <div style="flex:1;display:flex;flex-direction:column;gap:10px">
    <table class="t" style="font-size:13.5px"><tr><th>$M</th><th class="n">Clinical</th><th class="n">Non-clinical</th><th class="n">Total</th></tr>{yt}</table>
    <table class="t" style="font-size:13.5px"><tr><th>Check</th><th class="n">Reported</th><th class="n">Rebuilt</th></tr>{vt}</table>
  </div>
</div>
<div class="small" style="margin-top:10px">Clinical = clinical tests &times; average revenue per clinical test, as reported each quarter. Non-clinical = total &minus; clinical.
Rebuilt figures differ from reported 2024 Advanced Diagnostics revenue by up to $0.2M because revenue per test is rounded to whole dollars.</div>"""
S.append(slide("Limits of this brief, sources and method", "What could change the conclusion, and how the numbers were built", body,
               "Sources: SEC EDGAR: NEO 8-K earnings releases (Ex. 99.1) Q1 2024&ndash;Q3 2026; NEO FY2025 10-K; Labcorp FY2025 10-K. Prepared November 2026. Not investment advice."))

html = f"""<!doctype html><html><head><meta charset="utf-8"><title>NEO Non-clinical Briefing</title>
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:ital,wght@0,400;0,600;0,700;0,800;1,400&display=swap" rel="stylesheet">
<style>{CSS}</style></head><body>{''.join(S)}</body></html>"""
(HERE / "neo-pharma.html").write_text(html, encoding="utf-8")
print(f"slides {len(S)}; p23 {p23:.1f} p24 {p24:.1f} p25 {p25:.1f} LTM {LTM:.1f} run2 {RUN2:.1f} seq {SEQ*100:.1f} nc25 {NC_CHG25*100:.1f} "
      f"org {ORG:.1f} ({ORG/c24*100:.1f}%) pathline {PATHLINE:.1f} hurdles {LTM*.15:.1f}/{LTM*.285:.1f}/{LTM*.5:.1f}")

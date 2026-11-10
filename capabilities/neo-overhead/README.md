# NEO overhead

Deep dive on slides 5 and 6 of `NEO_Cost_Breakdown__Savings_v2`: what makes up NeoGenomics'
corporate overhead (G&A), and why its SG&A runs so far above other labs.

**Deliverable:** [NEO_Overhead_Deep_Dive.pdf](NEO_Overhead_Deep_Dive.pdf), 12 slides in the same style as v2, opening with an
executive summary. Brief: [neo-overhead-brief.md](../../docs/briefs/neo-overhead-brief.md). Sources:
[data/neo-overhead-sources.md](../../data/neo-overhead-sources.md).

Every figure is reported in a 10-K, the 2026 proxy or an earnings release, or is arithmetic on
reported figures. The one thing that isn't public is G&A by function, and the deck says so.

## What it finds

- **G&A of $273.3M (37.6% of sales) is only $176M of real back office.** $67.9M is non-cash
  (stock pay $34.3M, depreciation $20.8M, amortization $12.8M), $22.0M is "one-time"
  (litigation, deals, CEO change) and $7.3M is executive and board cash pay.
- **The 30.6-point SG&A gap to Quest ($223M):** 10.2 points are stock pay, one-offs and
  depreciation; 20.4 points are recurring cash overhead that Quest's disclosures can't split further.
- **Against specialty labs, total SG&A is below the median** (50.2% vs. 55.4%), and so are
  selling (12.6% vs. 32.3%) and stock pay (5.7% vs. 10.4%).
- **G&A is the outlier:** 31.1% of sales excluding stock pay and amortization, against a 24.3%
  peer median. That's 6.8 points (~$50M), or 3.8 points (~$28M) after NEO's 2025 one-offs.
- **Collections:** 80 days of sales in receivables, against 48 at Quest and a 46-day specialty median.

## Files

| File | What it is |
|---|---|
| `pull_xbrl.py` | Pulls FY2025 line items for NEO and peers from SEC XBRL company facts |
| `pull_10k.py` | Downloads each FY2025 10-K as text, for the line items XBRL doesn't carry |
| `build_deck.py` | Holds every number and builds the HTML. Run `python3 build_deck.py` |
| `neo-overhead-deck.html` | The generated slides (1334x750 each) |
| `render.js` | Playwright: `node render.js <abs html> <abs pdf> <png dir>` |
| `NEO_Overhead_Deep_Dive.pdf` | Rendered deck |

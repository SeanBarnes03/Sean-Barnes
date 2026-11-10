# NEO overhead

Deep dive on slides 5 and 6 of `NEO_Cost_Breakdown__Savings_v2`: what makes up NeoGenomics'
corporate overhead (G&A), and why its SG&A runs so far above other labs.

**Deliverable:** [NEO_Overhead_Deep_Dive.pdf](NEO_Overhead_Deep_Dive.pdf), 12 slides in the same style as v2.
Brief: [neo-overhead-brief.md](../../docs/briefs/neo-overhead-brief.md). Sources and method:
[data/neo-overhead-sources.md](../../data/neo-overhead-sources.md).

## What it finds

- **G&A of $273.3M (37.6% of sales) is only $176M of real back office.** $67.9M is non-cash
  (stock pay ~$34.7M, depreciation ~$20.3M, amortization $12.9M), $22.1M is "one-time"
  (litigation, deals, CEO change) and $7.3M is executive cash pay and board fees.
- **The 30.7-point SG&A gap to Quest ($223M) is mostly not cash you can cut.** About 10 points
  are accounting and one-offs, about 17 points are the specialty business model (sales force,
  billing complexity, fixed costs on a small base), and about 3.5 points ($25M) are excess.
- **Against specialty labs NEO's total SG&A is low; its G&A is the outlier:** 37.6% against a
  27.4% median.
- **The recurring cash gap is about 4 points, roughly $27M:** cash G&A of 25.2% of sales
  against about 21% at Castle. That matches the v2 deck's ~$24M "overhead under 30%" prize.

## Files

| File | What it is |
|---|---|
| `build_deck.py` | Holds every number and builds the HTML. Run `python3 build_deck.py` |
| `neo-overhead-deck.html` | The generated slides (1334x750 each) |
| `render.js` | Playwright: `node render.js <abs html> <abs pdf> <png dir>` |
| `NEO_Overhead_Deep_Dive.pdf` | Rendered deck |

Every figure marked **EST** on a slide is an estimate. The method is on that slide and on the notes slide.

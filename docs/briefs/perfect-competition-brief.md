---
type: brief
engagement: perfect-competition
capability: marginal-analysis
date: 2026-08-26
status: committed          # committed | superseded
hypothesis: "About 5 tomato, 10 carrot and 20 mesclun beds — tomato labor is 10% per bed versus 2.5% and 1.25%, and I expect that to counter a 3-4x revenue advantage within a few beds"
---

# Perfect competition — engagement brief

## The problem

**What is being decided:** how many beds of each of the three crops to plant across the
64 beds available until we find the P=MC tipping point where we lose money.

**By whom:** The farmer.  She can't control the demand or the price, the only factor she can control is the supply of what she grows.  

**What happens if it is decided badly:** too much or too little will waste time/money/resources.  Once planted these are sunk costs and can't be replaced.  

**What is fixed:**

- Season: 36 weeks
- Fixed costs: $20,000
- Beds: 64 (16 beds × 4 plots)
- The farmer: $50,000 a season, half her time in the field — 720 field hours at an
  implied $34.72/hr
- Temporary workers: up to 4 at $25,000 each, 1,440 hours each, $17.36/hr
- Prices below are set by the market and cannot be changed

| Crop | Price $/bed | Fertilizer $/bed | Labor hrs/wk/bed | Diminishing returns | Max beds |
|---|---|---|---|---|---|
| Tomatoes | 8,800 | 880 | 2.50 | 10.00% / bed | 20 |
| Carrots | 2,094 | 440 | 0.833 | 2.50% / bed | 20 |
| Mesclun | 2,700 | 880 | 1.25 | 1.25% / bed | 30 |

**What is chosen:** how many beds of each crop to plant.

**What limits the choice:** each crop's own bed cap — 20 tomatoes, 20 carrots, 30 mesclun — no more than 64 beds in total, and no more than 4 temporary workers on top of the farmer's own 720 field hours.

## What I am assuming

- Labor is the resource I am economizing on. Plant more of what costs less in labor to
  enhance ROI.
- Weather or external factors will not change the planned yields. With more time, test
  different configurations of crops and contingency plans if external factors did change
  yields or workers were not available.
- The wage that prices an added bed of labor is not settled by the case. The farmer's own
  time implies $34.72/hr and a temporary worker $17.36/hr, and the two do not give the
  same answer. I am carrying this into the Stage 1.2 spec as an assumption to state
  before anything is built.

## Hypothesis

I expect about **5 tomato beds, 10 carrot beds and 20 mesclun beds** — 35 of the 64
available — since mesclun and carrots take half or less the hours of labor compared to
tomatoes.

Tomatoes earn the most, but become more expensive to plant, so I went with more mesclun and carrot for that reason, and both are cheaper to produce. 

## How I would know I was wrong

If we had beds left over, I was too conservative in my estimate. I left too much on the table to achieve P=MC.  Or if estimated number of bed fails to reach P=MC.  

---

-Reasoning stress-tested with Claude (Anthropic, 2026); written by me.

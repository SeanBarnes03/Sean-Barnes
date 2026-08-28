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

> **[Sean to decide — new point, I did not raise this earlier]** "The only factor she can
> control is the supply of what she grows" reads as if she controls market supply. Under
> perfect competition she is too small to move it — she chooses *her own output*, which
> is not the same thing. The 8/24 critique flagged a supply-vs-demand framing as
> inconsistent with price-taking and it has come back. Your call whether to reword.
> Bullets: she is one small seller among many; the price is given to her at any quantity
> she could grow; growing less will not raise it, growing more will not lower it.


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

> **[Sean to write — the one that matters, 3 or 4 sentences]** Four things this paragraph
> currently does not do. Fixing 1 and 2 is where the points are.
>
> 1. **Carrots vs mesclun still inverts your own logic.** You predict 20 mesclun and 10
>    carrots, but carrots take 0.833 hrs/wk/bed against mesclun's 1.25 — carrots are the
>    cheaper crop in labor. Your assumption says plant more of what costs less in labor.
>    Say why mesclun anyway. Bullets you had before: mesclun earns $2,700 a bed against
>    carrots' $2,094, and escalates at 1.25%/bed against carrots' 2.5% — half the rate —
>    so it stays profitable further up its range.
> 2. **Nothing is multiplied out.** Adam took 2 points for this. The numbers are in your
>    own table: tomatoes $8,800 against $2,700 and $2,094 (3-4x); tomato beds start at
>    2.50 hrs/wk against 1.25 and 0.833; each added tomato bed raises labor on *every*
>    tomato bed by 10%, against 1.25% and 2.5%. Say what compounding at 10% does.
> 3. **It restates the assumption instead of deriving from it.** "Plant what costs less in
>    labor" is the assumption; "I went with more mesclun and carrot, both cheaper to
>    produce" is the same sentence again. Nothing on the page produces the number *five*.
> 4. **29 beds go unplanted with no reason given.** You predict 35 of 64. Bullet you had
>    before: all three crops pass the point where marginal cost exceeds price before they
>    hit their caps, so those beds are not worth planting rather than merely unused.


## How I would know I was wrong

If we had beds left over, I was too conservative in my estimate. I left too much on the table to achieve P=MC.  Or if estimated number of bed fails to reach P=MC.  

> **[Sean to write — 1 or 2 sentences, plus one clarification]**
>
> - **Clause 1 may already be true on the day you write it.** You predict 35 of 64 beds —
>   you *are* leaving 29 beds over. As written your own hypothesis trips your own
>   falsifier. If you mean "if the model plants more beds than I did," say that.
> - **Clause 2 is unclear.** "If estimated number of bed fails to reach P=MC" — name the
>   observation you would actually see in the model output.
> - **Neither clause tests the mechanism.** Both test the count. Bullet you had before,
>   which Adam called the harder and better version and the one most likely to fire: if a
>   crop stops at its bed cap instead of where its marginal cost meets its price, then a
>   fence set that crop's level and not the economics — the opposite of what this brief
>   claims.


> **[Sean to decide — two one-word calls]**
>
> - **"About"** is still in the frontmatter and in the hypothesis line. Adam took a point
>   for it: "the numbers are precise enough to be checked, so let them be."
> - **The frontmatter says "tomato labor is 10% per bed."** Tomato labor is 2.50 hrs/bed;
>   10% is the escalation rate. As written the first line a reader sees misstates your own
>   mechanism.

---

-Reasoning stress-tested with Claude (Anthropic, 2026); written by me.

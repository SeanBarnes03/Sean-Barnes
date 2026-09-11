---
type: analysis
engagement: perfect-competition
capability: marginal-analysis
date: 2026-09-10
status: draft
---

# Perfect competition — what the model found

The question was how many beds of each crop to plant. Based on the model I recommend the optimum mix as 10 tomato, 20 carrot, 30 mesclun beds. Projected season profit of $42,762.  

## Why tomatoes stop at 10 beds

Tomato MC at bed 10 is $8,249 (`MCSchedules F17`) and at bed 11 is $9,391
(`MCSchedules F18`). The price of $8,800 sits between the two. Tomatoes planted in
bed 11 do not pay for themselves, while the other two crops continue to pay for
themselves up to 20 and 30 beds.

![Tomato marginal cost against price](figures/tomato-mc-vs-price.png)


## Which constraints bind, and what relaxing one is worth

Carrot MC at bed 21 is $1,741.51 (`MCSchedules P28`) against a price of $2,094 — a
gap of $352.49. Mesclun MC at bed 31 is $2,453.53 (`MCSchedules Z38`) against
$2,700 — a gap of $246.47. Marginal cost for both crops is still under price at the
cap, so the cap stopped them rather than the economics.

Each shadow price is computed two ways, and the two agree to the cent:

| | Cost engine route | PRICE − MC route |
|---|---|---|
| Carrot bed cap | $352.49 (`Checks C19`) | $352.49 (`Checks B21`) |
| Mesclun bed cap | $246.47 (`Checks C20`) | $246.47 (`Checks B22`) |

The plan uses 60 of the 64 available beds (`Optimization B10`) and 4,557.2 of the
5,760 available temporary hours (`Optimization B11`).

<!-- TODO (content): the temp-worker line as written states the trap rather than
     resolving it. Under a SLACK heading, "4 of 4 workers" reads as binding. The
     headcount cell (Optimization B13) reads 4 because ROUNDUP turns 3.17 into 4;
     the constraint Solver enforces is hours, and 1,203 of them are spare. Both
     halves need to be in the sentence. Then: what follows for spending — what is
     worth money to acquire, and what is not. -->

<!-- TODO (content): the standalone-vs-optimum point — carrot MC crosses price around
     bed 11 and mesclun around bed 7 in the charts below, yet the plan fills both to
     their caps. Explain why that is not a contradiction.

     TODO (content): a sentence pointing at each of the two charts, making a claim.

     TODO (content): the shadow prices as advice — which ground is worth buying
     first, and what a bed of it is worth. -->

![Carrot marginal cost against price](figures/carrots-mc-vs-price.png)

![Mesclun marginal cost against price](figures/mesclun-mc-vs-price.png)

## The tomato marginal cost dip at bed 6

The dip is caused by hours going up while cost goes down. Tomato labor hours at bed
4 are 527.1 (`MCSchedules B11`), within the farmer's 720. At bed 5 they are 724.7
(`B12`), so the farmer's hours run out inside that bed. At bed 6 they are 956.6
(`B13`), and every hour past 720 is temp labor. Marginal cost at bed 5 is $7,661
(`F12`) and at bed 6 it falls to $4,906 (`F13`). The marginal wage fell from $34.72
to $17.36 as temp workers took over from the farmer's more costly labor.  The farmers hours ran out at 720 which cut the labor cost in half from $34.72 to $17.36.  This is why the curve falls.   In this case both inputs changed.  At bed 6 the hours went up but the wage was cut in half.  

## Why grow crops that lose money on their own

The farmer pays $20,000 in fixed costs (`Inputs B15`). That is paid no matter what
is planted.  In this case average variable cost is less than price for every crop:

| Crop | Total cost | Beds | AVC | Price | |
|---|---|---|---|---|---|
| Tomatoes | $61,827 (`MCSchedules E17`) | 10 | $6,182.72 | $8,800 | under |
| Carrots | $38,369 (`MCSchedules O27`) | 20 | $1,918.45 | $2,094 | under |
| Mesclun | $72,922 (`MCSchedules Y37`) | 30 | $2,430.74 | $2,700 | under |

conversely, carrots and mesclun output alone lose money when the $20,000 fixed costs are factored in:

| Crop | Revenue | Variable + $20,000 | Standalone |
|---|---|---|---|
| Tomatoes | $88,000 | $81,827 | +$6,173 |
| Carrots | $41,880 | $58,369 | −$16,489 |
| Mesclun | $81,000 | $92,922 | −$11,922 |

however, carrots and mesclun still make money that can be put toward the fixed costs, that is why its worth it to plant crops that lose money on their own.  All three together contribute to paying fixed costs.  Better than empty beds which contribute nothing.  (see tab AVC tab in model)

## Against my Stage 1 hypothesis

I predicted a 5 / 10 / 20 mix, thinking the more expensive tomatoes would reach
P = MC before the two less costly crops, while saving on cheaper labor for the
carrot and mesclun beds. The model returned 10 / 20 / 30 — I was under by 5, 10 and
10 beds respectively.  Both my falsifiers were wrong.  Carrots and Mesclun hit their caps.  Tomatoes hit 10 beds not 8.  Labor as a driving factor was incorrect - 1,203 hours left over.  I  did call that tomatoes would get too expensive to plant before it hit MC.  

---

-Drafted with help from Claude (Anthropic, 2026); reviewed and edited by me.

---
type: spec
engagement: perfect-competition
capability: marginal-analysis
date: 2026-08-30
status: draft          # draft | committed | superseded
---

# Marginal analysis model — specification

## 1. Inputs

### Per-crop inputs

| Name | Tomatoes | Carrots | Mesclun | Unit | Source |
|---|---|---|---|---|---|
| `MAX_BEDS` | 20 | 20 | 30 | beds | case scenario |
| `PRICE_PER_BED` | 8,800 | 2,094 | 2,700 | $ per bed per season | case scenario — "Price $/bed" |
| `HRS_PER_BED_WEEK` | 2.50 | 5/6 | 1.25 | hours per bed per week | case scenario — carrots shown as 0.833, stored as 5/6 |
| `FERTILIZER_PER_BED` | 880 | 440 | 880 | $ per bed | case scenario |
| `DIM_PCT` | 10.00% | 2.50% | 1.25% | % per additional bed | case scenario |

### Farm-level inputs

| Name | Value | Unit | Source |
|---|---|---|---|
| `WEEKS` | 36 | weeks per season | case scenario |
| `FIXED_COSTS` | 20,000 | $ per season | case scenario |
| `TOTAL_BED_CAP` | 64 | beds (16 beds x 4 plots) | case scenario |
| `FARMER_SALARY` | 50,000 | $ per season | case scenario |
| `FARMER_FIELD_HRS` | 720 | hours per season | case scenario |
| `FARMER_RATE` | `= FARMER_SALARY / (2 * FARMER_FIELD_HRS)` | $ per hour | derived — the case's "implied $34.72/hr" |
| `TEMP_COST_EACH` | 25,000 | $ per worker per season | case scenario |
| `TEMP_HRS_EACH` | 1,440 | hours per worker per season | case scenario |
| `TEMP_RATE` | `= TEMP_COST_EACH / TEMP_HRS_EACH` | $ per hour | derived — the case's "$17.36/hr" |
| `MAX_TEMPS` | 4 | workers | case scenario |

### Decision variables

Chosen by the optimizer, not given by the case. Integers, at least zero.

| Name | Unit | Bounded by |
|---|---|---|
| `BEDS_TOMATO` | beds | `MAX_BEDS` tomatoes = 20 |
| `BEDS_CARROT` | beds | `MAX_BEDS` carrots = 20 |
| `BEDS_MESCLUN` | beds | `MAX_BEDS` mesclun = 30 |

`FARMER_RATE` and `TEMP_RATE` are **derived, not typed**. The case calls $34.72 an
"implied" rate; it is $50,000 over the farmer's 1,440 season hours, and $17.36 is
$25,000 over 1,440. Typing the rounded figures instead shifts season profit by
about $13 and fails the tolerance in Section 4. For the same reason carrot labor is
stored as 5/6 hours per bed-week, which the case displays as 0.833.

`PRICE_PER_BED` is the P in P = MC. The farm is a price taker: P is the same for
the first bed and the last, and does not vary with quantity planted.

---

## 2. Structure

Five sheets. Sheet names carry no spaces: Excel's Solver add-in on macOS mishandles
unquoted sheet references containing spaces and raises a VBA 1004 error.

- **Inputs** — every named range in Section 1, one cell each, with its unit in an
  adjacent label cell. Nothing calculated here.
- **CostStructure** — total labor hours, farmer hours used, temp hours used,
  temp workers required, farmer labor dollars, temp labor dollars, the blended
  labor rate, fertilizer cost, and total cost, at the current bed counts.
- **MCSchedules** — one block per crop, q = 0 through that crop's
  `MAX_BEDS`. Columns: q, labor hours, labor cost, fertilizer cost, total cost,
  marginal cost, and `PRICE_PER_BED` for comparison.
- **Optimization** — the three decision variables, season profit as the objective,
  and one cell per constraint in 3.12 showing PASS or FAIL.
- **Checks** — one row per validation rule in Section 4, each showing its required
  value, the value the workbook produced, and PASS or FAIL.

---

## 3. Calculation logic

### 3.1 Labor hours (the engine)

    LABOR_HRS(q) = q * HRS_PER_BED_WEEK * WEEKS * (1 + DIM_PCT)^q
One more bed raises the labor hours required by every bed of that crop, not just
the new one — pest pressure spreads, harvest windows collide, walking time grows.

Do not remove or simplify the `(1 + DIM_PCT)^q` term. Without it labor hours grow
in a straight line with beds, every bed costs the same as the last, marginal cost
is flat, and the model can never find a stopping point.

### 3.2 What the diminishing-returns rate acts on

`DIM_PCT` multiplies **labor hours**, as written in 3.1. It does not reduce yield,
price, or revenue.

Some versions of the case data table label `DIM_PCT` a "marginal yield loss
factor". That wording is not what this model implements. Revenue per bed stays at
`PRICE_PER_BED` regardless of how many beds are planted.

### 3.3 Revenue

    SEASON_REVENUE = BEDS_TOMATO * PRICE_PER_BED(tomato)
                   + BEDS_CARROT * PRICE_PER_BED(carrot)
                   + BEDS_MESCLUN * PRICE_PER_BED(mesclun)

Revenue **per bed** is constant — the 20th tomato bed earns the same $8,800 as the
first. Nothing reduces it. Total revenue therefore rises in a straight line with
beds.

### 3.4 Fertilizer cost

    FERTILIZER_COST = BEDS_TOMATO * FERTILIZER_PER_BED(tomato)
                    + BEDS_CARROT * FERTILIZER_PER_BED(carrot)
                    + BEDS_MESCLUN * FERTILIZER_PER_BED(mesclun)

Fertilizer is linear in beds. `DIM_PCT` does not affect it — the 20th tomato bed
costs the same $880 as the first.

### 3.5 Labor costing — consumption order

    TOTAL_LABOR_HRS = LABOR_HRS(BEDS_TOMATO, tomato)
                    + LABOR_HRS(BEDS_CARROT, carrot)
                    + LABOR_HRS(BEDS_MESCLUN, mesclun)

    FARMER_HRS_USED = MIN(TOTAL_LABOR_HRS, FARMER_FIELD_HRS)
    TEMP_HRS_USED   = MAX(0, TOTAL_LABOR_HRS - FARMER_FIELD_HRS)

The farmer's `FARMER_FIELD_HRS` are always consumed first. Temporary workers cover
only the remainder. Temporary hours are never used while the farmer has field
hours left.

### 3.6 Labor costing — how the farmer is charged

    FARMER_LABOR_COST = FARMER_HRS_USED * FARMER_RATE

The farmer is labor, not a fixed cost. She is paid `FARMER_SALARY` ($50,000) for
1,440 hours, of which only `FARMER_FIELD_HRS` (720) are field hours. The model
charges her field hours at `FARMER_RATE`, so her full-season field labor is
720 x $34.72 = $25,000.

The remaining $25,000 of her salary buys non-field time — admin, marketing,
paperwork — which does not change with the number of beds planted. It is not
charged as crop labor, and it is **not** added to `FIXED_COSTS`.

### 3.7 Labor costing — how temporary workers are charged

    TEMP_LABOR_COST = TEMP_HRS_USED * TEMP_RATE

Temporary labor is charged for the hours actually used, not as a lump sum per
worker hired. A plan needing 400 temp hours is charged 400 x $17.36 = $6,944, not
the full `TEMP_COST_EACH` of $25,000.

`TEMP_COST_EACH` and `TEMP_HRS_EACH` are used only to derive `TEMP_RATE` and to
size the worker cap in 3.8. They are not charged directly.

### 3.8 Number of temporary workers required

    TEMPS_REQUIRED = ROUNDUP(TEMP_HRS_USED / TEMP_HRS_EACH, 0)

Any fraction is rounded up: you cannot hire part of a person, so needing any part
of another worker's season means hiring another worker.

If `TOTAL_LABOR_HRS` is at or below `FARMER_FIELD_HRS`, `TEMP_HRS_USED` is zero and
`TEMPS_REQUIRED` is 0.

The plan fails if `TEMPS_REQUIRED` exceeds `MAX_TEMPS` (4).

The optimizer constrains this cap in its smooth form,
`TEMP_HRS_USED <= MAX_TEMPS * TEMP_HRS_EACH` (5,760 hours), which is exactly
equivalent — `ROUNDUP(h / 1440) <= 4` holds precisely when `h <= 5760`. GRG
Nonlinear assumes smooth functions, and a step function in a constraint makes it
stall. `TEMPS_REQUIRED` remains the reported headcount and is checked in the
workbook.

`TEMPS_REQUIRED` is a headcount used only for the constraint check. Cost is always
computed from `TEMP_HRS_USED` per 3.7, never from this count.

### 3.9 Blended labor rate for the P&L

    TOTAL_LABOR_COST = FARMER_LABOR_COST + TEMP_LABOR_COST
    BLENDED_RATE     = TOTAL_LABOR_COST / TOTAL_LABOR_HRS

Dollars, not rates: `FARMER_LABOR_COST` and `TEMP_LABOR_COST` are each hours times
a rate, per 3.6 and 3.7. `TOTAL_LABOR_HRS` is all hours across all three crops,
farmer and temporary together, per 3.5.

Every crop's labor cost is its own hours times `BLENDED_RATE`. The
permanent-versus-temporary split is a farm-level fact and is never pushed down
into an individual crop's cost — no crop is charged "the farmer's hours" or "a
temp's hours".

### 3.10 Marginal cost

    MC(q) = TOTAL_COST(q) - TOTAL_COST(q-1)

where, for this schedule,

    TOTAL_COST(q) = labor cost at q beds + fertilizer cost at q beds

Labor cost at q beds follows 3.5 through 3.7 — the farmer's field hours first, then
temporary hours. `FIXED_COSTS` is excluded: it does not change with q and cancels
in the subtraction.

**Standalone** means the other two crops are held at **zero beds**, so the schedule
shows that crop's cost alone. Each schedule runs q = 0 through that crop's
`MAX_BEDS`, and `TOTAL_COST(0)` is zero.

The standalone P = MC point for a crop is the **first** crossing: the largest q such
that `MC(b)` is at or below that crop's `PRICE_PER_BED` for every bed b from 1 to q.
Equivalently, one less than the lowest q at which `MC(q)` first exceeds
`PRICE_PER_BED`.

State it this way rather than as "the largest q where `MC(q)` is below price".
`MC(q)` is not guaranteed to rise monotonically, so a later q can fall back below
price after the first crossing; taking the last such q would report the wrong
point.

This section defines how marginal cost is computed. It makes no claim about the
shape of the resulting curve.

### 3.11 Profit

    SEASON_PROFIT = SEASON_REVENUE - FERTILIZER_COST - TOTAL_LABOR_COST - FIXED_COSTS

`TOTAL_LABOR_COST` is counted once, as defined in 3.9 (`FARMER_LABOR_COST` +
`TEMP_LABOR_COST`). The per-crop labor figures produced by `BLENDED_RATE` are an
allocation of that same money for reporting, and are never added on top of it.

`FIXED_COSTS` is $20,000 and contains no part of `FARMER_SALARY`.

### 3.12 Optimization

Objective: maximize season profit.
Changing cells: `BEDS_TOMATO`, `BEDS_CARROT`, `BEDS_MESCLUN`.
Method: GRG Nonlinear, with the three bed counts constrained to integers and >= 0.
Constraints:
  - each crop's bed count is at most its own `MAX_BEDS`
  - the three bed counts sum to at most `TOTAL_BED_CAP`
  - temporary workers required is at most `MAX_TEMPS`

---

## 4. Validation rules

The workbook must compute each of these and report pass or fail.

### Acceptance criteria — published check figures

| Check | Required value |
|---|---|
| Optimal mix | Tomatoes 10 · Carrots 20 · Mesclun 30 (60 beds) |
| Season profit | $42,762 |
| Standalone P is approximately MC | Tomatoes ~10 beds · Carrots ~10 beds · Mesclun ~6 beds |

### Hand calculation

| Check | Required value |
|---|---|
| `LABOR_HRS(1)` for tomatoes | 1 x 2.50 x 36 x 1.10 = 99 hours |

### Structural rules

- No error cells anywhere in the workbook — no `#REF!`, `#DIV/0!`, `#NAME?`,
  `#VALUE!` or `#N/A`.
- Every calculated cell contains a formula referencing named ranges. No pasted
  values.
- Every input is a real named range carrying the unit stated in Section 1.
- Every constraint check in 3.12 is computed in the workbook and displays PASS.

### Tolerances

- Season profit passes within +/- $5 of $42,762, to absorb rounding in
  `FARMER_RATE` and `TEMP_RATE`.
- The optimal mix must match 10 / 20 / 30 exactly.
- A standalone P = MC point passes within +/- 1 bed of the stated value.
- "PASS" means the check cell displays the text PASS. This spec uses PASS and FAIL
  rather than colour, because the capability README already reserves green font for
  cross-sheet links.

---

## 5. Outputs

The model must report:

**The decision**
- Optimal bed counts for each crop — tomatoes, carrots, mesclun

**The evidence**
- Season profit
- The standalone P = MC point for each crop

**The audit trail**
- Total labor hours
- Farmer hours used and temporary hours used
- Temporary workers required
- The blended labor rate
- The full marginal cost schedule for each crop
- The q = 1 tomato hand-check cell (labor hours for one tomato bed)

**Rule status** — each shown as pass or fail
- Optimal mix equals 10 tomatoes / 20 carrots / 30 mesclun
- Season profit equals $42,762
- Standalone P = MC points are approximately 10 / 10 / 6 beds
- Temporary workers required is at most 4
- Each crop's bed count is within its own MAX_BEDS
- The three bed counts sum to at most 64
- q = 1 tomato equals 99 labor hours
- No error cells anywhere in the workbook
- Every calculated cell contains a formula

---

## 6. Audit findings

Five checks run against the workbook after it was built and solved in Excel.

**1. q = 1 by hand.** Calculated one tomato bed by hand: 1 x 2.50 x 36 x 1.10 = 99
hours, and the workbook returned 99. Without the `^q` term we would have gotten 90
instead of 99 — and the same missing term would flatten marginal cost in every
schedule, so the model would never find a stopping point.

**2. Farm Profit Lab cross-check.** I compared 6 versus 7 tomato beds. The lab gave
$59,974 and $54,388 against my $39,974 and $34,388 — $20,000 higher in both,
exactly the fixed costs the lab includes and my schedule excludes, so they cancel
and both give the same marginal cost of $5,586. The hand check only tests the
first bed; this one tests a bed in the middle of the curve, where a wrong labor
rate or a farmer-to-temp switchover at the wrong point would produce a wrong
marginal cost while q = 1 still looked perfect.

---

-Drafted with help from Claude (Anthropic, 2026); reviewed and edited by me.

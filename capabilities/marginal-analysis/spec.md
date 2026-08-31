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
| `REVENUE_PER_BED` | 8,800 | 2,094 | 2,700 | $ per bed per season | case scenario |
| `HRS_PER_BED_WEEK` | 2.50 | 0.833 | 1.25 | hours per bed per week | case scenario |
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
| `FARMER_RATE` | 34.72 | $ per hour | case scenario (implied) |
| `TEMP_COST_EACH` | 25,000 | $ per worker per season | case scenario |
| `TEMP_HRS_EACH` | 1,440 | hours per worker per season | case scenario |
| `TEMP_RATE` | 17.36 | $ per hour | case scenario (implied) |
| `MAX_TEMPS` | 4 | workers | case scenario |

---

## 2. Structure

>>   - Inputs
>>   - Cost structure
>>   - Marginal cost schedules (one per crop)
>>   - Optimization
>>   - Checks
>>   - price = marginal cost
>>   - tomatoes
>>   - mesclun
>>   - carrots
>>   - hours
>>   - workers
>>   - beds
>>   - weeks
>>   - total bed cap
>>   - farmer salary
>>   - farmer field hours
>>   - temp worker costs
>>   - temp hours each
>>   - max temps
>>   - q = 0 through each crop's MAX_BEDS
---

## 3. Calculation logic

### 3.1 Labor hours (the engine)

    LABOR_HRS(q) = q * HRS_PER_BED_WEEK * WEEKS * (1 + DIM_PCT)^q
>> one more bed raises the cost of all preceding beds.  Do not remove the exponential term, costs of each bed stays the same as before, marginal cost falls.  

### 3.2 What the diminishing-returns rate acts on

>> Revenue for tomato beds stays the same at $8,800 per bed no matter how many you plant.  Ignore the "yield loss" naming convention.  

### 3.3 Revenue

Revenue for the season is number of beds x revenue per bed.  Add up that number for tomatoes, carrots, and mesclun.
Revenue is constant from the first bed to the last bed.  

### 3.4 Fertilizer cost

Same as revenue.  Cost of fertilizer x number of beds.  Add up that number for tomatoes, carrots, and mesclun.  Cost of fertilizer is constant from first to last bed.  

### 3.5 Labor costing — consumption order

The farmer's hours are always consumed first. Temp worker only cover what's left over.

### 3.6 Labor costing — how the farmer is charged

Farmer is paid $50,000 to run the farm.  Fixed cost.  

### 3.7 Labor costing — how temporary workers are charged

>> TODO: if the model needs a partial worker's worth of hours, state whether the
>> cost is the full TEMP_COST_EACH or the hours actually used at TEMP_RATE.

### 3.8 Number of temporary workers required

>> TODO: state how the count of temporary workers is derived from hours, and how
>> partial workers are handled, so the "at most MAX_TEMPS" rule can be checked.

### 3.9 Blended labor rate for the P&L

>> TODO: define the blended rate and state which labor dollars and which labor
>> hours go into it. State that the permanent-vs-temporary split is a farm-level
>> fact and is not pushed down into individual crop costs.

### 3.10 Marginal cost

>> TODO: define the marginal cost of the qth bed as a change in total cost, not
>> as a shape. Do NOT write "marginal cost increases with quantity" — state the
>> mechanism and let the workbook produce whatever shape falls out.

### 3.11 Profit

>> TODO: state how season profit is calculated from revenue and all costs.

### 3.12 Optimization

Objective: maximize season profit.
Changing cells: the three bed counts.
Method: GRG Nonlinear, with the bed counts constrained to integers.
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

- No error cells anywhere in the workbook.
- Every calculated cell contains a formula. No pasted values.
- Every input is a real named range carrying the unit stated in Section 1.
- Every constraint check in 3.12 is computed in the workbook and displays green.

>> TODO: add any further validation rule you want the build held to.

---

## 5. Outputs

The model must report:

**The decision**
- Optimal bed counts for each crop — tomatoes, carrots, mesclun

**The evidence**
- Season profit
- The standalone P = MC point for each crop

**The audit trail**
- Temporary workers used
- The q = 1 tomato hand-check cell (labor hours for one tomato bed)

**Rule status** — each shown as pass or fail
- Optimal mix equals 10 tomatoes / 20 carrots / 30 mesclun
- Season profit equals $42,762
- Standalone P = MC points are approximately 10 / 10 / 6 beds
- Temporary workers used is at most 4
- q = 1 tomato equals 99 labor hours

---

## 6. Audit findings

>> Leave empty until after the build. Filled in during the audit stage:
>> what you checked, what you found, and what you did about it.
>> Minimum five checks: the q = 1 hand calculation, one intermediate marginal cost
>> cross-checked against the Farm Profit Lab, Solver run from 0/0/0 and again from
>> 20/0/0 with any path-dependence noted, the published check figures, and a
>> spot-check that calculated cells contain formulas rather than pasted values.

---

-Drafted with help from Claude (Anthropic, 2026); reviewed and edited by me.

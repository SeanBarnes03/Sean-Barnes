---
type: spec
engagement: perfect-competition
capability: marginal-analysis
date: 2026-08-30
status: draft          # draft | committed | superseded
---

# Marginal analysis model — specification

<!--
HOW TO USE THIS FILE
This is a scaffold, not a spec. Every ">> TODO" is a decision only you can make.
Write in your own words. Rough is fine. Delete these comments when you are done.
The test: could someone who has never seen this case build the workbook from
this document alone, with no other conversation?
-->

## 1. Inputs

Every input below is taken from the case scenario. Values are given; the names
are the contract — Section 3 refers to these names and never to cell addresses.

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

>> TODO: add any input you decide the model needs that is not listed above.

---

## 2. Structure

>> TODO: list every sheet or region of the workbook and one line on what it is for.
>> Suggested starting point — edit, rename, add, or delete as you see fit:
>>   - Inputs
>>   - Cost structure
>>   - Marginal cost schedules (one per crop)
>>   - Optimization
>>   - Checks
>>
>> Also state the range each marginal-cost schedule must cover
>> (e.g. "q = 0 through each crop's MAX_BEDS").

---

## 3. Calculation logic

Written in named ranges. No cell addresses anywhere in this section.

### 3.1 Labor hours (the engine)

    LABOR_HRS(q) = q * HRS_PER_BED_WEEK * WEEKS * (1 + DIM_PCT)^q

>> TODO: state in one sentence what the (1 + DIM_PCT)^q term represents and what
>> it does to the model. This is the sentence that stops a builder from
>> simplifying it away.

### 3.2 What the diminishing-returns rate acts on

>> TODO — RESOLVE THIS CONFLICT. The case data table describes DIM_PCT as a
>> "marginal yield loss factor", but the formula in 3.1 applies it to labor hours.
>> Those are two different models. State plainly which one this workbook builds.

### 3.3 Revenue

>> TODO: state how season revenue is calculated from bed counts. Say explicitly
>> whether revenue scales linearly with beds or is reduced by anything.

### 3.4 Fertilizer cost

>> TODO: state how fertilizer cost is calculated. Say explicitly whether it is
>> linear in beds.

### 3.5 Labor costing — consumption order

>> TODO: state the order in which labor hours are consumed. Which hours are used
>> first, and which cover the remainder.

### 3.6 Labor costing — how the farmer is charged

>> TODO: the farmer is paid FARMER_SALARY but has only FARMER_FIELD_HRS field
>> hours at FARMER_RATE. State what her labor costs this model, and why.

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

>> TODO: add any further constraint you decide the model needs
>> (e.g. bed counts must be non-negative).

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

>> TODO: name every result the workbook has to produce. If it is not named here,
>> it is not required, and you have no grounds to call it missing at audit.
>> Consider: the optimal bed counts, season profit, total labor hours, temporary
>> workers used, the blended labor rate, the marginal cost schedule for each crop,
>> the standalone P = MC point for each crop, and the status of every rule in
>> Section 4.

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

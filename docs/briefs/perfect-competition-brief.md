# Engagement Brief — Perfect Competition

> **STATUS: DRAFT SCAFFOLD — NOT SUBMITTABLE.**
> Every section marked `TODO` must be filled in from the case page and the Stage 1
> handout before this brief is submitted. Nothing below is sourced from the case yet.

**Capability:** `capabilities/marginal-analysis/`
**Stage:** 1 — written before any Solver work
**Date drafted:** 2026-08-24
**Author:** Sean Barnes

---

## 1. Scenario

TODO — Summarize the case in a short paragraph: who the producer is, what market
they sell into, and why perfect competition is the right frame (price taker,
homogeneous product, free entry/exit, many buyers and sellers).

## 2. Assumptions

TODO — Pull these directly from the case page. Do not estimate.

| Assumption | Value | Source |
|---|---|---|
| Crops available | TODO | case page |
| Market price per unit | TODO | case page |
| Variable cost per unit / acre | TODO | case page |
| Fixed costs | TODO | case page |
| Yield per acre | TODO | case page |

## 3. Constraints (caps)

TODO — List every binding cap the case imposes, with its numeric limit.

| Constraint | Limit | Source |
|---|---|---|
| Total acreage | TODO | case page |
| Labor hours | TODO | case page |
| Water allocation | TODO | case page |
| Operating budget | TODO | case page |
| Per-crop min/max | TODO | case page |

## 4. Hypothesis

TODO — **This is the graded element.** State, before running Solver, which specific
crop mix you expect to maximize profit, and the economic mechanism that drives it.

A complete hypothesis does three things:

1. **Names the mix specifically** — the crops and the approximate allocation
   (e.g. acres or share of total), not "a mix of high-value crops."
2. **Gives the mechanism** — why that mix wins in economic terms. Under perfect
   competition the producer is a price taker, so the lever is cost and constraint
   structure, not pricing power: the profit-maximizing mix pushes output toward the
   crop with the highest contribution margin *per unit of the binding constraint*,
   until that constraint is exhausted or marginal cost rises to meet market price
   (MC = MR = P).
3. **Identifies which constraint binds** — and therefore what the shadow price is
   measuring when Solver reports it.

> **Hypothesis:** TODO

## 5. Method

TODO — Confirm or adjust against the Stage 2 spec.

1. Build the model workbook in `capabilities/marginal-analysis/`, following the
   color convention recorded in that folder's `README.md` (blue = hardcoded input,
   black = formula, green = cross-sheet link).
2. Set up the objective (total profit), decision variables (acres per crop), and
   the constraints from §3.
3. Run Solver; record the optimal mix, the binding constraints, and shadow prices.
4. Compare the result against the hypothesis in §4 — including where it was wrong.

## 6. What would falsify the hypothesis

TODO — State in advance what result would count as the hypothesis failing. For
example: a different constraint binds than predicted, or the optimum is a corner
solution concentrating on one crop when a mix was predicted.

## 7. Deliverables

- This brief — `docs/briefs/perfect-competition-brief.md` (Stage 1)
- Spec — `capabilities/marginal-analysis/spec.md` (Stage 2)
- Model workbook — `capabilities/marginal-analysis/` (Stage 2)
- Findings and charts — `analysis/` and `analysis/figures/`
- Recommendation — `docs/decisions/`

---

-Drafted with help from Claude (Anthropic, 2026); reviewed and edited by me.

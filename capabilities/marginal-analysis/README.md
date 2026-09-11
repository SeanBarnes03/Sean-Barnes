# Marginal Analysis

Using marginal cost and marginal revenue to find the profit-maximizing crop mix under perfect competition.

**Exercised in:** the perfect-competition engagement — a 64-bed market garden choosing how many beds of tomatoes, carrots and mesclun to plant at prices it cannot set. Brief: `docs/briefs/perfect-competition-brief.md`. Specification: `spec.md`. Model: `model.xlsx`. Analysis: `../../analysis/perfect-competition-analysis.md`, with figures in `../../analysis/figures/`. Decision: `../../docs/decisions/perfect-competition-memo.md`.

The engagement closed on 10 tomato, 20 carrot and 30 mesclun beds at a season profit of $42,762. The capability produced two findings the bed counts alone do not show: both cheap crops stop at their bed caps rather than where marginal cost meets price, which makes another carrot bed worth $352.49 and another mesclun bed $246.47; and tomato marginal cost falls at bed 6, because the farmer's own field hours run out there and cheaper temporary labor takes over.

## Workbook color convention

Any Excel model added to this folder (e.g. `model.xlsx`) follows the standard financial-modeling font-color convention:

- **Blue** — hardcoded inputs (assumptions, given data)
- **Black** — formulas (calculated within the same sheet)
- **Green** — links to another sheet or workbook

`model.xlsx` follows this convention. It is built from `spec.md`, and its Checks sheet computes every validation rule in Section 4 of that spec as PASS or FAIL.

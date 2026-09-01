<!-- PR TARGET: https://github.com/SeanBarnes03/Sean-Barnes | Stage 1.2 (8 pts) -->
# Stage 1.2 review — spec, build, audit

**Provisional score 74 out of 100 — held, not entered. The stage is not due until 6 September and this is a build in progress, not a finished one.**

**Spec:** [`capabilities/marginal-analysis/spec.md`](https://github.com/SeanBarnes03/Sean-Barnes/blob/main/capabilities/marginal-analysis/spec.md)

> Graded 2026-08-31, first pass. Your specification is one of the two strongest in the cohort. The workbook is built from it and is structurally correct. Solver has never been run, so the workbook does not yet report an answer and the audit section is empty — which is why this is held rather than entered. One Excel session moves this a long way.

| Criterion | Earned | Notes |
|---|---|---|
| Spec completeness — inputs, structure, calculation flow | 37 / 37.5 | Genuinely excellent, and it does the thing that separates a specification from a description: it writes down the conventions a builder would otherwise invent. Section 3.5 through 3.9 fixes the costing order, how the farmer is charged, how temporary labor is charged, the headcount rule, and the blended rate — and then adds the rule most people miss, that the permanent-versus-temporary split is a farm-level fact and is never pushed down into a crop's cost. Section 3.2 is the sharpest half-page in the document: the diminishing-returns rate multiplies labor hours, it does not reduce yield, and some versions of the case table label it a "marginal yield loss factor" which is not what this model implements. That is you catching an ambiguity in the source and closing it in writing. One person in this cohort has that misreading live in their brief right now. |
| Spec validation rules | 23 / 25 | Complete, written before the build, and every acceptance figure carries a tolerance with a reason — the $5 profit band exists to absorb rounding in the two derived wage rates, and you say so. The first-crossing definition in 3.10 is the most careful statement of it anyone wrote: you define the crossing as the largest q such that MC is at or below price for every bed up to q, and then explain why the looser phrasing would report the wrong point when the curve is non-monotonic. Two points off for one gap. Your only hand-calculated anchor is q = 1 tomato at 99 hours, and that is precisely the check a defective model passes: a builder that writes a flat (1 + dim) instead of compounding by q returns exactly 99.0 at q = 1 and 990 instead of 2,334.37 at q = 10. Add the second anchor. The stage's cross-check against the Farm Profit Lab is also not in your validation rules, and it is on the checklist. |
| Workbook satisfies the contract | 14 / 25 | The build is real and it follows the spec. Five sheets named as Section 2 specifies, 47 defined names, zero error cells, formulas referencing names rather than addresses, the Solver settings written into the Optimization sheet so the run is reproducible, and a Checks sheet laid out one row per validation rule. Structurally this is sound work. What it does not do is answer the question: the changing cells B5:B7 on Optimization are still 0 / 0 / 0, so every Actual and Status cell on the Checks sheet is blank and the two-starting-point table beneath them has no rows filled. The workbook was generated from the spec and committed without ever being opened in Excel and solved. |
| Audit note | 0 / 12.5 | Section 6 of the spec is an empty heading. That is the correct state for a workbook that has not been run, and nothing is lost — the audit is written after the build, and the build finished three hours before I looked at it. |
| **Final** | **74 / 100** | held |

### What to do, in order

- Open model.xlsx in Excel desktop. Solver is not in the web version.

- Set B5:B7 on Optimization to 0 / 0 / 0, enter the Solver settings you already wrote into rows 22 through 30, and run. Record the mix and the profit in the Solver path-dependence table on the Checks sheet.

- Reset to 20 / 0 / 0 and run again. Record it. If the two disagree, that is a finding worth writing up, not an error to hide.

- Read what the Checks sheet now says. Your acceptance criteria are 10 / 20 / 30 exactly and $42,762 within $5. Whether they pass is the whole point of having written them down first.

- Add the q = 10 tomato anchor to Section 4 and to the Checks sheet: 10 x 2.50 x 36 x 1.10^10 = 2,334.368214 hours. Confirm the workbook returns it.

- Cross-check one intermediate marginal cost against the Farm Profit Lab.

- Then write Section 6. Four or five checks, each saying what you checked, what you found, what you did about it, and — this is the part most people skip — what that check would have caught if it had failed. A check that could not have failed is not evidence.

### One thing worth saying about the derived rates

You wrote that typing the rounded $34.72 and $17.36 instead of deriving them shifts season profit by about $13, and made deriving them a rule. That is not a hypothetical.

Another workbook in this cohort types the rounded figures, and its profit comes out $13.16 above the check figure — enough to fail a tolerance, small enough to look like a modeling error rather than a rounding one, and genuinely difficult to find once the model is built. You reasoned your way to that in advance and wrote a rule against it, which is what a specification is for.

Storing carrot labor as 5/6 rather than 0.833 is the same instinct and it is worth the same amount. The case displays 0.833; the number is five sixths.

### A small inconsistency

capabilities/marginal-analysis/README.md still ends with "No workbook has been added yet; this documents the convention ahead of it." model.xlsx is sitting next to it. One line to fix, and it is worth fixing because that README is the file a reader opens first to find out what is in the folder.

Your spec frontmatter also still says status: draft. Once Solver has run and Section 6 is written, that becomes committed.

### Why this is held rather than entered

37.5 of the 100 points on this stage sit in the workbook and the audit, and both are mid-flight. Entering 74 today would record a snapshot of a Saturday morning rather than a piece of work, and the stage is not due for six days.

I am telling you the number so you know where you stand, not as a grade. Run Solver and write the audit and this lands in a very different place.

---

### How to work this review

Treat this PR the way an analyst treats feedback from a senior reviewer — a review is a proposal to engage with, not a checklist to rubber-stamp.

1. **Read it yourself first.** Form your own view before you change anything. Disagreeing *with a documented reason* is a legitimate, senior response.
2. **Stress-test it with an LLM.** Paste this review and your spec into your assistant and ask it to (a) explain anything you are unsure of, and (b) argue the *other side* — where might the reviewer be wrong, and what would you give up by making each change.
3. **Then correct the spec, not the workbook.** This is the rule that makes the stage work: when a check fails, you fix the specification and regenerate, so the document keeps describing what was actually built.
4. **Close the loop.** Reply in this thread with what you changed and what you pushed back on, then commit and push.

*Nothing here is final. Stage 1.2 is not due until 6 September, and the stage is re-graded from scratch at the deadline.*

— Adam

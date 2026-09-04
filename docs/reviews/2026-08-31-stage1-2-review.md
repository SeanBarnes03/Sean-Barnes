<!-- PR TARGET: https://github.com/SeanBarnes03/Sean-Barnes | Stage 1.2 -->
# Stage 1.2 review — spec, build, audit

**Spec:** [`capabilities/marginal-analysis/spec.md`](https://github.com/SeanBarnes03/Sean-Barnes/blob/main/capabilities/marginal-analysis/spec.md)

> Re-graded 2026-09-04 against your commits of 3 September. You have been reviewed on this before. You closed the round-trip gap, and you closed it the way the stage is supposed to work — by writing the rule into the specification and adding a validation check for it, not by quietly fixing the file.

| Criterion | Where it stands |
|---|---|
| Spec completeness — inputs, structure, calculation flow | Everything this criterion asks for, and the new Round-trip rule in Section 2 is the reason it stayed there. "Any tool that writes this workbook programmatically — openpyxl or equivalent — stores formulas without evaluating them, and strips whatever calculated values the file already carried. A workbook in that state has live formulas and blank results: it computes correctly the moment Excel opens it, and says nothing at all to anyone who reads it without recalculating." That is a build constraint most people would have treated as a one-off mistake, written down as a standing rule with its reason attached. |
| Spec validation rules | Everything this criterion asks for. You did not stop at the rule — you added the check that enforces it: "The committed workbook carries its calculated values, not just its formulas. Open the committed file and the Checks sheet must report Actual and Status without recalculating; blank result columns mean the file was written programmatically and never round-tripped through Excel." A rule that cannot be tested is advice. This one can fail. |
| Workbook satisfies the contract | The committed file now carries its values. All twelve checks read PASS with computed results rather than blanks: mix 10 / 20 / 30, profit $42,761.6647 against the $42,762 target inside the $5 band, standalone crossings 10 / 10 / 6, both hand anchors at 99 and 2,334.3682 hours, the blended-rate allocation reconciling to $104,118.3353, and the Farm Profit Lab cross-check at $5,585.71 against $5,586. Both Solver runs are recorded with their profit. Forty-six named ranges, no error cells, and the only numeric literals in the file are the case inputs, the q index columns, the three decision cells and the acceptance targets — which is exactly where literals belong. |
| Audit note | Unchanged and still everything this criterion asks for. Five checks, each with what was checked and what it was intended to catch, and every figure in it reproduces independently against my own model. |

### Why this is the full mark and not merely a fixed file

The gap last pass was that the committed workbook had been written by openpyxl and never opened in Excel, so it carried live formulas and blank results. The minimum fix was to open it, let it calculate, and commit again. That would have earned the marks back.

You did that and then went one level up: you asked why it happened, wrote the answer into Section 2 as a rule that binds every future build, and added an acceptance check so the next violation fails visibly instead of sitting there looking fine. The specification now prevents the defect rather than the workbook merely no longer having it.

That is the difference between fixing a bug and fixing the process that produced it, and it is the distinction this stage exists to teach.

### What this submission is, relative to the cohort

There are five finished workbooks in this cohort now. Yours and Michelle Buff's are the two whose specifications a stranger could build from without asking a single question, and yours is the one with the most conventions written down — Section 3.2 on what the diminishing-returns rate actually multiplies, 3.5 through 3.9 on the costing order, the smooth-constraint equivalence proof for the temporary-worker cap, and now the round-trip rule.

Every one of those is a decision a builder would otherwise have had to invent, recorded with the reasoning. That is why your workbook came out right the first time it was solved.

### Stage 1.3

You already have the two hardest things it asks for. The marginal-cost dip at tomato bed 6 is a real finding with a real explanation behind it — the curve falls at the moment the marginal labor source changes from the farmer's hours to the temporary workers' — and your brief committed a prediction the model can be compared against.

One standing rule: do not revise the brief to match the model. If they disagree, that is the finding. Your brief on main is still the version that commit 7dba227 overwrote back in August, and restoring your revised text is worth doing before you write the reflection, so the comparison is against what you actually believed.

---

### How to work this review

Treat this PR the way an analyst treats feedback from a senior reviewer — a review is a proposal to engage with, not a checklist to rubber-stamp.

1. **Read it yourself first.** Form your own view before you change anything. Disagreeing *with a documented reason* is a legitimate, senior response.
2. **Stress-test it with an LLM.** Paste this review and your spec into your assistant and ask it to (a) explain anything you are unsure of, and (b) argue the *other side*.
3. **Then correct the spec, not the workbook.** When a check fails, you fix the specification and regenerate, so the document keeps describing what was actually built.
4. **Close the loop.** Reply in this thread with what you changed and what you pushed back on, then commit and push.

*Your score and the per-criterion breakdown are in your Lamaku comment, not here — this repository is public.*

— Adam

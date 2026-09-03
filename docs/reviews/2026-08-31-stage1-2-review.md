<!-- PR TARGET: https://github.com/SeanBarnes03/Sean-Barnes | Stage 1.2 (8 pts) -->
# Stage 1.2 review — spec, build, audit

**You scored 98 out of 100 (A+) — 14.70 of the 15 points for this stage. Entered; the hold is lifted.**

**Spec:** [`capabilities/marginal-analysis/spec.md`](https://github.com/SeanBarnes03/Sean-Barnes/blob/main/capabilities/marginal-analysis/spec.md)

> Re-graded 2026-09-02 against your 1 September commits. Your previous result was 74, held, because Solver had never been run and the audit section was an empty heading. Both are done, both gaps I named in the validation rules are closed, and every figure in your audit reconciles against my own model. This is finished work.

| Criterion | Earned | Notes |
|---|---|---|
| Spec completeness — inputs, structure, calculation flow | 37.5 / 37.5 | Up from 37, and full marks. Two additions did it, and both are the same kind of thing: a convention written down with the reason attached. The sheet-name rule — no spaces, because Solver on macOS mishandles unquoted sheet references containing them and raises a 1004 — is a build constraint a future builder would otherwise rediscover the hard way. And the smooth-constraint note on TEMPS_REQUIRED is better than that: you kept ROUNDUP out of the Solver constraint and used TEMP_HRS_USED <= 5,760 instead, then proved the two are equivalent (ROUNDUP(h/1440) <= 4 holds exactly when h <= 5760) and said why the step function would stall GRG Nonlinear. That is a modeling decision, its justification, and its proof of equivalence in five lines. |
| Spec validation rules | 25 / 25 | Up from 23, and both gaps are closed exactly as named. The second labor anchor is in at q = 10 with the reasoning written into the spec rather than left implicit: a builder who writes a flat (1 + DIM_PCT) instead of compounding by q returns exactly 99 hours at q = 1 and 990 at q = 10 against the required 2,334.368214, so the second anchor is the one that catches it. The Farm Profit Lab cross-check is in too, and you handled the part most people would have got wrong — the lab carries FIXED_COSTS inside its totals and your spec excludes them, so its totals run $20,000 higher at every bed count. You compare marginal figures, where the constant offset cancels, and you say why. |
| Workbook satisfies the contract | 23 / 25 | Up from 14. B5:B7 now hold 10 / 20 / 30, both Solver runs are recorded, 46 named ranges, every calculated cell is a formula referencing names rather than addresses, and the only numeric literals anywhere are the case inputs, the q index columns, the three decision cells, and the acceptance targets — which is exactly where literals belong. Two points off for one thing: the committed file was written by openpyxl and has never been saved out of Excel, so it carries no calculated values. Open it and everything computes; but until someone does, the Actual and Status columns on Checks are blank, and the two Solver runs live as typed records rather than as the workbook's own state. The file that was solved and the file that is committed are not the same file. |
| Audit note | 12.5 / 12.5 | Up from 0, and full marks. Five checks, each with what you checked and what it was intended to catch. I reproduced every number in it independently and they all hold — see below. |
| **Final** | **98 / 100** | entered |

### I checked your audit figures against my own model and they all hold

This matters more than the score, so I want to be specific about it.

The tomato marginal cost of $7,661 at bed 5 and $4,906 at bed 6 — I get $7,660.86 and $4,906.27. The Farm Profit Lab comparison of $59,974 against $54,388 for a difference of $5,586 — I get variable costs of $39,973.40 and $34,388.38, which are your numbers less the $20,000 the lab carries and yours does not, and a marginal cost of $5,585.02. Season profit $42,761.66, crossings 10 / 10 / 6, q = 1 at 99 hours: all correct.

So your audit is not a narrative about having checked things. It is a set of independently verifiable claims, and they verify.

### The marginal cost dip at bed 6, and why you should not explain it yet

You recorded it and did not explain it, which is right — that belongs in Stage 1.3. But hold onto what you found, because it is the most interesting thing in this case and most of the cohort's workbooks paper over it.

Tomato marginal cost rises to $7,661 at bed 5, falls to $4,906 at bed 6, then rises again. A cost curve that falls in the middle looks like a defect. It is not. The farmer's 720 hours are the cheap hours in the sense that matters here — they are already bought — and by bed 5 they are nearly gone. The fifth bed is expensive because part of it is priced at her $34.72; the sixth is cheaper because all of it is priced at the temp's $17.36. The curve dips at the moment the marginal labor source changes.

That is worth writing about in Stage 1.3 because it is a real economics point, not a spreadsheet artifact, and because it is the reason "the first q where MC exceeds price" is the wrong definition of the crossing — a definition you had already written the correct version of in section 3.10 before the workbook existed to show you why it mattered.

### The two points, and how to close them in five minutes

Open model.xlsx in Excel, let it calculate, and commit it again. That is the whole fix. The file then carries its own values, and someone who opens it on GitHub or in a viewer that does not recalculate sees a workbook that reports its answer rather than one that reports blanks.

It is worth doing for a reason beyond the two points: a workbook that has to be recalculated to say anything is a workbook whose committed state cannot be reviewed. Your spec is unusually careful about the artifact being the thing of record; this is the same principle applied one level down.

### Where this submission sits

There are now three finished workbooks in the cohort and yours is one of them. What distinguishes it is the specification: it is the document that most reads like something a second person could build from without asking you a single question, and the sections that write down conventions rather than formulas — 3.2 on what the diminishing-returns rate multiplies, 3.5 through 3.9 on the costing order — are the reason your workbook came out right the first time it was solved.

For Stage 1.3: you already have the two hardest things it asks for. The dip at bed 6 is a finding with a real explanation behind it, and your brief committed a prediction that the model can be compared against. Do not revise the brief to match the model.

---

### How to work this review

Treat this PR the way an analyst treats feedback from a senior reviewer — a review is a proposal to engage with, not a checklist to rubber-stamp.

1. **Read it yourself first.** Form your own view before you change anything. Disagreeing *with a documented reason* is a legitimate, senior response.
2. **Stress-test it with an LLM.** Paste this review and your spec into your assistant and ask it to (a) explain anything you are unsure of, and (b) argue the *other side* — where might the reviewer be wrong, and what would you give up by making each change.
3. **Then correct the spec, not the workbook.** This is the rule that makes the stage work: when a check fails, you fix the specification and regenerate, so the document keeps describing what was actually built.
4. **Close the loop.** Reply in this thread with what you changed and what you pushed back on, then commit and push.

*Nothing here is final. Stage 1.2 is not due until 6 September, and the stage is re-graded from scratch at the deadline.*

— Adam

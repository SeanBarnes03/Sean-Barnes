<!-- PR TARGET: https://github.com/SeanBarnes03/Sean-Barnes | Stage 1.1 -->
# Stage 1.1 review — engagement brief

**Brief:** [`docs/briefs/perfect-competition-brief.md`](https://github.com/SeanBarnes03/Sean-Barnes/blob/main/docs/briefs/perfect-competition-brief.md)

> Re-checked 2026-08-31. Your score is unchanged. The file on main is still the reverted version — the recovery I described four days ago has not happened, and your Stage 1.2 spec and workbook are now built on top of a brief that does not say what you think it says. Read the first section before anything else.

| Criterion | Where it stands |
|---|---|
| Problem restated in your own voice | Graded at commit 0160cef, not at main. You separate what is being decided, by whom, what happens if it goes badly, what is fixed, what is chosen, and what limits the choice — the full frame, and one of four in the cohort that has all six parts. The caps, the season, the fixed costs, the farmer's 720 hours at $34.72 and the four temporary workers at $17.36 are all correct. |
| Hypothesis names a specific mix | 5 tomato, 10 carrot, 20 mesclun — 35 of the 64 beds, with the shortfall stated rather than hidden. Committed and specific, and the frontmatter agrees with the body. |
| Economic mechanism | You name the comparison the case turns on and you take a side on it: tomato labor compounds at 10 percent per bed against 2.5 and 1.25, and you expect that to overcome a three-to-four-times revenue advantage "within a few beds." That is a falsifiable claim about where the crossing sits. What is still open: "within a few beds" is where a number belongs — you predict the fifth or sixth tomato bed stops paying, and the case gives you everything needed to check it in one line. |
| Falsifiability and process | "If we had beds left over, I was too conservative in my estimate. I left too much on the table to achieve P=MC." That is a real condition — it names an observable and the direction of the error, and given a 35-bed prediction it is very likely to fire, which is a sign you wrote it honestly rather than defensively. Four points off, and they are for the AI boundary rather than the writing — see below. |

### Your brief on main is still the overwritten version

Commit 7dba227, on 27 August at 05:07, removed 73 lines and added 9. It replaced your revised brief with an earlier draft. The crop table, the three assumptions, the hypothesis reasoning, and the two-part falsification section are all gone from main and have not come back.

I graded 0160cef — "Revise the Stage 1 hypothesis against the critique," 26 August at 22:16 — which is your real work and was committed and pushed well before any deadline. That version scores 91. What is on main right now would score in the sixties.

This now matters more than it did four days ago, because you have built on top of it. Your specification and workbook went in this morning, and your capability README points at docs/briefs/perfect-competition-brief.md as the brief the model answers. In Stage 3 you compare what you predicted against what the model found — and the file that comparison reads from is the one on main.

To recover it: open https://github.com/SeanBarnes03/Sean-Barnes/blob/0160cef/docs/briefs/perfect-competition-brief.md, copy the contents, paste them over the current file, and commit with a message saying what happened — "Restore the revised Stage 1 brief overwritten by 7dba227" is exactly right. The history keeps both versions, which is the point of having it.

The likely cause is worth knowing: a browser tab left open on the GitHub editor from before the revision, saved afterwards. The tab had no idea the file had changed underneath it. It is a common way to lose work and it costs nothing once you know the shape of it.

### The gap, and why they are four and not more

Your prompt log states plainly that Claude drafted the revised wording at your direction. I want to be precise about the line, because it is not obvious.

The stage allows an assistant to explain the economics, to attack your reasoning, and to tell you where an argument does not hold. It does not allow it to write the brief. The reason is Stage 3: you will be asked to explain why your prediction and your model disagreed, and a prediction you did not personally reason your way to has nothing to explain.

It cost marks rather than more because you disclosed it, and I want that to be the lesson rather than the caution. A log that records what the tool did is what makes the boundary enforceable at all, and honest logging will never be punished harder than silence would have been. Your prompt log is the best in this cohort and that has not changed.

For Stage 3 the practical version is: let the assistant argue with your draft as hard as you like, then close it and write the paragraph yourself.

### On your Stage 1.2 work

Your specification is excellent and is graded separately — it is one of the two strongest in the cohort. There is one thing in it that connects back to this brief: your acceptance criteria include the published check figures, which means your workbook is built to reproduce an answer you already know.

That is correct for Stage 2 and it is what the stage asks for. Just keep it separate in your head from Stage 3, where the interesting question is why your brief predicted 5 tomato beds and the model returned something else. Do not edit the brief toward the model. The gap is the finding.

---

### How to work this review

Treat this PR the way an analyst treats feedback from a senior reviewer — a review is a proposal to engage with, not a checklist to rubber-stamp.

1. **Read it yourself first.** Form your own view before you change anything. Disagreeing *with a documented reason* is a legitimate, senior response.
2. **Stress-test it with an LLM.** Paste this review and your brief into your assistant and ask it to (a) explain anything you are unsure of, and (b) argue the *other side* — where might the reviewer be wrong, and what would you give up by making each change.
3. **Then write the changes yourself.** For a brief this matters more than usual: a hypothesis you did not generate cannot be honestly compared against your model in Stage 3, and that comparison is the entire point of writing the brief first.
4. **Close the loop.** Reply in this thread with what you changed and what you pushed back on, then commit and push.

*One standing rule: do not revise your hypothesis to match what your model later tells you. If the model contradicts the brief, that is a finding, not an error.*

*Your score and the per-criterion breakdown are in your Lamaku comment, not here — this repository is public.*

— Adam

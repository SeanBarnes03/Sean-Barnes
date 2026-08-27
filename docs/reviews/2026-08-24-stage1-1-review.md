<!-- PR TARGET: https://github.com/SeanBarnes03/Sean-Barnes | Stage 1.1 (2.5 pts) -->
# Stage 1.1 review — engagement brief · **91 / 100** (A-) · 2.28 / 2.5 pts

**Brief:** [`docs/briefs/perfect-competition-brief.md`](https://github.com/SeanBarnes03/Sean-Barnes/blob/main/docs/briefs/perfect-competition-brief.md)

> Graded 2026-08-27 against commit 0160cef, not against what is on main right now. Read the first section below before anything else — your best version of this brief is not the one currently published, and that is worth fixing today.

| Criterion | Earned | Notes |
|---|---|---|
| Problem restated in your own voice | 28 / 30 | Strong, and strongest exactly where this case is hardest. Your price-taker paragraph is the best in the cohort: "far too small to move the price of a tomato at the farmers' market... She cannot raise it by growing less or lower it by growing more, which is why the decision is about quantity and cost, not about pricing." That is the definition of perfect competition arrived at from the farm's position rather than recited from a textbook. You also do something nobody else did — you say what is not a decision: "the number of temporary workers is not a separate decision, it follows from the labor hours those beds require." Getting the decision variables right is half of setting up an optimization, and most briefs quietly treat workers as a fourth lever. "The whole season is committed in one decision and cannot be undone in July" is not in the case materials anywhere; it is yours, and it is the reason this decision is worth a model at all. The two points off are presentation: the "What is fixed" line is a single run-on strung together with hyphens, and it is the one part of the brief a reader has to work at. |
| Hypothesis names a specific mix | 24 / 25 | Five tomato, 10 carrot, 20 mesclun — 35 of the 64 beds. Three committed integers with the total stated, which is more than most. One point off for "about," which does no work here: the numbers are precise enough to be checked, so let them be. |
| Economic mechanism | 23 / 25 | You build the argument from the case's own figures rather than around them. The revenue ratios (three times mesclun, four times carrots), the starting hours (2.50 against 1.25 and 0.833), and the escalation rates (10 percent against 1.25 and 2.5) are all in the reasoning, not just in a table. Then the sentence that earns most of this: you prefer mesclun to carrots even though carrots need fewer hours, because mesclun earns $2,700 against $2,094 and escalates at half the rate. That is a genuine trade-off worked out rather than a preference asserted, and it is the kind of reasoning the rest of this stage is short on. You also account for the 29 unplanted beds — "not worth planting, not merely unplanted" — which is a real economic claim. Two points off because you never multiply anything out. You predict the fifth or sixth tomato bed costs more than it earns; the case gives you everything needed to check that in one line, and doing it would either confirm your number or move it. |
| Falsifiability and process | 16 / 20 | Two named outcomes and both test the mechanism rather than the number, which is the harder and better version. "If any crop stops at its bed cap rather than where its marginal cost meets its price, then a fence set that crop's level and not the economics" is a real disconfirming observation, and it is the one most likely to fire. The brief is at the correct path, committed before any modeling, with a message saying what changed. Your AI critique session is logged in full — see below. The four points off are for one thing, and it is worth being direct about: your log records that Claude drafted the revised wording at your direction. The stage allows an assistant to explain the economics and to attack your reasoning; it does not allow it to write the brief. You disclosed it plainly, which counts for a great deal and is why this costs four points rather than more. |
| **Final** | **91 / 100** | earned on merit |

### Read this first — your brief on main is the wrong version

Your last commit to this file, 7dba227 on 27 August at 05:07, removed 73 lines and added 9. It replaced the good version of your brief with an earlier draft: the crop table is gone, the three assumptions are gone, the hypothesis reasoning is reduced to the bed counts with nothing behind them, and the two-part falsification section is down to one line about having beds left over.

I do not think you meant to do that. It has the signature of a browser tab left open on an older version of the file and then saved — the GitHub web editor will happily write a stale copy over newer work without warning you.

Nothing is lost. Your good version is commit 0160cef, "Revise the Stage 1 hypothesis against the critique," from 26 August at 22:16, and I graded that one. To get it back: open the file on github.com, click History, click that commit, click the three dots at the top right, and choose View file. Copy what you see, then edit the file on main and paste it in. Commit with a message saying what happened — "Restore the revised brief overwritten by 7dba227" is exactly right, and a year from now you will be glad the history says so.

The general lesson is the one this course keeps making: history is permanent, which cuts both ways. It is why an accidental overwrite is recoverable, and it is why the thing to check after any web edit is what main actually holds.

### What makes this brief work

Two things, and the second is rarer than the first.

- You committed to a prediction that is probably wrong, and you made it easy to prove wrong. You expect all three crops to stop on economics before they reach their caps. That is a strong claim, it is checkable in one glance at the model output, and if it fails it fails loudly. A brief that cannot embarrass its author is not doing this stage's job.

- You kept your own numbers when the critique pushed on them. Your log says the model told you 5/10/20 does not follow from the mechanism you gave, and that your carrot-versus-mesclun ordering inverted your own low-labor logic. You did not change the numbers to make the objection go away. You went back and repaired the reasoning around them instead, and where you still disagreed you said why. That is the correct response and it is uncommon — the usual move is to adopt whatever the critique implies and lose track of what you actually thought.

### What I'd sharpen

- Do the arithmetic on the tomato claim. You predict the fifth or sixth bed stops paying. Labor hours for q beds are q x 2.50 x 36 x 1.10^q, fertilizer is $880 a bed, and the price is $8,800. Work out the cost of the fifth bed and the sixth. If they come in well under $8,800, your tomato number is low and you will want to know that now rather than in Stage 3.

- Check the same way on carrots and mesclun, because that is where I think your prediction is most exposed. Mesclun escalates at 1.25 percent a bed. Over 30 beds that is a factor of about 1.45 on labor — compounding, but gently. Ask yourself whether a crop escalating that slowly really stops paying at 20 beds, or whether it runs to its cap. Your falsification section already names this as the outcome that would refute you, so you have set the test correctly; it is worth checking the answer before the model does it for you.

- Next time, write the words yourself. Use the assistant exactly the way you did for the critique — attack this, do not rewrite it — and then type the revision in your own voice, even if it comes out rougher. Rougher is fine. Stage 3 asks you to compare what you predicted against what the model found, and that comparison only means something if the prediction was yours all the way down to the sentences.

### Where this leaves you for Stage 1.2

Stage 1.2 asks for capabilities/marginal-analysis/spec.md written before the workbook exists, then an audit of what gets built from it. Your capability folder is already there and already carries the color convention, which is a real head start.

The one thing to carry across: put the published check figures into the spec as acceptance criteria before you build anything, with a tolerance on each. Both of the completed workbooks in this cohort so far have costing errors that a check-figure table would have caught in a minute, and neither spec had one.

---

### How to work this review

Treat this PR the way an analyst treats feedback from a senior reviewer — a review is a proposal to engage with, not a checklist to rubber-stamp.

1. **Read it yourself first.** Form your own view before you change anything. Disagreeing *with a documented reason* is a legitimate, senior response.
2. **Stress-test it with an LLM.** Paste this review and your brief into your assistant and ask it to (a) explain anything you are unsure of, and (b) argue the *other side* — where might the reviewer be wrong, and what would you give up by making each change.
3. **Then write the changes yourself.** For a brief, this matters more than usual: a hypothesis you did not generate cannot be honestly compared against your model in Stage 3, and that comparison is the entire point of writing the brief first.
4. **Close the loop.** Reply in this thread with what you changed and what you pushed back on, then commit and push.

*One standing rule for this stage: do not revise your hypothesis to match what your model later tells you. If the model contradicts the brief, that is a finding, not an error — Stage 3 asks you to explain the gap, and a brief quietly edited to be right afterwards has nothing left to explain.*

— Adam

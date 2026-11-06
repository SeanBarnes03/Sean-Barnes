---
name: mental-models
description: Stress-test a brief, spec, analysis, decision memo, draft or plan by choosing the 3–5 mental models that best fit it and using them to find hidden assumptions, second-order effects and the conditions under which the argument fails. Use when I say "apply mental models", "red-team this", "stress-test my argument", "what am I missing", "falsify this" or "run the models on <file>". It critiques first, then rewrites the weak passages when I ask.
---

# Mental models review

Pressure-test my work the way a red team would: choose the few lenses that matter, use
them to attack the reasoning, and tell me where it breaks. The model library is
[`models.md`](models.md), in the same folder as this file.

## Ground rules

- **Critique first, then fix.** Finish the review before changing anything, so I can see
  the reasoning on its own. Then offer to rewrite the passages that failed. When I say yes,
  edit the file directly in my voice and list each change with the finding it answers.
- **Quote, don't paraphrase.** Every finding points at a specific line, cell or figure in
  the work, with `file:line` where there is one.
- **Use the work's own numbers.** If a model suggests a check (a margin, a base rate, an
  opportunity cost), run it against the figures in the repo instead of describing it.
  Say which figures you used.
- **Fewer, sharper lenses.** Three to five models. Each one must change what I would do.
  A model that only produces a generic warning is noise and gets dropped.
- **No flattery and no hedged verdicts.** If the argument holds, say so and say why it holds.

## Steps

1. **Read the target.** If I named a file, read it in full. If I named an engagement, read
   its brief in `docs/briefs/`, its spec in `capabilities/<name>/`, and its decision in
   `docs/decisions/` if one exists. If I gave no target, ask which piece of work I mean.
   State the central claim in one sentence: what the work argues and what it recommends.

2. **Select 3–5 models.** Read [`models.md`](models.md). Choose models from at least two
   different families. For each, give one line on why it fits *this* work: the feature of
   the argument it bears on. Also list one or two tempting models you rejected and why.
   That shows the selection was a choice rather than a default.

3. **Stress-test.** For each selected model:
   - The question the model asks, applied to this work.
   - What the work assumes, explicitly or silently, that the model exposes.
   - The evidence: a quotation from the work, or a calculation from its own figures.
   - Severity: **breaks the argument**, **weakens it**, or **holds up**.

4. **Falsify.** Use inversion. What would have to be true for the recommendation to be
   wrong? Name the single most likely failure condition, how I would observe it, and what
   it would cost. Then trace the main second-order consequence of the recommendation:
   what happens after the first effect, and who reacts to it.

5. **Verdict.** In a few lines:
   - The strongest counter-argument to my position, stated as its best advocate would put it.
   - What I should check, measure or reconsider before I commit, in priority order.
   - Whether the core claim survives.

6. **Fix (when I ask).** Rewrite the passages behind each **breaks** or **weakens** finding.
   Keep my structure and numbers unless a finding shows they are wrong, and flag any number
   you changed. Do not touch passages that held up.

## Output

Report the review in the chat under the headings for steps 1–5. Only if I ask for it to be saved,
write it to `docs/reviews/<date>-<slug>-mental-models.md`. Use the Hawaii date (HST, UTC-10),
as `AGENTS.md` requires. If the review or the fixes change my scope or conclusions, add a row
to `prompt-log.md` that says what changed and why.

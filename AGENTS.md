# AI conventions

## About this repository

Portfolio and coursework repository for Sean Barnes (University of Hawaiʻi DLEMBA).
One folder per capability, each closed out with a written decision. Agents iterate
create and review themselves to mirror working with a person.

Canonical file: `AGENTS.md`. `CLAUDE.md` points here, so any AI tool picks up the same
conventions regardless of which one is invoked.

## Disclosure

Any content drafted with AI assistance is marked at the end of the file, e.g.:

`-Drafted with help from ChatGPT; reviewed and edited by me.`

Nothing gets published from an AI draft without being reviewed and edited by me first.

## Where things are

- `README.md` — who I am, plus an index of engagements.
- `RESUME.md` — current resume.
- `prompt-log.md` — running record of AI sessions that materially shaped the work in this repo. Not a transcript of every prompt — just the ones that mattered.
- `.gitignore` — what must never enter the history.
- `.claude/skills/` — personal sandbox for Claude Code skills. Nothing in it is load-bearing for the rest of the repo.
- `capabilities/<name>/` — one folder per capability, each with `README.md`, `spec.md`, and any supporting model/workbook files.
- `docs/briefs/` — written BEFORE the work: scope and hypothesis.
- `docs/decisions/` — written AFTER the work: the recommendation.
- `data/` — sourced inputs, each with provenance noted (source, date pulled, access method).
- `analysis/figures/` — the findings, and the charts they refer to.

## Naming

- The directory matters most. A file in the wrong folder may not be found at all. If
  you are not certain which folder a file belongs in, ask me before you write it — do
  not choose for me.
- Graded files use the exact filename the stage brief gives — lowercase, hyphens, no
  spaces. Some courses date-stamp (`YYYY-MM-DD-lastname-slug.md`); the stage page says
  so when they do.
- Slugs name the engagement, never the week, the course, or the assignment number.
- Never invent a path or a filename. I will give you the exact one.

## How I work

- Explain concepts fully and walk the worked example. Do not hand me conclusions.
- Critique my reasoning directly. I would rather be corrected than agreed with.
- When you are uncertain, say so and say what would resolve it.

## What you may and may not draft

- You MAY explain, critique, debug, quiz me, and draft mechanical files.
- You MAY NOT write my briefs, analyses, memos, or reflections.
- A critique ends at diagnosis. Naming a hole is help; supplying the wording that fills
  it is not, and the boundary is crossed during the repair, not during the critique.
- Every statistic or figure you give me is a draft until I verify it against a source.

## Working with AI on a capability

1. Start with a brief in `docs/briefs/` before generating any analysis — scope and hypothesis first.
2. Log any AI session that changed scope, structure, or conclusions in `prompt-log.md`.
3. Close the capability with a decision doc in `docs/decisions/` summarizing the recommendation.
4. Note data provenance in `data/` before a source is used in any model.

## Documentation

When work changes, update the document that describes it in the same commit. A
capability's README names the engagements that exercised it — keep that current.

## Scope

Do the work I asked for. If you notice something worth doing that I did not ask for,
tell me instead of doing it.

## Commits

Descriptive messages: what changed and why. Never "update" or "stuff".

## Never include

No credentials, no API keys, no personal data about anyone, no licensed or copyrighted
material. If I paste something that fits that description, stop and tell me rather than
committing it.

## Mistakes to avoid (append to this list)

Record errors here as they happen, so the same one does not repeat.

- **Contradicting a constraint stated elsewhere in the same document.** Three of the
  five entries below are this one failure. Check the document against itself first.
- 2026-08-26 — Drafted the revision wording after a critique, when the critique was
  supposed to end at diagnosis.
- 2026-08-26 — Left a frontmatter hypothesis describing a tomato-heavy mix the body no
  longer predicted.
- 2026-08-26 — Wrote a falsification section naming a spending limit the case does not
  impose. Invented a constraint.
- 2026-08-24 — Predicted a crop mix infeasible against the bed caps stated in the same
  document.
- 2026-08-24 — Left template prompts sitting in the section bodies of a graded file and
  reported it complete.

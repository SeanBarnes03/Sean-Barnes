# AGENTS.md

Agents iterate create and review themselves to mirror working with a person. Canonical file for how AI tools are used in this repository. `CLAUDE.md` points here so any AI agent picks up the same conventions regardless of which tool is invoked.

## Dates and time zone

I work in Hawaii (HST, UTC-10). Any date written into this repository — frontmatter,
`prompt-log.md` rows, review filenames — is the Hawaii date, and refers to when the
content was written rather than when the file was created or last touched.

Agents run in UTC, which is 10 hours ahead and usually a day later in the evening.
Convert before stamping a date, and convert before reasoning about when something was
committed or pushed.

## Disclosure

Any content drafted with AI assistance is marked at the end of the file, e.g.:

`-Drafted with help from ChatGPT; reviewed and edited by me.`

Nothing gets published from an AI draft without being reviewed and edited by me first.

Files in `docs/reference/` are my own background material, not coursework, and do not carry the disclosure line.

## Repository layout

- `README.md` — who I am, plus an index of engagements.
- `RESUME.md` — current resume.
- `docs/reference/` — background material for agents. `resume-2026-08.md` (with the original `.docx`) is my full-length resume: every role from 2011 on, with scope and results. Read it when you need detail on my experience that the condensed `RESUME.md` leaves out.
- LinkedIn: [linkedin.com/in/seanwbarnes](https://www.linkedin.com/in/seanwbarnes/). Agents usually can't load it, because LinkedIn requires a login and blocks automated readers. Treat the resume files as the source of truth, and don't describe the profile's contents without a saved copy in `docs/reference/`.
- `prompt-log.md` — running record of AI sessions that materially shaped the work in this repo. Not a transcript of every prompt — just the ones that mattered.
- `.gitignore` — what must never enter the history.
- `.claude/skills/` — personal sandbox for Claude Code skills. Nothing in it is load-bearing for the rest of the repo.
- `capabilities/<name>/` — one folder per capability, each with `README.md`, `spec.md`, and any supporting model/workbook files.
- `docs/briefs/` — written BEFORE the work: scope and hypothesis.
- `docs/decisions/` — written AFTER the work: the recommendation.
- `data/` — sourced inputs, each with provenance noted (source, date pulled, access method).
- `analysis/figures/` — the findings, and the charts they refer to.

## Working with AI on a capability

1. Start with a brief in `docs/briefs/` before generating any analysis — scope and hypothesis first.
2. Log any AI session that changed scope, structure, or conclusions in `prompt-log.md`.
3. Close the capability with a decision doc in `docs/decisions/` summarizing the recommendation.
4. Note data provenance in `data/` before a source is used in any model.

# Skills

Claude Code skills for this repository. Each folder holds a `SKILL.md` that Claude Code
loads when the request matches its description, or when the skill is called by name
(for example `/mental-models`).

| Skill | What it does |
|---|---|
| [`mental-models`](mental-models/) | Stress-tests a brief, spec, analysis, memo or draft. It chooses 3–5 lenses from [a curated library](mental-models/models.md), finds hidden assumptions and second-order effects, and names the condition under which the argument fails. It critiques first, then rewrites the weak passages on request. |

Example requests:

- `/mental-models docs/briefs/research-brief.md`
- "Red-team my perfect-competition memo with mental models."
- "What am I missing in the Maui groundwater recommendation?"
- "Red-team my brief, then fix what breaks."

None of these skills is load-bearing: the rest of the repository does not depend on them.

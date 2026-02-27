# Project Crucible

## First Thing Every Session
1. Read `HANDOFF.md` — tells you what to do next, what's blocked, and what NOT to do
2. Read `AGENT.md` — project conventions, known gotchas, decisions log
3. Read the files listed in HANDOFF.md's "Reading Order" section before writing any code

## PR Conventions
- **Separate bug fixes / tooling changes from experiment runs.** If you fix a bug or add a feature while running an experiment, make separate PRs — one for the code change, one for the run results. Don't bundle them together.

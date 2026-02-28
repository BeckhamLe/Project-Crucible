# Project Crucible

## First Thing Every Session
1. Read `HANDOFF.md` — tells you what to do next, what's blocked, and what NOT to do
2. Read `AGENT.md` — project conventions, known gotchas, decisions log, literature review findings
3. Read the files listed in HANDOFF.md's "Reading Order" section before writing any code

## Critical: Simulation Output is Append-Mode
`rounds.jsonl` is opened with `"a"` (append). If you run a simulation into a directory that already has results, it APPENDS to the existing file and corrupts the data. **NEVER re-run a simulation into an existing results directory.** Always delete the output directory first, or use a unique run-id. This has already caused data corruption — do not repeat it.

## Smoke Test Rules
- **NEVER use a real poc config** (e.g., poc_005.json) for smoke tests — they have `rounds: 30` and you'll burn a full run by accident
- Create a throwaway config with `rounds: 5` or use a unique smoke test run-id
- **Delete the smoke test config AND results directory** when done — don't leave artifacts
- Use a unique run-id for each smoke test attempt (e.g., `smoke_test_1`, `smoke_test_2`) — never reuse a run-id

## Known Gotchas
- `analysis/` module is NOT dead code — it's a post-processing pipeline that runs AFTER simulation. Don't "fix" it by deleting or refactoring it.
- `Action` dataclass in `sim/models.py` is imported but unused — the system uses plain dicts for actions. It's harmless schema documentation. Don't treat it as a bug.
- `.harness/` dashboard is future infrastructure for live experiment monitoring. It's gitignored. Don't delete it.
- Don't use model ID `claude-3-5-haiku-20241022` — it 404s. Use `claude-haiku-4-5-20251001`.
- Prompt language must be neutral across all action types — no hype words ("UNIQUE POWER", "IMMEDIATELY"), no capitalized emphasis ("ALL", "YOU"), no loaded framing. All actions described with the same clinical tone. Biased prompts contaminate experiment results.

## PR Conventions
- **Separate bug fixes / tooling changes from experiment runs.** If you fix a bug or add a feature while running an experiment, make separate PRs — one for the code change, one for the run results. Don't bundle them together.

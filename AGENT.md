# AGENT.md — Project Knowledge Base

> Read this at session start and before each task. Update when you
> discover something that would save a future agent time.

## Project Conventions
- One model (Claude 3.5 Haiku) for all agent personas — personas come from system prompts, not different models
- Credits are fake currency (not API tokens) — fixed pool, zero-sum
- Results are immutable after analysis — iterate by creating new runs, not editing old ones
- findings/log.md is append-only

## Known Gotchas
- `analysis/` module is NOT dead code — it's a post-processing pipeline (runs AFTER simulation). It reads from `results/{run_id}/` and produces `metrics.json` + plots. It's intentionally not called by `run.py` yet. Don't "fix" this by deleting or refactoring it.
- `Action` dataclass in `sim/models.py` is imported but unused — the system uses plain dicts for actions. It's harmless documentation of the action schema. Don't treat it as a bug.
- `.harness/` dashboard is future infrastructure for live experiment monitoring. It's gitignored and not connected to the sim. Don't delete it.

## Decisions Log
| Date | Decision | Context | Decided By |
|------|----------|---------|------------|
| 2026-02-24 | Name: Project Crucible | "Agora" had naming collision with existing AI lab | Beckham |
| 2026-02-24 | Claude 3.5 Haiku for PoC | Cheapest option (~$1-2 for full PoC), swap later if needed | Beckham |
| 2026-02-24 | Same model, different prompts | Isolates persona as the only variable — scientifically cleaner | Beckham |
| 2026-02-24 | Fake credits, not API tokens | Scarcity is simulated, not real. 10 credits per agent, zero-sum pool | Beckham |

## What Has Failed (Anti-Patterns)
- Killing a running simulation and restarting into the same `results/{run_id}/` directory corrupts `rounds.jsonl` because the engine writes in append mode (`"a"`). Always delete the output directory before re-running with the same run_id.

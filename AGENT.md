# AGENT.md — Project Knowledge Base

> Read this at session start and before each task. Update when you
> discover something that would save a future agent time.

## Project Conventions
- One model (Claude 3.5 Haiku) for all agent personas — personas come from system prompts, not different models
- Credits are fake currency (not API tokens) — fixed pool, zero-sum
- Results are immutable after analysis — iterate by creating new runs, not editing old ones
- findings/log.md is append-only

## Known Gotchas
- (none yet)

## Decisions Log
| Date | Decision | Context | Decided By |
|------|----------|---------|------------|
| 2026-02-24 | Name: Project Crucible | "Agora" had naming collision with existing AI lab | Beckham |
| 2026-02-24 | Claude 3.5 Haiku for PoC | Cheapest option (~$1-2 for full PoC), swap later if needed | Beckham |
| 2026-02-24 | Same model, different prompts | Isolates persona as the only variable — scientifically cleaner | Beckham |
| 2026-02-24 | Fake credits, not API tokens | Scarcity is simulated, not real. 10 credits per agent, zero-sum pool | Beckham |

## What Has Failed (Anti-Patterns)
- (none yet)

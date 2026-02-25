# AGENT.md — Project Knowledge Base

> Read this at session start and before each task. Update when you
> discover something that would save a future agent time.

## Project Conventions
- One model (Claude Haiku 4.5, ID: claude-haiku-4-5-20251001) for all agent personas — personas come from system prompts, not different models
- Credits are fake currency (not API tokens) — fixed pool, zero-sum
- Results are immutable after analysis — iterate by creating new runs, not editing old ones
- findings/log.md is append-only

## Known Gotchas
- Model ID `claude-3-5-haiku-20241022` returns 404. Use `claude-haiku-4-5-20251001` instead.
- RLHF cooperation bias: Equal starting credits + no maintenance cost = agents default to consensus regardless of persona prompts. Must add pressure mechanics (maintenance cost, unequal starts) to produce meaningful conflict.
- Agents will invent fictional shared resources in their memories even when no actual trades occurred. Don't trust agent memory — cross-reference with the actual interaction log.

## Decisions Log
| Date | Decision | Context | Decided By |
|------|----------|---------|------------|
| 2026-02-24 | Name: Project Crucible | "Agora" had naming collision with existing AI lab | Beckham |
| 2026-02-24 | Claude 3.5 Haiku for PoC | Cheapest option (~$1-2 for full PoC), swap later if needed | Beckham |
| 2026-02-24 | Same model, different prompts | Isolates persona as the only variable — scientifically cleaner | Beckham |
| 2026-02-24 | Fake credits, not API tokens | Scarcity is simulated, not real. 10 credits per agent, zero-sum pool | Beckham |

## What Has Failed (Anti-Patterns)
- Equal starting credits (10/10/10) with no survival cost produces zero economic activity. Agents have no reason to trade.
- "Rebel" persona prompt is too mild — the RLHF cooperation bias overrides it. Rebel voted yes on the first governance proposal and praised the system for 27 rounds.

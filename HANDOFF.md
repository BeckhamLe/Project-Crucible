# Project Crucible — Handoff

> Next agent: read this first, then follow the reading order below.

## Current State (updated: 2026-02-24)
- **Phase**: PoC (proof of concept — concept NOT yet proven)
- **Last completed**: poc_001 — baseline run showed RLHF cooperation bias, zero conflict
- **Next task**: Build and run poc_002 with pressure mechanics (maintenance cost + unequal starts + stronger prompts)
- **Blockers**: None
- **Open PRs**:
  - PR #1 (PRD): https://github.com/BeckhamLe/Project-Crucible/pull/1
  - PR #2 (poc_001 results): https://github.com/BeckhamLe/Project-Crucible/pull/2
  - PR #3 (model name fix): https://github.com/BeckhamLe/Project-Crucible/pull/3

## Read These Files (in order)
1. `docs/CRUCIBLE.md` — active state, agent assignments
2. `docs/AGENT.md` — gotchas, conventions, anti-patterns, decisions log
3. `findings/hypotheses.md` — what's been tested, what's queued (H4 and H5 are next)
4. `findings/log.md` — read the poc_001 entry for full context on what failed and why

## What the Next Agent Should Do
1. Merge the 3 open PRs to main (they're all approved/ready)
2. Create branch `run/poc-002-pressure` from main
3. Add **maintenance cost** mechanic to `sim/engine.py` — each agent loses 2 credits per round at the start of their turn. If credits hit 0, agent can still act but is "bankrupt" (visible to all)
4. Create `configs/templates/pressure.json` — 3 agents, 30 rounds, **unequal starts**: Builder=15, Rebel=5, Judge=10, maintenance_cost=2
5. Rewrite persona prompts in `sim/agents.py` — make them more aggressive, add explicit goals (e.g., Rebel: "your goal is to have the most credits and resist any rules that don't benefit you")
6. Run poc_002, analyze results, document findings in `findings/log.md`
7. Create PR with results

## What NOT to Do
- Don't use model ID `claude-3-5-haiku-20241022` — it 404s. Use `claude-haiku-4-5-20251001`
- Don't run equal starting credits (10/10/10) with no maintenance cost — produces zero conflict (proven in poc_001)
- Don't trust agent memory text as ground truth — agents invented a fictional "pooled venture" in poc_001 that never actually happened. Always cross-reference with the interaction log
- Don't create a new `.env` file — one already exists with the API key

## Session History
- Session 1: Verified experiment novelty (4 research agents), chose name "Project Crucible", scaffolded repo, built complete simulation engine (7 modules), created research harness, ran poc_001 (cooperative consensus — no conflict), documented findings, created PRD, set up GitHub repo with PR workflow

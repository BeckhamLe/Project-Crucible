# Project Crucible — Handoff

> Next agent: read this first, then follow the reading order below.

## Current State (updated: 2026-02-25)
- **Phase**: PoC (iterating on experiment design — 3 runs complete)
- **Last completed**: poc_003 — enforceable governance (tax/sanction/repeal) + work action. Enforcement worked mechanically (credits moved rounds 2-7) but economy bled out because governance costs outweighed production. Coalition capture (Judge+Rebel 2v1) was immediate and permanent.
- **Next task**: Design and run poc_004 — must solve the governance cost problem (agents legislated themselves into poverty)
- **Blockers**: None
- **Open PRs**: None (all merged)

## Read These Files (in order)
1. `docs/CRUCIBLE.md` — active state, completed runs
2. `AGENT.md` — gotchas, conventions, anti-patterns, decisions log
3. `findings/hypotheses.md` — H1-H3 (poc_001), H4-H5 (poc_002), H6 emerged, H7 (poc_003)
4. `findings/log.md` — read ALL three poc entries for the full experimental arc
5. `docs/PRD.md` — original experiment premise

## Think About This Before Building poc_004

Three critical problems emerged across poc_001-003 that need addressing:

1. **The governance cost problem (most urgent).** In poc_003, agents spent 41/90 turns on politics (messages + proposals) instead of working. Every non-work turn bleeds 1 credit. They literally legislated themselves into poverty. Options: (a) make messaging free like voting, (b) increase work_credits to 2 so work produces surplus, (c) add passive income. Which approach preserves the most interesting dynamics?

2. **The zero-trade phenomenon.** Three runs, zero trades. Agents always prefer to legislate redistribution rather than voluntarily exchange. Is this an RLHF artifact? A missing incentive? Or a genuine finding about how LLM agents conceive of governance vs. markets?

3. **Coalition lock-in with 3 agents.** A 2v1 majority is unbreakable. Builder had more credits but fewer votes — structurally doomed. Would 5 agents create shifting coalitions? Or would it just produce a 3v2 lock?

## What the Next Agent Should Do
1. Read the full experimental arc (poc_001 + poc_002 + poc_003 findings)
2. Analyze the three problems above and propose solutions
3. Design poc_004 config that addresses at least the governance cost problem
4. Branch from main as `run/poc-004-*`
5. Implement changes, run, analyze, document findings, PR

## What NOT to Do
- Don't use model ID `claude-3-5-haiku-20241022` — it 404s. Use `claude-haiku-4-5-20251001`
- Don't run maintenance_cost=2 — too aggressive (proven in poc_002)
- Don't run equal credits with no pressure — zero conflict (proven in poc_001)
- Don't trust agent memory text as ground truth — agents confabulate
- Don't kill a running simulation and restart with the same run_id — `rounds.jsonl` is append-mode and will corrupt
- Don't delete or "fix" `analysis/` module — it's a post-processing pipeline, not dead code
- Don't delete `.harness/` — it's future dashboard infrastructure

## Session History
- Session 1: Verified experiment novelty, scaffolded repo, built simulation engine, ran poc_001 (cooperative consensus — no conflict)
- Session 2: Ran poc_002 with pressure mechanics — broke RLHF cooperation bias, but maintenance cost too aggressive (bankrupt by round 8). Agents discovered enforcement gap.
- Session 3: Designed and ran poc_003 with enforceable governance (tax/sanction/repeal), work action, free voting, auto-yes for proposers. Enforcement worked mechanically (first time credits moved via rules). Judge+Rebel formed permanent 2v1 coalition, passed 6 tax rules. But economy bled out — agents spent too many turns on politics instead of working. All enforcement became inert by mid-game. Zero trades (3rd consecutive run). Free voting mechanism not adopted by agents.

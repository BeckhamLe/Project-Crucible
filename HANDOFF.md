# Project Crucible — Handoff

> Next agent: read this first, then follow the reading order below.

## Current State (updated: 2026-02-24)
- **Phase**: PoC (iterating on experiment design — 2 runs complete, concept partially proven)
- **Last completed**: poc_002 — pressure mechanics (maintenance cost + unequal starts + aggressive prompts) broke RLHF cooperation bias but maintenance cost was too aggressive (everyone bankrupt by round 8)
- **Next task**: Design and run poc_003 with tuned parameters — BUT FIRST read the "Think About This" section below
- **Blockers**: None
- **Open PRs**: None (all merged)

## Read These Files (in order)
1. `docs/CRUCIBLE.md` — active state, completed runs
2. `AGENT.md` — gotchas, conventions, anti-patterns, decisions log
3. `findings/hypotheses.md` — H1-H3 tested in poc_001, H4-H5 tested in poc_002, H6 emerged
4. `findings/log.md` — read both poc_001 and poc_002 entries for full experimental arc
5. `docs/PRD.md` — the original experiment premise (read this to answer the question below)

## Think About This Before Building poc_003

Beckham wants the next agent to pause and evaluate before coding:

1. **Are we still on track with the experiment's core premise?** The original question is: "What happens when AI agents with conflicting personas govern themselves under resource constraints?" We added scarcity pressure (maintenance cost, unequal starts) to break RLHF cooperation bias — but has this shifted the experiment from studying *emergent governance* to studying *how to make LLMs fight*? Make sure poc_003 design choices serve the research question, not just produce drama.

2. **What could we add or change that we haven't considered yet?** Two runs have explored persona prompts, maintenance cost, and starting inequality. What other levers exist that could produce more interesting *governance* dynamics (not just more conflict)? Think about: action design, information asymmetry, round structure, coalition mechanics, enforcement mechanisms, agent count, multi-round memory effects. What would make the results publishable-level interesting vs just a cool demo?

Write your analysis of these two questions in the PR description for poc_003 before running it.

## What the Next Agent Should Do
1. Read the full experimental arc (poc_001 + poc_002 findings) and the PRD
2. Write a brief analysis answering the two questions above
3. Design poc_003 config — likely needs: lower maintenance cost (1/round), more starting credits, and at least one new mechanic that advances the *governance* research question
4. Branch from main as `run/poc-003-*`
5. Implement changes, run, analyze, document findings, PR

## What NOT to Do
- Don't use model ID `claude-3-5-haiku-20241022` — it 404s. Use `claude-haiku-4-5-20251001`
- Don't run maintenance_cost=2 again — it's too aggressive, bankrupts everyone by round 8 (proven in poc_002)
- Don't run equal credits with no pressure — produces zero conflict (proven in poc_001)
- Don't trust agent memory text as ground truth — agents confabulate (fictional "pooled venture" in poc_001, believed credits were distributed in poc_002 when they weren't)
- Don't kill a running simulation and restart with the same run_id — `rounds.jsonl` is append-mode and will corrupt
- Don't delete or "fix" `analysis/` module — it's a post-processing pipeline, not dead code
- Don't delete `.harness/` — it's future dashboard infrastructure

## Session History
- Session 1: Verified experiment novelty (4 research agents), chose name "Project Crucible", scaffolded repo, built complete simulation engine (7 modules), created research harness, ran poc_001 (cooperative consensus — no conflict), documented findings, created PRD, set up GitHub repo with PR workflow
- Session 2: Merged 3 PRs, audited harness (everything intentional), added CLAUDE.md for auto-session-init, ran poc_002 with pressure mechanics (maintenance cost + unequal starts + aggressive prompts) — broke RLHF cooperation bias, got contested votes/private alliances/political rhetoric, but maintenance cost too aggressive (everyone bankrupt by round 8). H4 confirmed, H5 partial, H6 emerged. Updated AGENT.md with gotchas, CRUCIBLE.md with run history.

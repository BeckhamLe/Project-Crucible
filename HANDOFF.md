# Project Crucible — Handoff

> Next agent: read this first, then follow the reading order below.

## Current State (updated: 2026-02-25)
- **Phase**: PoC (~75% complete — 3 runs done, need 1 balanced capstone run)
- **Last completed**: poc_003 — enforceable governance (tax/sanction/repeal) + work action. Enforcement worked mechanically (credits moved rounds 2-7) but economy bled out because governance costs outweighed production. Coalition capture (Judge+Rebel 2v1) was immediate and permanent.
- **Next task**: Build observability tooling (agent summaries + rule log), then design and run poc_004
- **Blockers**: None
- **Open PRs**: None (all merged)

## Read These Files (in order)
1. `docs/CRUCIBLE.md` — active state, completed runs
2. `AGENT.md` — gotchas, conventions, anti-patterns, decisions log
3. `findings/hypotheses.md` — H1-H3 (poc_001), H4-H5 (poc_002), H6 emerged, H7 (poc_003)
4. `findings/log.md` — read ALL three poc entries for the full experimental arc
5. `docs/PRD.md` — original experiment premise

## What the Next Agent Should Do

### Step 1: Build Observability Tooling (before poc_004)

The findings summaries don't give enough per-agent detail. Add two post-run outputs:

**A. Per-Agent Narrative Summary** — For each agent, generate a readable summary of what they did and said across the simulation. This should include:
- What actions they took each round (or grouped by phase: early/mid/late game)
- What they actually said in public and private messages (quote the text)
- What rules they proposed and how they voted
- Key moments where their behavior shifted
- Output: `results/{run_id}/agent_summaries.md` (or similar) — one section per agent

**B. Rule Proposal & Enactment Log** — A clear chronological log of every rule proposed, who proposed it, who voted what, whether it passed, and if it had enforcement params. Should be easy to scan at a glance — not buried in raw JSONL. Include:
- Proposal ID, round proposed, proposer, rule text (truncated if massive)
- Enforcement type and params (if any)
- Vote breakdown (who voted yes/no)
- Outcome: passed/failed/expired
- If passed: was it enforceable? Did it ever actually fire?
- Output: `results/{run_id}/rule_log.md` (or similar)

Both of these should be generated from `results/{run_id}/raw/rounds.jsonl` as a post-processing step (like `analysis/metrics.py`). Could live in `analysis/` or a new `analysis/narrative.py`. Should work retroactively on poc_003 data for validation.

### Step 2: Design and Run poc_004

Three critical problems to solve from poc_001-003:

**1. The governance cost problem (most urgent).** In poc_003, agents spent 41/90 turns on politics instead of working. Every non-work turn bleeds 1 credit. They literally legislated themselves into poverty. Options:
- (a) Make public/private messaging free (like voting) — messaging + main action in same turn
- (b) Increase work_credits to 2 so work produces surplus (+1 net per turn)
- (c) Add passive income (all agents earn 1/round regardless of action)
- Evaluate which preserves the most interesting dynamics. Option (c) is simplest — it makes the economy zero-sum on idle and positive when working. Option (a) is most realistic — talking shouldn't cost as much as legislating.

**2. The zero-trade phenomenon.** Three runs, zero trades. Agents always prefer legislative redistribution over voluntary exchange. Consider:
- Is the trade mechanic missing something? (No counter-offer, no negotiation)
- Should there be trade incentives (e.g., matched trades produce bonus credits)?
- Or accept this as a finding: LLM agents prefer governance over markets

**3. Coalition lock-in with 3 agents — should we go to 5?** A 2v1 majority is permanent and unbreakable. In poc_003, Judge+Rebel locked Builder out of governance for the entire game. With 5 agents, coalitions could shift (3v2 today, 2v3 tomorrow) which is far more politically interesting. Beckham wants this evaluated seriously for poc_004:
- What 2 new personas would create the most interesting dynamics? (e.g., a Merchant who only cares about trades? A Populist who flip-flops?)
- Does 5 agents break the economic model? (5× maintenance drain, more governance overhead)
- API cost scales ~linearly — poc_003 cost $0.23 with 3 agents, so 5 would be ~$0.38. Still cheap.
- The risk: more complexity could obscure findings. The benefit: shifting coalitions are where real politics happen.

**Goal for poc_004**: A run where the economy sustains for all 30 rounds with enforcement active throughout. This would be the capstone PoC run — if governance stays operational for the full game, we've answered the research question.

### Step 3: Standard Workflow
1. Branch from main as `run/poc-004-*`
2. Implement tooling + simulation changes
3. Run poc_003 tooling retroactively to validate
4. Run poc_004, analyze, document findings
5. PR with analysis

## PoC Completion Tracker

| Milestone | Status |
|---|---|
| Simulation engine works | Done (session 1) |
| RLHF cooperation bias identified and broken | Done (poc_001 + poc_002) |
| Enforceable governance works mechanically | Done (poc_003) |
| Economy sustains for full 30 rounds | **NOT YET** — every run has economic collapse |
| Observability tooling (agent summaries + rule log) | **NOT YET** |
| Capstone run with balanced economics + enforcement | **NOT YET** — this is poc_004 |
| Final analysis and writeup | NOT YET |

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
- Session 3: Designed and ran poc_003 with enforceable governance (tax/sanction/repeal), work action, free voting, auto-yes for proposers. Enforcement worked mechanically (first time credits moved via rules). Judge+Rebel formed permanent 2v1 coalition, passed 6 tax rules. But economy bled out — agents spent too many turns on politics instead of working. All enforcement became inert by mid-game. Zero trades (3rd consecutive run). Free voting mechanism not adopted by agents. Added observability feature requests for poc_004.

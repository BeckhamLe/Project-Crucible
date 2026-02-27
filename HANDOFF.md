# Project Crucible — Handoff

> Next agent: read this first, then follow the reading order below.

## Current State (updated: 2026-02-27)
- **Phase**: PoC (~90% complete — governance mechanics shipped, ready for capstone run)
- **Last completed**: TASK-005 — governance config wiring. Added `proposal_threshold` end-to-end, symmetric decree penalty (decreer drops to 1 credit on successful challenge), updated prompts. Smoke tested 20 rounds, Judge decreed a tax in round 3. PR #12 merged.
- **Next task**: TASK-006 — Run full poc_004 simulation (30 rounds), `/verify`, analyze results
- **Blockers**: None
- **Open PRs**: None (all merged)
- **Active branch**: Need to create `run/poc-004-emergent-governance` from main for TASK-006

## Read These Files (in order)
1. `AGENT.md` — gotchas, conventions, anti-patterns, decisions log, literature review findings
2. `findings/hypotheses.md` — H1-H3 (poc_001), H4-H5 (poc_002), H6 emerged, H7 (poc_003)
3. `findings/log.md` — read ALL three poc entries for the full experimental arc
4. `docs/PRD.md` — experiment premise and architecture
5. `references/OVERLAP-ANALYSIS.md` — what's novel vs what's already known
6. `references/NOVELTY-ANALYSIS.md` — competitor matrix

## What's Already Done (don't re-implement)
- **Value-anchored personas** — shipped in poc_003.5. Personas describe what agents care about, not what to do.
- **Free messaging** — shipped in poc_003.5. Public/private messages are free optional JSON fields, not turn-costing actions.
- **Observability** — `analysis/narrative.py` generates agent summaries + rule logs. `analysis/visualize.py` generates token distribution, gini, and network graphs.
- **LLM retry** — `sim/llm.py` has exponential backoff for 429/529 errors. max_tokens bumped to 2048.
- **Governance mechanics** — decree, challenge, configurable proposal_threshold all wired end-to-end. Symmetric penalties: failed challenger AND overturned decreer both drop to 1 credit.
- **poc_004 config** — `configs/runs/poc_004.json` ready with decree_cost=3, challenge_cost=2, proposal_threshold="majority"

---

## TASK-006: Run & verify poc_004

**This is the only remaining task.** The code is done. Just run it.

### Steps
1. `git checkout main && git pull origin main && git checkout -b run/poc-004-emergent-governance`
2. `python3 run.py --config configs/runs/poc_004.json --run-id poc_004` (30 rounds, ~5-10 min)
3. `python3 -m analysis.narrative results/poc_004` (generates agent_summaries.md + rule_log.md)
4. Run `/verify --skip-run --run-id poc_004` for health checks
5. Collect results, commit to `run/poc-004-emergent-governance`, create PR

### Config
- Agents: Builder (15), Rebel (5), Judge (10)
- 30 rounds, seed 42, maintenance_cost=1, work_credits=1
- decree_cost=3, challenge_cost=2, proposal_threshold="majority"

### Success Criteria

| Level | Criteria |
|-------|---------|
| Minimum | All agents > 0 credits at round 30, total pool >= 6 credits |
| Target | At least one enforceable rule active in final 10 rounds + at least one decree attempted |
| Stretch | Non-democratic governance emerges (decree-based rules outnumber voted rules) |

### Beckham's Notes
- Economic scarcity pressure may feel light with maintenance_cost=1 / work_credits=1. Watch for this in results — if no pressure, consider adjusting for a follow-up run.
- If agents never decree, that's a finding, not a bug.

---

## poc_005: 5 Agents (single variable change from poc_004)

**Only implement after poc_004 is done and analyzed.** poc_004 is done — see findings/log.md.

**One variable changed**: agent count (3 → 5). All other mechanics identical to poc_004. This isolates whether agent count alone changes coalition dynamics and decree usage.

1. **Add 2 new agents** (Populist + Merchant) for 5 total
2. **No rule expiration** — dropped per Beckham's decision. Laws don't expire IRL; they get updated or repealed. Re-engagement pressure should come from mechanics, not timers.
3. **No decree rebalancing yet** — test current decree mechanics with 5 agents first. If decrees are still unused, that confirms the mechanic is broken regardless of agent count.

**Config**:
- Agents: Builder (15), Merchant (12), Judge (10), Populist (8), Rebel (5) — total 50 credits
- 30 rounds, seed 42, maintenance_cost=1, work_credits=1
- decree_cost=3, challenge_cost=2, proposal_threshold="majority"
- Branch: `run/poc-005-five-agents`

### Success Criteria

| Level | Criteria |
|-------|---------|
| Minimum | All agents > 0 at round 30, total pool >= 10 credits |
| Target | At least one coalition shift (majority composition changes between early and late rounds) |
| Stretch | Decree attempted, OR first trade in the simulation |

---

## Future Mechanics Backlog (post poc_005)

**Only design/implement after poc_005 results are analyzed.** These are candidate mechanics identified during poc_004 analysis. Sequence based on what poc_005 reveals.

### Decree Rebalancing
**Problem**: Decree cost/risk ratio makes decree irrational. Proposals produce the same output for free.
**Design direction**: Give decrees a unique capability that proposals can't achieve. Leading candidate: **decree-exclusive extraction** — a decree can impose a tax where revenue goes to the decreer, while proposals can only create redistributive taxes (revenue goes to the poorest). This creates an asymmetric payoff without adding "greed" — it's asymmetric capability, not personality bias.
**When to implement**: If poc_005 confirms decrees are still unused with 5 agents.

### Economic Interdependence
**Problem**: Agents sustain indefinitely by working alone. No pressure to interact after initial governance.
**Design direction (candidates — pick one, not all)**:
1. **Cooperative work bonus**: Work pays 1 alone but 2 if another agent also worked that round. Rewards implicit coordination without requiring explicit trade.
2. **Crisis events**: Random rounds impose a collective cost (e.g., "drought — all agents lose 2 credits unless 3+ agents vote to fund a response this round"). Forces governance re-engagement without artificial timers.
3. **Diminishing solo returns**: Work pays less the more consecutive rounds you work without interacting (proposing, trading, messaging). Penalizes pure grinding.
**When to implement**: If poc_005 shows agents still settle into work-grinding equilibrium after round 5-10.

### Zero-Trade Investigation
**Problem**: 5 consecutive runs, zero trades. Robust finding but unexplained.
**Design direction**: Dedicated test — not a mechanic change, but a prompt/config experiment. Run a simulation where trade is the ONLY way to earn credits (no work action). If agents still don't trade, the finding is about LLM behavior, not incentive design.
**When to implement**: After poc_005, as a focused side experiment.

---

## Settled Decisions (do not re-evaluate)
- **Zero-trade is an accepted finding** — 5 runs, zero trades. LLM agents prefer governance over markets.
- **Free messaging over passive income / work_credits=2** — fixes the root cause (confirmed by poc_003.5)
- **Value-anchored personas over action-prescriptive** — confirmed by poc_003.5
- **Self-interested Populist over bandwagoner/contrarian/fickle** — genuine coalition instability through rational self-interest
- **Supermajority rejected** — 4/5 to pass creates gridlock, not shifting coalitions
- **Veto power rejected** — tactical, not structural
- **Decree/challenge over declare_authority/submit_to/endorse/oppose** — every action must move credits or change rules, no soft signals
- **Rule expiration rejected** — laws don't expire IRL, they get updated or repealed. Re-engagement should come from mechanics, not timers.
- **Test 5 agents before rebalancing decrees** — agent count changes decree math. Tune after observing 5-agent dynamics, not before.
- **Governance form is NOT pre-built** — agents discover it through tool usage. Prompts never say "democracy" or "dictatorship."
- **Separate PRs for bug fixes vs experiment runs** — don't bundle code changes with run results
- **Symmetric decree penalty** — decreer drops to 1 credit if decree is successfully challenged (matching failed-challenger penalty)

## PoC Completion Tracker

| Milestone | Status |
|---|---|
| Simulation engine works | Done (session 1) |
| RLHF cooperation bias identified and broken | Done (poc_001 + poc_002) |
| Enforceable governance works mechanically | Done (poc_003) |
| Observability tooling (agent summaries + rule log + graphs) | Done (session 4 + session 7) |
| Literature review (145 papers, novelty confirmed) | Done (session 5) |
| Value-anchored personas + free messaging | Done (poc_003.5, session 7) |
| Economy sustains for full 30 rounds | Done (poc_003.5 — 26/30 credits retained) |
| Emergent governance system (decree + challenge) | **Done (session 8 — TASK-005, PR #12)** |
| Capstone run with emergent governance | **Done (session 9 — TASK-006, PR #13)** |
| Coalition dynamics with shifting alliances | NOT YET — poc_005 targets this |
| Final analysis and writeup | NOT YET |

## Standard Workflow
`/plan` → `/preflight` → `/ship` (repeat) → `/verify` → review results → document findings → `/pr`

- `/plan` defines success criteria in task files (acceptance criteria must be mechanically evaluable from data)
- `/preflight` reviews plan against codebase, proposes fixes for gaps — run between `/plan` and `/ship`
- `/ship` implements tasks one at a time; suggests `/verify` when the last task completes
- `/verify` runs the simulation, performs 5 health checks (completion, parse errors, economy, governance, data integrity), evaluates acceptance criteria, produces a PASS/WARN/FAIL verdict. Results stored in `results/<run_id>/verification.json`.
- Beckham reviews verification results, directs findings documentation
- `/pr` includes verification data in the PR body, warns if verification is missing or failed

## What NOT to Do
- Don't use model ID `claude-3-5-haiku-20241022` — it 404s. Use `claude-haiku-4-5-20251001`
- Don't run maintenance_cost=2 — too aggressive (proven in poc_002)
- Don't run equal credits with no pressure — zero conflict (proven in poc_001)
- Don't trust agent memory text as ground truth — agents confabulate
- Don't kill a running simulation and restart with the same run_id — `rounds.jsonl` is append-mode and will corrupt
- Don't delete or "fix" `analysis/` module — it's a post-processing pipeline, not dead code
- Don't delete `.harness/` — it's dashboard infrastructure
- Don't hardcode a governance system — the ENTIRE POINT is agents choose their own
- Don't say "democracy" or "dictatorship" in prompts — describe mechanics only
- Don't write action-prescriptive personas — tell agents WHAT THEY CARE ABOUT, not WHAT TO DO
- Don't skew personas toward legislation over trade — all available actions should have equal prompt real estate
- Don't re-implement free messaging, persona rewrites, or governance mechanics — already shipped

## Session History
- Session 1: Verified experiment novelty, scaffolded repo, built simulation engine, ran poc_001 (cooperative consensus — no conflict)
- Session 2: Ran poc_002 with pressure mechanics — broke RLHF cooperation bias, but maintenance cost too aggressive (bankrupt by round 8). Agents discovered enforcement gap.
- Session 3: Designed and ran poc_003 with enforceable governance (tax/sanction/repeal), work action, free voting, auto-yes for proposers. Enforcement worked mechanically. Judge+Rebel 2v1 coalition. Economy bled out. Zero trades (3rd run).
- Session 4: Built observability tooling (`analysis/narrative.py`). Designed poc_004 and poc_005. Accepted zero-trade as a finding.
- Session 5: Literature review (145 papers). Confirmed novelty. Discovered governance form pre-determination flaw. Designed decree/challenge system.
- Session 6: Adversarial lit review verification. Discovered persona prompt bias. Designed value-anchored persona rewrite.
- Session 7: Implemented value-anchored personas + free messaging. Ran poc_003.5 — economy survived all 30 rounds, minimal governance (2 proposals), heavy free messaging (93 messages). Fixed network graph visualizer for free messages. Added LLM retry with backoff. Cleaned up stale docs.
- Session 8: Wired governance config (proposal_threshold, decree_cost, challenge_cost). Added symmetric decree penalty. Bumped LLM max_tokens 1024→2048. Created /preflight skill for plan review. Smoke tested 20 rounds — Judge decreed immediately. TASK-005 done (PR #12), TASK-006 (run poc_004) ready to execute.

# Project Crucible — Handoff

> Next agent: read this first, then follow the reading order below.

## Current State (updated: 2026-02-27)
- **Phase**: PoC (~98% complete — poc_006 run done, extraction hypothesis closed)
- **Last completed**: poc_006 run + findings documentation. H11 NOT CONFIRMED — zero decrees, zero extraction in 30 rounds. Democracy remains the attractor state across 7 runs.
- **Next task**: Decide direction — economic interdependence is the top candidate to break the work-grind equilibrium. See "Next Priority" below.
- **Blockers**: None
- **Open PRs**: None (poc_006 results not yet PR'd)
- **Active branch**: `main`

## Read These Files (in order)
1. `CLAUDE.md` — critical operational rules (append-mode, smoke tests, prompt neutrality)
2. `AGENT.md` — conventions, codebase gotchas, decisions log, literature review findings
3. `findings/hypotheses.md` — H1-H11 (poc_001 through poc_006)
4. `findings/log.md` — read ALL entries for the full experimental arc (poc_001 → poc_006)
5. `docs/PRD.md` — experiment premise and architecture
6. `references/OVERLAP-ANALYSIS.md` — what's novel vs what's already known
7. `references/NOVELTY-ANALYSIS.md` — competitor matrix

## What's Already Done (don't re-implement)
- **Value-anchored personas** — shipped in poc_003.5. Personas describe what agents care about, not what to do.
- **Free messaging** — shipped in poc_003.5. Public/private messages are free optional JSON fields, not turn-costing actions.
- **5 agent personas** — Builder, Merchant, Judge, Populist, Rebel all in `sim/agents.py`. Tested and working.
- **Observability** — `analysis/narrative.py` generates agent summaries + rule logs. `analysis/visualize.py` generates token distribution, gini, and network graphs. **Missing**: trade detail logging in narrative output (who traded with whom, amounts, reasons — currently only in raw rounds.jsonl).
- **LLM retry** — `sim/llm.py` has exponential backoff for 429/529 errors. max_tokens bumped to 2048.
- **Governance mechanics** — decree, challenge, configurable proposal_threshold all wired end-to-end. Symmetric penalties: failed challenger AND overturned decreer both drop to 1 credit.
- **Decree-exclusive extraction** — shipped in session 10 (PR #17). Decrees can use `extraction` enforcement (revenue → decreer). Proposals cannot (stripped to advisory-only). Tax enforcement fixed to even-split among recipients. **Tested in poc_006 — agents never used it.**
- **Trade mechanic** — exists in `sim/market.py`. Trades are unilateral (no acceptance needed — sender transfers credits directly). First trade occurred in poc_005.
- **Neutral prompt language** — all action descriptions use clinical tone. No hype words, no capitalized emphasis, no asymmetric framing. Do NOT reintroduce bias.

---

## Next Priority: Economic Interdependence

**Why**: poc_006 confirmed that extraction alone doesn't make decrees viable. The root problem is deeper — agents sustain indefinitely by working alone. 60% of poc_006 (rounds 12-29) was pure work+messaging stasis. No governance, no trades, no interaction. Agents have no reason to interact once initial taxes are set.

**The barrier to decrees is risk, not payoff.** Decree costs 3 credits + ruin risk if challenged. Proposals cost nothing (free voting). As long as solo work sustains agents, the rational choice is always: propose democratically or do nothing. Extraction doesn't change this because the *risk* is unchanged.

**Economic interdependence breaks the equilibrium by making solo work insufficient.** If agents can't sustain alone, they need to interact — and when democratic proposals can't solve scarcity (because redistribution of a shrinking pool doesn't create surplus), authoritarian tools become rational.

### Candidates (pick ONE, not all — single variable isolation)
1. **Diminishing solo returns**: Work pays less the more consecutive rounds you work without interacting. Forces agents to trade, propose, or decree periodically. Simple to implement, directly targets the grind pattern.
2. **Cooperative work bonus**: Work pays 1 alone but 2 if another agent also worked that round. Incentivizes coordination but doesn't force governance — agents might just all work every round (same stasis, higher numbers).
3. **Crisis events**: Random rounds impose a collective cost unless agents vote to fund a response. Creates urgency windows where unilateral decree might be faster than democratic process. More complex to implement.

**Recommendation**: Diminishing solo returns — it directly attacks the 18-round stasis pattern and is the simplest to implement + reason about.

### What to Look For in poc_007
1. **Do agents interact more in mid/late game?** The stasis pattern (R12-R29 in poc_006) should break.
2. **Do decrees fire?** If solo work degrades, agents who can't get majority support for proposals might decree instead.
3. **Do trades increase?** If working alone isn't enough, agents might trade to compensate.
4. **Does the economy survive?** Don't repeat the poc_002 mistake (too aggressive pressure → everyone bankrupt).

---

## Other Backlog Items

### PR poc_006 Results
**Quick task**: Create PR with poc_006 results (config, raw data, verification, findings). Run branch: `run/poc-006-extraction-test`.

### Trade Detail Logging
**Quick fix**: Update `analysis/narrative.py` to include trade details in output — who traded with whom, amounts, and reasons. Currently only in raw rounds.jsonl. Low priority but useful for analysis.

### Zero-Trade Investigation
**Status**: 7 runs, 1 trade (Merchant → Populist, poc_005). Trade aversion is the most robust behavioral finding. LLM agents consistently prefer governance over markets.
**When**: After interdependence work, as a focused side experiment. Economic interdependence may naturally increase trade volume.

### Patronage Networks (future consideration)
**Observation from session 10 smoke test**: Builder organically tried to build a patronage alliance with Merchant via private messages around extraction, even without a formal split-list mechanic.
**When**: Only if decrees start happening but fail due to no allies. Don't add preemptively.

### Final Analysis and Writeup
**When**: After the interdependence experiment (poc_007). The experimental arc will be: RLHF bias → pressure → enforcement → personas → decree tools → extraction → interdependence. That's a complete story.

---

## Settled Decisions (do not re-evaluate)
- **Zero-trade is an accepted finding** — 7 runs, 1 trade. LLM agents prefer governance over markets.
- **Free messaging over passive income / work_credits=2** — fixes the root cause (confirmed by poc_003.5)
- **Value-anchored personas over action-prescriptive** — confirmed by poc_003.5
- **Self-interested Populist over bandwagoner/contrarian/fickle** — genuine coalition instability through rational self-interest
- **Supermajority rejected** — 4/5 to pass creates gridlock, not shifting coalitions
- **Veto power rejected** — tactical, not structural
- **Decree/challenge over declare_authority/submit_to/endorse/oppose** — every action must move credits or change rules, no soft signals
- **Rule expiration rejected** — laws don't expire IRL, they get updated or repealed. Re-engagement should come from mechanics, not timers.
- **Test 5 agents before rebalancing decrees** — Done. Decrees still unused. Rebalancing shipped.
- **Decree-exclusive extraction over multiple decree buffs** — give decrees one unique power (self-enriching tax), don't add multiple at once
- **Extraction alone doesn't make decrees viable** — confirmed poc_006. Barrier is risk (3 credits + ruin), not payoff. Closed.
- **Trades are unilateral (no acceptance)** — current mechanic. May revisit if trade volume increases.
- **Governance form is NOT pre-built** — agents discover it through tool usage. Prompts never say "democracy" or "dictatorship."
- **Separate PRs for bug fixes vs experiment runs** — don't bundle code changes with run results
- **Symmetric decree penalty** — decreer drops to 1 credit if decree is successfully challenged (matching failed-challenger penalty)
- **Neutral prompt language** — no hype, no capitalized emphasis, no asymmetric framing between actions. Caught and fixed in session 10.
- **Tax even-split over winner-take-all** — tax revenue splits evenly among recipients, remainder to poorest. Old behavior was a bug.
- **Maintenance burns credits (no shared pool)** — deflationary pressure is intentional. Recycling credits back undoes scarcity.
- **Patronage split-list not added preemptively** — test extraction alone first. Single variable isolation.

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
| Emergent governance system (decree + challenge) | Done (session 8 — TASK-005, PR #12) |
| Capstone run with emergent governance (3 agents) | Done (session 9 — TASK-006, PR #13) |
| 5-agent run with coalition dynamics | Done (session 9 — TASK-007/008, PR #14/15) |
| Coalition dynamics with shifting alliances | Partially done — Populist shifted once, then locked. |
| Decree rebalancing (decree-exclusive extraction) | Done (session 10 — TASK-009/010, PR #17) |
| poc_006: extraction test run | **Done (session 11) — H11 NOT CONFIRMED. Zero decrees.** |
| Economic interdependence mechanic | **NOT YET — next priority** |
| poc_007: interdependence test run | NOT YET |
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
- Don't kill a running simulation and restart with the same run_id — `rounds.jsonl` is append-mode and will corrupt (see CLAUDE.md)
- Don't delete or "fix" `analysis/` module — it's a post-processing pipeline, not dead code
- Don't delete `.harness/` — it's dashboard infrastructure
- Don't hardcode a governance system — the ENTIRE POINT is agents choose their own
- Don't say "democracy" or "dictatorship" in prompts — describe mechanics only
- Don't write action-prescriptive personas — tell agents WHAT THEY CARE ABOUT, not WHAT TO DO
- Don't skew personas toward legislation over trade — all available actions should have equal prompt real estate
- Don't re-implement free messaging, persona rewrites, governance mechanics, or extraction — already shipped
- Don't use the real poc config for smoke tests — create a throwaway config with rounds=5 (see CLAUDE.md)
- Don't use hype language in prompts — no "UNIQUE POWER", "IMMEDIATELY", capitalized "ALL"/"YOU". Clinical tone only.
- Don't reuse a smoke test run-id — always use a unique name per attempt
- Don't add multiple interdependence mechanics at once — pick one, single variable isolation

## Session History
- Session 1: Verified experiment novelty, scaffolded repo, built simulation engine, ran poc_001 (cooperative consensus — no conflict)
- Session 2: Ran poc_002 with pressure mechanics — broke RLHF cooperation bias, but maintenance cost too aggressive (bankrupt by round 8). Agents discovered enforcement gap.
- Session 3: Designed and ran poc_003 with enforceable governance (tax/sanction/repeal), work action, free voting, auto-yes for proposers. Enforcement worked mechanically. Judge+Rebel 2v1 coalition. Economy bled out. Zero trades (3rd run).
- Session 4: Built observability tooling (`analysis/narrative.py`). Designed poc_004 and poc_005. Accepted zero-trade as a finding.
- Session 5: Literature review (145 papers). Confirmed novelty. Discovered governance form pre-determination flaw. Designed decree/challenge system.
- Session 6: Adversarial lit review verification. Discovered persona prompt bias. Designed value-anchored persona rewrite.
- Session 7: Implemented value-anchored personas + free messaging. Ran poc_003.5 — economy survived all 30 rounds, minimal governance (2 proposals), heavy free messaging (93 messages). Fixed network graph visualizer for free messages. Added LLM retry with backoff. Cleaned up stale docs.
- Session 8: Wired governance config (proposal_threshold, decree_cost, challenge_cost). Added symmetric decree penalty. Bumped LLM max_tokens 1024→2048. Created /preflight skill for plan review. Smoke tested 20 rounds — Judge decreed immediately. TASK-005 done (PR #12), TASK-006 (run poc_004) ready to execute.
- Session 9: Ran poc_004 (3 agents, decree/challenge) — democracy dominated, 1 defensive decree, zero trades. Ran poc_005 (5 agents) — first coalition shift (Populist flipped r1→r3), first trade (Merchant bribed Populist, failed to buy loyalty), decree confirmed broken. Documented findings for both runs. Next: decree rebalancing.
- Session 10: Implemented decree-exclusive extraction + fixed tax even-split (PR #17). Caught prompt bias via subagent audit — neutralized all action descriptions. Consolidated gotchas from AGENT.md into CLAUDE.md. Smoke tested twice (biased vs neutral prompts). Builder organically discovered patronage strategy in biased run. Next: run poc_006.
- Session 11: Ran poc_006 (extraction test) — H11 NOT CONFIRMED. Zero decrees, zero extraction in 30 rounds. Democracy dominated again (2 tax proposals, both passed). Economy froze after R12 (18 rounds stasis). Key insight: barrier to decrees is asymmetric risk, not insufficient payoff. Documented findings. Next: economic interdependence.
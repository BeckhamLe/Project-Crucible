# Project Crucible — Handoff

> Next agent: read this first, then follow the reading order below.

## Current State (updated: 2026-02-27)
- **Phase**: PoC (~97% complete — decree rebalancing shipped, poc_006 run is next)
- **Last completed**: TASK-009/010 — Decree-exclusive extraction + tax redistribution fix + smoke test. Merged as PR #17.
- **Next task**: Run poc_006 — 5 agents, 30 rounds, same config as poc_005 but with extraction mechanic now in the code. This is a `run/` branch, not a `feat/` branch.
- **Blockers**: None
- **Open PRs**: None
- **Active branch**: `main`

## Read These Files (in order)
1. `CLAUDE.md` — critical operational rules (append-mode, smoke tests, prompt neutrality)
2. `AGENT.md` — conventions, codebase gotchas, decisions log, literature review findings
3. `findings/hypotheses.md` — H1-H10 (poc_001 through poc_005)
4. `findings/log.md` — read ALL entries for the full experimental arc (poc_001 → poc_005)
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
- **Decree-exclusive extraction** — shipped in session 10 (PR #17). Decrees can use `extraction` enforcement (revenue → decreer). Proposals cannot (stripped to advisory-only). Tax enforcement fixed to even-split among recipients.
- **Trade mechanic** — exists in `sim/market.py`. Trades are unilateral (no acceptance needed — sender transfers credits directly). First trade occurred in poc_005.
- **Neutral prompt language** — all action descriptions use clinical tone. No hype words, no capitalized emphasis, no asymmetric framing. Do NOT reintroduce bias.

---

## Next Priority: Run poc_006

**Goal**: Test whether extraction makes decrees viable. Single variable isolation — the only change from poc_005 is the extraction enforcement type + tax even-split fix in the code.

### Setup
- Create `configs/runs/poc_006.json` — copy poc_005 config, update hypothesis text
- Same params: 5 agents, 30 rounds, same token distribution, same decree/challenge costs
- Run on a `run/poc-006-extraction-test` branch
- Use `/plan` → `/ship` → `/verify` workflow

### What to Look For
1. **Do any agents decree with extraction?** This is the primary question.
2. **If yes**: Does the challenge mechanic fire? Does the extraction get overturned? Who challenges?
3. **If no**: Extraction alone isn't enough incentive. Next step would be economic interdependence from backlog.
4. **Coalition dynamics**: Does the Populist shift allegiances? Do alliances form around extraction?
5. **Tax even-split**: Verify the fixed redistribution works correctly over 30 rounds.

### Smoke Test Results (session 10)
- Biased prompts: Builder planned extraction decree by round 4, was forming patronage alliance with Merchant via private messages
- Neutral prompts: No decree attempts in 5 rounds, 2 tax proposals passed, even-split working
- The difference confirms prompt neutrality matters — behavior should be emergent, not prompted

---

## Other Backlog Items (after poc_006)

### Trade Detail Logging
**Quick fix**: Update `analysis/narrative.py` to include trade details in output — who traded with whom, amounts, and reasons. Currently only in raw rounds.jsonl. Low priority but useful for analysis.

### Economic Interdependence
**Problem**: Agents sustain indefinitely by working alone. No pressure to interact after initial governance.
**Candidates (pick one, not all)**:
1. **Cooperative work bonus**: Work pays 1 alone but 2 if another agent also worked that round
2. **Crisis events**: Random rounds impose a collective cost unless agents vote to fund a response
3. **Diminishing solo returns**: Work pays less the more consecutive rounds you work without interacting
**When**: If agents still grind-to-equilibrium after decree rebalancing

### Zero-Trade Investigation
**Status**: 6 runs, 1 trade (Merchant → Populist, poc_005). The trade-motivated persona produced the first trade — persona design matters. But still nearly zero trading overall.
**When**: After decree work, as a focused side experiment

### Patronage Networks (future consideration)
**Observation from smoke test**: Builder organically tried to build a patronage alliance with Merchant via private messages around extraction, even without a formal split-list mechanic. Agents may discover patronage through existing tools (decree + trade + private messaging) without needing a new mechanic.
**When**: Only if poc_006 shows decrees happening but failing immediately due to no allies. Don't add this preemptively.

---

## Settled Decisions (do not re-evaluate)
- **Zero-trade is an accepted finding** — 6 runs, 1 trade. LLM agents prefer governance over markets.
- **Free messaging over passive income / work_credits=2** — fixes the root cause (confirmed by poc_003.5)
- **Value-anchored personas over action-prescriptive** — confirmed by poc_003.5
- **Self-interested Populist over bandwagoner/contrarian/fickle** — genuine coalition instability through rational self-interest
- **Supermajority rejected** — 4/5 to pass creates gridlock, not shifting coalitions
- **Veto power rejected** — tactical, not structural
- **Decree/challenge over declare_authority/submit_to/endorse/oppose** — every action must move credits or change rules, no soft signals
- **Rule expiration rejected** — laws don't expire IRL, they get updated or repealed. Re-engagement should come from mechanics, not timers.
- **Test 5 agents before rebalancing decrees** — Done. Decrees still unused. Rebalancing shipped.
- **Decree-exclusive extraction over multiple decree buffs** — give decrees one unique power (self-enriching tax), don't add multiple at once
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
| Coalition dynamics with shifting alliances | Partially done — Populist shifted once, then locked. Need decree rebalancing for sustained dynamics. |
| Decree rebalancing (decree-exclusive extraction) | **Done (session 10 — TASK-009/010, PR #17)** |
| poc_006: extraction test run | **NOT YET — next priority** |
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

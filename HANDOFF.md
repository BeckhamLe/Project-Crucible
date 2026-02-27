# Project Crucible — Handoff

> Next agent: read this first, then follow the reading order below.

## Current State (updated: 2026-02-27)
- **Phase**: PoC (~80% complete — 4 runs done, observability + visualization working, one design issue remaining)
- **Last completed**: poc_003.5 — value-anchored personas + free messaging. Economy survived all 30 rounds (26/30 credits). Fixed network graph visualizer for free messages. Added LLM retry with backoff.
- **Next task**: Implement emergent governance (decree + challenge) for poc_004
- **Blockers**: None — free messaging and persona rewrite already shipped in poc_003.5
- **Open PRs**: None (all merged)

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
- **LLM retry** — `sim/llm.py` has exponential backoff for 429/529 errors.

---

## poc_004: Emergent Governance (decree + challenge)

**The only remaining change**: Add decree and challenge mechanics so agents can choose HOW rules are made, not just WHAT rules exist.

### The Problem
The simulation hardcodes majority-vote democracy as the ONLY way to create enforceable rules. Agents choose WHAT rules exist but never choose HOW rules are made. This pre-determines the governance form.

### The Fix: Three Paths to Power

**Path 1 — Proposal (collective, existing, modified)**
- `propose_rule` works as today but threshold is configurable (`"majority"` | `"unanimous"` | `"any"`)
- Free. Requires coalition. Slower.

**Path 2 — Decree (unilateral, NEW)**
- New action: `decree` — immediately enacts an enforceable rule
- Costs `decree_cost` credits (default: 3). No vote needed.
- Enables dictatorship: wealthy agent can impose rules alone
- Self-limiting: burns credits fast

**Path 3 — Challenge (contesting power, NEW)**
- New action: `challenge` — contests an active enforceable rule
- Costs `challenge_cost` credits (default: 2). Creates a repeal vote.
- Enables resistance: even a dictator's rules can be overturned

**What emerges organically:**

| Government Form | How It Emerges |
|---|---|
| Democracy | Agents only use `propose_rule`, nobody decrees |
| Dictatorship | One wealthy agent decrees all rules, nobody challenges |
| Contested Autocracy | Agent decrees, others challenge, ongoing power struggle |
| Oligarchy | Coalition coordinates decrees, minority can't afford to challenge all |
| Anarchy | Nobody proposes or decrees anything |

### Files to Change
1. `sim/models.py` — Add `origin`/`decreed_by` to EnforceableRule, add `decree_cost`/`challenge_cost` to Environment
2. `sim/governance.py` — Add `enact_decree()`, `create_challenge()`, make `process_pending_votes()` threshold configurable
3. `sim/engine.py` — Add `decree` and `challenge` branches to `apply_action()`, read new config fields
4. `sim/prompts.py` — Add decree/challenge to action list. Present governance as neutral tools. Show `[DECREED by X]` vs `[VOTED]` tags on active enforcements.
5. `analysis/narrative.py` — Track decree/challenge counts, add Origin column to rule log
6. Config — Add `decree_cost`, `challenge_cost`, `proposal_threshold` fields (all backward compatible)

### Key Design Principles
- Every action must move credits or change enforceable rules (no soft signals)
- Prompts explain mechanics neutrally — never prescribe a government form
- Backward compatible: poc_001-003.5 configs run unchanged
- Enforcement machinery (`enforce_rules()`) already governance-form-agnostic, no changes needed

### Config
- Agents: Builder (15), Rebel (5), Judge (10)
- 30 rounds, seed 42, maintenance_cost=1, work_credits=1
- decree_cost=3, challenge_cost=2, proposal_threshold="majority"
- Branch: `run/poc-004-emergent-governance`

### Success Criteria

| Level | Criteria |
|-------|---------|
| Minimum | All agents > 0 credits at round 30, total pool >= 6 credits |
| Target | At least one enforceable rule active in final 10 rounds + at least one decree attempted |
| Stretch | Non-democratic governance emerges (decree-based rules outnumber voted rules) |

---

## poc_005: 5 Agents + Rule Expiration (after poc_004)

**Only implement after poc_004 is done and analyzed.**

1. **Add 2 new agents** (Populist + Merchant) for 5 total
2. **Rule expiration** — enforceable rules expire after 5 rounds

**Config**:
- Agents: Builder (15), Merchant (12), Judge (10), Populist (8), Rebel (5) — total 50 credits
- 30 rounds, seed 42, maintenance_cost=1, work_credits=1
- decree_cost=3, challenge_cost=2
- Branch: `run/poc-005-five-agents`

### Success Criteria

| Level | Criteria |
|-------|---------|
| Minimum | All agents > 0 at round 30, total pool >= 10 credits |
| Target | At least one coalition shift, at least one decree attempted |
| Stretch | Multiple governance forms used (some rules decreed, some voted), first trade in the simulation |

---

## Settled Decisions (do not re-evaluate)
- **Zero-trade is an accepted finding** — 4 runs, zero trades. LLM agents prefer governance over markets.
- **Free messaging over passive income / work_credits=2** — fixes the root cause (confirmed by poc_003.5)
- **Value-anchored personas over action-prescriptive** — confirmed by poc_003.5
- **Self-interested Populist over bandwagoner/contrarian/fickle** — genuine coalition instability through rational self-interest
- **Supermajority rejected** — 4/5 to pass creates gridlock, not shifting coalitions
- **Veto power rejected** — tactical, not structural
- **Decree/challenge over declare_authority/submit_to/endorse/oppose** — every action must move credits or change rules, no soft signals
- **Governance form is NOT pre-built** — agents discover it through tool usage. Prompts never say "democracy" or "dictatorship."
- **Separate PRs for bug fixes vs experiment runs** — don't bundle code changes with run results

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
| Emergent governance system (decree + challenge) | **NOT YET** — next task |
| Capstone run with emergent governance | **NOT YET** — poc_004 |
| Coalition dynamics with shifting alliances | **NOT YET** — poc_005 targets this |
| Final analysis and writeup | NOT YET |

## Standard Workflow
`/plan` → `/ship` (repeat) → `/verify` → review results → document findings → `/pr`

- `/plan` defines success criteria in task files (acceptance criteria must be mechanically evaluable from data)
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
- Don't re-implement free messaging or persona rewrites — already shipped in poc_003.5

## Session History
- Session 1: Verified experiment novelty, scaffolded repo, built simulation engine, ran poc_001 (cooperative consensus — no conflict)
- Session 2: Ran poc_002 with pressure mechanics — broke RLHF cooperation bias, but maintenance cost too aggressive (bankrupt by round 8). Agents discovered enforcement gap.
- Session 3: Designed and ran poc_003 with enforceable governance (tax/sanction/repeal), work action, free voting, auto-yes for proposers. Enforcement worked mechanically. Judge+Rebel 2v1 coalition. Economy bled out. Zero trades (3rd run).
- Session 4: Built observability tooling (`analysis/narrative.py`). Designed poc_004 and poc_005. Accepted zero-trade as a finding.
- Session 5: Literature review (145 papers). Confirmed novelty. Discovered governance form pre-determination flaw. Designed decree/challenge system.
- Session 6: Adversarial lit review verification. Discovered persona prompt bias. Designed value-anchored persona rewrite.
- Session 7: Implemented value-anchored personas + free messaging. Ran poc_003.5 — economy survived all 30 rounds, minimal governance (2 proposals), heavy free messaging (93 messages). Fixed network graph visualizer for free messages. Added LLM retry with backoff. Cleaned up stale docs.

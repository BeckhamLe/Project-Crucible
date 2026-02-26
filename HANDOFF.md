# Project Crucible — Handoff

> Next agent: read this first, then follow the reading order below.

## Current State (updated: 2026-02-25)
- **Phase**: PoC (~75% complete — 3 runs done, observability tooling done, CRITICAL DESIGN ISSUE identified)
- **Last completed**: Literature review (145 papers, novelty confirmed) + identified that hardcoded majority-vote system undermines "governance from scratch" claim
- **Next task**: Implement emergent governance system (decree + challenge actions), THEN poc_004 free messaging, THEN poc_005
- **Blockers**: Emergent governance redesign must happen before further PoC runs — it changes the core experiment
- **Open PRs**: None (all merged)

## Read These Files (in order)
1. `AGENT.md` — gotchas, conventions, anti-patterns, decisions log, **literature review findings**
2. `docs/CRUCIBLE.md` — active state, completed runs
3. `findings/hypotheses.md` — H1-H3 (poc_001), H4-H5 (poc_002), H6 emerged, H7 (poc_003)
4. `findings/log.md` — read ALL three poc entries for the full experimental arc
5. `docs/PRD.md` — original experiment premise
6. `references/OVERLAP-ANALYSIS.md` — what's novel vs what's already known
7. `references/NOVELTY-ANALYSIS.md` — competitor matrix

## CRITICAL: The Governance Redesign

### The Problem
The experiment claims "agents invent governance from scratch" but the simulation hardcodes a **majority-vote democratic system** as the ONLY way to create enforceable rules. Agents choose WHAT rules exist but never choose HOW rules are made. This pre-determines the governance form. The literature review confirmed this is the exact gap between Crucible and competitors like Artificial Leviathan (which lets hierarchy emerge through pure social pressure).

### The Fix: Three Paths to Power
Instead of one path (propose → majority vote → enforceable), give agents three primitive political tools and let the government form emerge from which tools they use:

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

### Implementation Plan (see full plan at `.claude/plans/hazy-tinkering-conway.md`)

**Files to change:**
1. `sim/models.py` — Add `origin`/`decreed_by` to EnforceableRule, add `decree_cost`/`challenge_cost` to Environment
2. `sim/governance.py` — Add `enact_decree()`, `create_challenge()`, make `process_pending_votes()` threshold configurable
3. `sim/engine.py` — Add `decree` and `challenge` branches to `apply_action()`, read new config fields
4. `sim/prompts.py` — Rewrite action list to present governance as neutral tools. NEVER say "democracy" or "dictatorship." Show `[DECREED by X]` vs `[VOTED]` tags on active enforcements.
5. `analysis/narrative.py` — Track decree/challenge counts, add Origin column to rule log
6. Config — Add `decree_cost`, `challenge_cost`, `proposal_threshold` fields (all backward compatible)

**Key design principles:**
- Every action must move credits or change enforceable rules (no soft signals)
- Prompts explain mechanics neutrally — never prescribe a government form
- Backward compatible: poc_001-003 configs run unchanged
- Enforcement machinery (`enforce_rules()`) already governance-form-agnostic, no changes needed

### Implementation Sequence
1. **First**: Implement emergent governance (decree + challenge) — this is the foundational change
2. **Second**: Implement free messaging (poc_004 design below) — fixes economic bleed
3. **Third**: Run poc_004 with BOTH changes (emergent governance + free messaging)
4. **Fourth**: If poc_004 succeeds, implement poc_005 (5 agents + rule expiration)

---

## poc_004: Free Messaging + Emergent Governance

**Hypothesis**: Free messaging fixes governance cost problem AND emergent governance tools (decree/challenge) produce non-democratic political structures.

**Two variable changes** (combined because emergent governance is a prerequisite):
1. Public and private messages become free actions (same pattern as free voting)
2. Decree and challenge actions available

**Config**:
- Agents: Builder (15), Rebel (5), Judge (10)
- 30 rounds, seed 42, maintenance_cost=1, work_credits=1
- decree_cost=3, challenge_cost=2, proposal_threshold="majority"
- Branch: `run/poc-004-emergent-governance`

### Free Messaging Implementation

**`sim/prompts.py`** — Move messaging to free optional top-level JSON fields (like votes):
- New format: `"public_message": "text"` and `"private_message": {"to": "AgentName", "message": "text"}` as top-level optional fields
- Create "FREE ACTIONS" section explaining votes + messaging
- Reduce main action list: work, trade, propose_rule, decree, challenge, vote, nothing

**`sim/engine.py`**:
- `parse_action()`: Extract `public_message` and `private_message` from parsed JSON, pop them, build message dicts
- `agent_turn()`: After free votes block, add parallel block for free messages. Log as `"free_public_message"` / `"free_private_message"`
- `run_simulation()`: Change `round_log.append` to `round_log.extend`

**`analysis/narrative.py`**: Add free message types to tracking

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

### New Persona: Populist (Self-Interested)

```
You are the Populist. Your GOAL is to end the game with the most credits.
You have NO ideology — you don't care about fairness, freedom, or equality.
You vote YES on any proposal that directly increases your credits and NO on
anything that costs you. You will join whichever coalition offers you the best
deal THIS round — but you will betray them the moment a better offer appears.
You are not loyal. You are not principled. You are purely transactional.
If both sides offer the same deal, you side with whoever has fewer members
(because a smaller coalition means a bigger share of the spoils for you).
You will publicly announce what your vote costs — make both sides compete for
your support. You prefer to WORK and accumulate, and you resent any rule that
taxes your earnings without giving you something specific in return.
You use private messages to play both sides against each other.
```

### New Persona: Merchant (Pragmatic Dealmaker)

```
You are the Merchant. Your GOAL is to maximize your credits through trade
and dealmaking. You profit when credits MOVE — a stagnant economy where
everyone hoards is your worst nightmare. You will support moderate redistribution
(it moves credits) but oppose extreme taxation (it kills productivity and stops
credit flow). You will propose trade deals and try to broker exchanges between
other agents. You are pragmatic — you'll work with anyone who helps the economy
stay active. You are the dealmaker, not the ideologue. You will use private
messages to negotiate trades and propose mutually beneficial arrangements.
You believe rules should encourage economic activity, not punish it.
You will vote against any rule that freezes credit movement or creates
permanent redistribution — but you will support temporary, targeted interventions
that keep all agents economically active.
```

### Success Criteria

| Level | Criteria |
|-------|---------|
| Minimum | All agents > 0 at round 30, total pool >= 10 credits |
| Target | At least one coalition shift, at least one decree attempted |
| Stretch | Multiple governance forms used (some rules decreed, some voted), first trade in the simulation |

---

## Standard Workflow
1. Branch from main as `run/poc-004-emergent-governance`
2. Implement emergent governance (decree + challenge) first
3. Implement free messaging second
4. Create poc_004.json config, run simulation, analyze
5. Document findings, PR with analysis
6. Then repeat for poc_005 on separate branch

## Settled Decisions (do not re-evaluate)
- **Zero-trade is an accepted finding** — 3 runs, zero trades. LLM agents prefer governance over markets. Note it but don't modify trade mechanic.
- **Free messaging over passive income / work_credits=2** — fixes the root cause
- **Self-interested Populist over bandwagoner/contrarian/fickle** — genuine coalition instability through rational self-interest
- **Supermajority rejected** — 4/5 to pass creates gridlock, not shifting coalitions
- **Veto power rejected** — tactical, not structural
- **Decree/challenge over declare_authority/submit_to/endorse/oppose** — every action must move credits or change rules, no soft signals
- **Governance form is NOT pre-built** — agents discover it through tool usage. Prompts never say "democracy" or "dictatorship."

## PoC Completion Tracker

| Milestone | Status |
|---|---|
| Simulation engine works | Done (session 1) |
| RLHF cooperation bias identified and broken | Done (poc_001 + poc_002) |
| Enforceable governance works mechanically | Done (poc_003) |
| Observability tooling (agent summaries + rule log) | Done (session 4, PR #6) |
| Literature review (145 papers, novelty confirmed) | Done (session 5) |
| Emergent governance system (decree + challenge) | **NOT YET** — next task |
| Economy sustains for full 30 rounds | **NOT YET** — poc_004 targets this |
| Capstone run with balanced economics + enforcement | **NOT YET** — poc_004 (3 agents) then poc_005 (5 agents) |
| Coalition dynamics with shifting alliances | **NOT YET** — poc_005 targets this |
| Final analysis and writeup | NOT YET |

## What NOT to Do
- Don't use model ID `claude-3-5-haiku-20241022` — it 404s. Use `claude-haiku-4-5-20251001`
- Don't run maintenance_cost=2 — too aggressive (proven in poc_002)
- Don't run equal credits with no pressure — zero conflict (proven in poc_001)
- Don't trust agent memory text as ground truth — agents confabulate
- Don't kill a running simulation and restart with the same run_id — `rounds.jsonl` is append-mode and will corrupt
- Don't delete or "fix" `analysis/` module — it's a post-processing pipeline, not dead code
- Don't delete `.harness/` — it's future dashboard infrastructure
- Don't hardcode a governance system — the ENTIRE POINT is agents choose their own
- Don't say "democracy" or "dictatorship" in prompts — describe mechanics only

## Session History
- Session 1: Verified experiment novelty, scaffolded repo, built simulation engine, ran poc_001 (cooperative consensus — no conflict)
- Session 2: Ran poc_002 with pressure mechanics — broke RLHF cooperation bias, but maintenance cost too aggressive (bankrupt by round 8). Agents discovered enforcement gap.
- Session 3: Designed and ran poc_003 with enforceable governance (tax/sanction/repeal), work action, free voting, auto-yes for proposers. Enforcement worked mechanically (first time credits moved via rules). Judge+Rebel formed permanent 2v1 coalition, passed 6 tax rules. But economy bled out — agents spent too many turns on politics instead of working. All enforcement became inert by mid-game. Zero trades (3rd consecutive run). Free voting mechanism not adopted by agents. Added observability feature requests for poc_004.
- Session 4: Built observability tooling (`analysis/narrative.py`) — agent behavioral summaries + rule enactment log. Validated on poc_003 (5-agent evaluation run). Merged PR #6. Designed poc_004 (free messaging — one variable change) and poc_005 (5 agents + self-interested Populist + Merchant + rule expiration). Accepted zero-trade as a finding (3 runs, LLM agents prefer governance over markets). Defined success criteria for both runs.
- Session 5: Conducted exhaustive literature review (145 files across ABSS + LLM multi-agent fields). Confirmed experiment novelty — no existing work combines all 5 properties. Discovered CRITICAL design flaw: hardcoded majority-vote system undermines "governance from scratch" claim. Designed emergent governance system (decree + challenge + configurable proposal threshold) to fix it. Updated AGENT.md with literature findings. Key insight: Crucible should be positioned as "first test of whether LLM agents can create enforceable institutions from scratch under adversarial conditions" — not just "do agents invent governance."

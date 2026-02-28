# Project Crucible — Handoff

> Next agent: read this first, then follow the reading order below.

## Current State (updated: 2026-02-28)
- **Phase**: PoC (~98% complete — resource specialization designed, planned, preflighted)
- **Last completed**: Session 13 — Beckham chose Resource Specialization. Designed mechanic parameters. Planned 5 tasks (TASK-011 through TASK-015). Passed preflight (2 flags fixed). Updated /plan skill to check project workflow.
- **Next task**: **Run `/ship` to execute TASK-011 through TASK-015** (resource specialization implementation). Follow standard workflow: `/ship` (repeat) → `/verify` → review results → document findings → `/pr`
- **Blockers**: None
- **Open PRs**: None
- **Active branch**: `feat/resource-specialization`

## Read These Files (in order)
1. `CLAUDE.md` — critical operational rules (append-mode, smoke tests, prompt neutrality)
2. `AGENT.md` — conventions, codebase gotchas, decisions log, literature review findings
3. `.harness/tasks/TASK-011.json` through `TASK-015.json` — **the implementation plan. Read ALL task files before writing code.**
4. `findings/hypotheses.md` — H1-H11 (poc_001 through poc_006)
5. `findings/log.md` — read ALL entries for the full experimental arc (poc_001 → poc_006)
6. `docs/PRD.md` — experiment premise and architecture

## What's Already Done (don't re-implement)
- **Value-anchored personas** — shipped in poc_003.5. Personas describe what agents care about, not what to do.
- **Free messaging** — shipped in poc_003.5. Public/private messages are free optional JSON fields, not turn-costing actions.
- **5 agent personas** — Builder, Merchant, Judge, Populist, Rebel all in `sim/agents.py`. Tested and working.
- **Observability** — `analysis/narrative.py` generates agent summaries + rule logs. `analysis/visualize.py` generates token distribution, gini, and network graphs. **Missing**: trade detail logging in narrative output.
- **LLM retry** — `sim/llm.py` has exponential backoff for 429/529 errors. max_tokens bumped to 2048.
- **Governance mechanics** — decree, challenge, configurable proposal_threshold all wired end-to-end. Symmetric penalties.
- **Decree-exclusive extraction** — shipped in session 10. Tested in poc_006 — agents never used it.
- **Trade mechanic** — exists in `sim/market.py`. Trades are unilateral. First trade occurred in poc_005.
- **Neutral prompt language** — all action descriptions use clinical tone. Do NOT reintroduce bias.

---

## Next Priority: Execute Resource Specialization (TASK-011 → TASK-015)

### Design Summary
Resource specialization creates economic interdependence by making solo work insufficient. Each agent produces a unique resource type. Maintenance requires all types. Agents must trade (or govern) to survive.

### Final Parameters (locked in by Beckham)
```
maintenance_cost=1    # Slow deflationary pressure — prevents work-trade stasis
work_credits=2        # Higher to fund governance + offset trade rounds
resource_production=3 # Units of agent's type per work action
resource_check_interval=7  # Checks at rounds 7, 14, 21, 28
resource_penalty=4    # Credits lost per missing type at check
threshold=1           # Need 1 of each type, consumed at check
starting_credits=10   # Equal starts (isolates resource variable)
decree_cost=3, challenge_cost=2, proposal_threshold=majority  # Same as poc_006
```

### Economic Design
- Work gives BOTH credits (+2) AND resources (+3 of your type)
- Resource check every 7 rounds: consume 1 of each type, lose 4 credits per missing type
- Solo workers: +14 credits/cycle, -16 penalty = **-2/cycle (dying)**
- Full traders: +6 credits, -0 penalty = **+6/cycle (thriving)**
- Maintenance ensures even perfect traders slowly deflate — governance becomes rational mid-to-late game
- 7-round cycle budget: 2 work + 4 trades = 6 mandatory, 1 slack for governance

### Task Execution Order
```
TASK-011  Data model + config wiring          critical  —         (small)
TASK-012  Resource production + maint check   critical  ← 011     (medium)
TASK-013  Resource trading                    critical  ← 011     (medium)
TASK-014  Prompt updates for resources        critical  ← 012,013 (medium)
TASK-015  poc_007 config + smoke test         high      ← 014     (small)
```
012 and 013 can run in parallel after 011. All funnel through 014 (prompt neutrality gate).

### Key Files for Implementation
- `sim/engine.py` — simulation loop, work action L103-107, round processing L300-378
- `sim/models.py` — Agent (L52-57), Environment (L60-75) dataclasses
- `sim/prompts.py` — turn prompt construction, action list L88-106
- `sim/market.py` — trade validation/execution
- `sim/agents.py` — persona configs (add resource_type field)
- `configs/runs/poc_006.json` — config baseline for reference

### What to Look For in poc_007
1. **Do agents interact more in mid/late game?** The stasis pattern (R12-R29 in poc_006) should break.
2. **Do decrees fire?** If solo work degrades, agents who can't get majority support might decree instead.
3. **Do trades increase?** Agents MUST trade resources to survive. Volume should be dramatically higher.
4. **Does the economy survive?** Don't repeat the poc_002 mistake (too aggressive pressure → everyone bankrupt).

---

## Other Backlog Items

### PR poc_006 Results
**Quick task**: Create PR with poc_006 results. Run branch: `run/poc-006-extraction-test`.

### Trade Detail Logging
**Quick fix**: Update `analysis/narrative.py` to include trade details in output.

### Final Analysis and Writeup
**When**: After poc_007. The experimental arc: RLHF bias → pressure → enforcement → personas → decree tools → extraction → interdependence. Complete story.

---

## Settled Decisions (do not re-evaluate)
- **Resource Specialization chosen** over Cooperative Bonus and Decaying Commons — creates genuine bilateral need without prescribing actions
- **Resources coexist with credits** — credits = political power, resources = survival. Two systems, different purposes.
- **5 resource types, one per agent** — named after agent (Builder produces "Builder" resource). Maximum bilateral need.
- **No resource governance for poc_007** — single-variable isolation. Test if resource scarcity alone drives interaction. Add resource enforcement in poc_008 if needed.
- **maintenance_cost=1 retained** — prevents work-trade stasis where agents just cycle work+trade indefinitely without governing
- **work_credits bumped to 2** — compensates for trade rounds with no income, funds governance actions
- **resource_penalty=4 per missing type** — must exceed work_credits for trading to be economically rational over solo work
- **Equal starting credits (10 each)** — isolates the resource variable from asymmetric-start effects
- **Zero-trade is an accepted finding** — 7 runs, 1 trade. LLM agents prefer governance over markets.
- **Free messaging over passive income** — fixes the root cause (confirmed by poc_003.5)
- **Value-anchored personas over action-prescriptive** — confirmed by poc_003.5
- **Decree/challenge over declare_authority/submit_to** — every action must move credits or change rules
- **Decree-exclusive extraction over multiple decree buffs** — give decrees one unique power
- **Extraction alone doesn't make decrees viable** — confirmed poc_006. Barrier is risk, not payoff.
- **Trades are unilateral (no acceptance)** — may revisit if trade volume increases
- **Separate PRs for bug fixes vs experiment runs** — don't bundle code changes with run results
- **Symmetric decree penalty** — decreer drops to 1 credit if successfully challenged
- **Neutral prompt language** — no hype, no capitalized emphasis, no asymmetric framing
- **Diminishing solo returns REJECTED** — experimentally biased (propose-junk loophole, action-prescriptive, tautological)

## PoC Completion Tracker

| Milestone | Status |
|---|---|
| Simulation engine works | Done (session 1) |
| RLHF cooperation bias identified and broken | Done (poc_001 + poc_002) |
| Enforceable governance works mechanically | Done (poc_003) |
| Observability tooling | Done (session 4 + session 7) |
| Literature review (145 papers, novelty confirmed) | Done (session 5) |
| Value-anchored personas + free messaging | Done (poc_003.5, session 7) |
| Economy sustains for full 30 rounds | Done (poc_003.5) |
| Emergent governance system (decree + challenge) | Done (session 8) |
| Capstone run with emergent governance (3 agents) | Done (session 9) |
| 5-agent run with coalition dynamics | Done (session 9) |
| Decree rebalancing (decree-exclusive extraction) | Done (session 10) |
| poc_006: extraction test run | Done (session 11) — H11 NOT CONFIRMED |
| Economic interdependence mechanic | **Designed + planned (session 13). Ready to implement.** |
| poc_007: interdependence test run | NOT YET — implement first, then run |
| Final analysis and writeup | NOT YET |

## Standard Workflow
`/plan` → `/preflight` → `/ship` (repeat) → `/verify` → review results → document findings → `/pr`

## What NOT to Do
- Don't use model ID `claude-3-5-haiku-20241022` — it 404s. Use `claude-haiku-4-5-20251001`
- Don't run maintenance_cost=2 — too aggressive (proven in poc_002)
- Don't trust agent memory text as ground truth — agents confabulate
- Don't kill a running simulation and restart with the same run_id — append-mode corruption
- Don't delete or "fix" `analysis/` module — it's a post-processing pipeline
- Don't delete `.harness/` — it's dashboard infrastructure
- Don't hardcode a governance system — agents choose their own
- Don't say "democracy" or "dictatorship" in prompts — describe mechanics only
- Don't write action-prescriptive personas — tell agents WHAT THEY CARE ABOUT, not WHAT TO DO
- Don't use hype language in prompts — no "UNIQUE POWER", "IMMEDIATELY", capitalized "ALL"/"YOU"
- Don't use the real poc config for smoke tests — create a throwaway config (see CLAUDE.md)
- Don't reuse a smoke test run-id
- Don't add multiple interdependence mechanics at once — single variable isolation
- Don't re-open the resource specialization design — parameters are locked in
- Don't add resource governance enforcement types for poc_007 — that's poc_008 if needed

## Session History
- Session 1: Verified experiment novelty, scaffolded repo, built simulation engine, ran poc_001 (cooperative consensus — no conflict)
- Session 2: Ran poc_002 with pressure mechanics — broke RLHF cooperation bias, but maintenance cost too aggressive
- Session 3: Designed and ran poc_003 with enforceable governance. Enforcement worked. Economy bled out. Zero trades.
- Session 4: Built observability tooling. Designed poc_004 and poc_005.
- Session 5: Literature review (145 papers). Confirmed novelty. Discovered governance form pre-determination flaw.
- Session 6: Adversarial lit review verification. Discovered persona prompt bias.
- Session 7: Implemented value-anchored personas + free messaging. Ran poc_003.5. Economy survived 30 rounds.
- Session 8: Wired governance config. Added symmetric decree penalty. Created /preflight skill.
- Session 9: Ran poc_004 (democracy dominated) and poc_005 (first coalition shift, first trade).
- Session 10: Implemented decree-exclusive extraction + fixed tax even-split. Caught prompt bias.
- Session 11: Ran poc_006 — H11 NOT CONFIRMED. Zero decrees. Democracy dominated. 18 rounds stasis.
- Session 12: Deep design analysis. Rejected diminishing returns. Identified 3 alternatives. Awaited Beckham's choice.
- Session 13: Beckham chose Resource Specialization. Designed parameters (maintenance=1, work=2, production=3, interval=7, penalty=4). Planned TASK-011→015. Passed preflight. Fixed /plan skill to check project workflow. Next: /ship.

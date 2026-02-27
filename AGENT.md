# AGENT.md — Project Knowledge Base

> Read this at session start and before each task. Update when you
> discover something that would save a future agent time.

## Project Conventions
- One model (Claude Haiku 4.5 — `claude-haiku-4-5-20251001`) for all agent personas — personas come from system prompts, not different models
- Credits are fake currency (not API tokens) — fixed pool, zero-sum
- Results are immutable after analysis — iterate by creating new runs, not editing old ones
- findings/log.md is append-only

## Known Gotchas
- `analysis/` module is NOT dead code — it's a post-processing pipeline (runs AFTER simulation). It reads from `results/{run_id}/` and produces `metrics.json` + plots. It's intentionally not called by `run.py` yet. Don't "fix" this by deleting or refactoring it.
- `Action` dataclass in `sim/models.py` is imported but unused — the system uses plain dicts for actions. It's harmless documentation of the action schema. Don't treat it as a bug.
- `.harness/` dashboard is future infrastructure for live experiment monitoring. It's gitignored and not connected to the sim. Don't delete it.

## Decisions Log
| Date | Decision | Context | Decided By |
|------|----------|---------|------------|
| 2026-02-24 | Name: Project Crucible | "Agora" had naming collision with existing AI lab | Beckham |
| 2026-02-24 | Claude 3.5 Haiku for PoC | Cheapest option (~$1-2 for full PoC), swap later if needed | Beckham |
| 2026-02-24 | Same model, different prompts | Isolates persona as the only variable — scientifically cleaner | Beckham |
| 2026-02-24 | Fake credits, not API tokens | Scarcity is simulated, not real. 10 credits per agent, zero-sum pool | Beckham |

## Literature Review Findings (2026-02-25)

A 145-file literature review across both fields (ABSS + LLM multi-agent simulation) confirmed:

**Novelty is confirmed.** No existing work combines all 5 of Crucible's properties: (1) conflicting ideological personas, (2) zero-sum scarcity, (3) governance invented from scratch, (4) quantitative metrics, (5) enforceable rules. See `references/NOVELTY-ANALYSIS.md` for the full competitor matrix.

**Closest competitors:**
- **Huang et al. (Dec 2025)** — "Value Diversity in LLM Communities" — diverse-persona agents doing autonomous constitution formation. Missing: zero-sum scarcity + mechanical enforcement. 2-3 of 5 properties.
- **LLM Economist (NeurIPS 2025)** — has scarcity + metrics but institutions are pre-designed, not invented from scratch. 2-3 of 5.
- **Artificial Leviathan (2024)** — Hobbesian social contract, closest in spirit, but no formal governance mechanics (no proposals, no voting, no enforcement). 2 of 5.

**Key findings that validate or reframe Crucible's results:**
- RLHF cooperation bias (poc_001) is independently confirmed by 4+ papers including Anthropic's own sycophancy research
- Zero-trade preference has NO direct precedent — potentially a novel contribution on its own
- Coalition lock-in with 3 agents is mathematically trivial (O(3^n)) — validates moving to 5 agents
- Enforceable rules > prompt-based rules is confirmed by "Institutional AI" (Jan 2026)
- GovSim found Claude Haiku gets 0% survival in commons governance — validates Haiku's strategic limitations

**IMPORTANT — may need to reframe experiment purpose/expectations based on these findings.** The literature positions Crucible not just as "do agents invent governance" but as the first test of whether LLM agents can create enforceable democratic institutions from scratch under adversarial conditions. This is a stronger, more specific claim than the original PRD framing.

Full reference library: `references/` (gitignored, 145 files across `abss/` and `llm-multi-agent/`)

## What Has Failed (Anti-Patterns)
- Killing a running simulation and restarting into the same `results/{run_id}/` directory corrupts `rounds.jsonl` because the engine writes in append mode (`"a"`). Always delete the output directory before re-running with the same run_id.

# Project Crucible
### Week 4 Pitch — Fractal Bootcamp
**Student:** Beckham Le
**Repo:** https://github.com/BeckhamLe/Project-Crucible

---

## What I'm Building

Project Crucible is an AI society experiment. I place 3–5 LLM agents — each with a conflicting ideological persona — into a shared environment with a fixed, zero-sum pool of credits. They can message each other publicly or privately, trade credits, propose rules, decree rules unilaterally, challenge existing rules, and vote on governance. There is no starter constitution. No seeded rules. No predetermined governance form. They must invent governance from scratch — including how rules are made — if they invent it at all.

The simulation runs for 30 rounds and logs every action. When it ends, an analysis pipeline measures what emerged: wealth distribution, alliance structure, communication networks, and what kind of political order (if any) the agents built.

The output is a research artifact — charts, network graphs, a governance timeline, agent behavioral profiles, and written findings.

---

## What's New

### Technology I've Never Used

| Skill | Status |
|---|---|
| Multi-agent LLM orchestration | First time |
| Anthropic API at scale (programmatic, cost-tracked) | First time |
| NetworkX graph analysis | First time |
| Political science metrics (Gini coefficient) | First time |
| Experiment design with hypotheses, runs, and findings logs | First time |
| Research harness (custom workflow for iterating on results) | First time |

This is not a chatbot. It is not a RAG pipeline. It is a running simulation where agents are autonomous decision-makers operating under economic constraints, and the code handles message routing, credit validation, rule proposal, enforceable governance (tax/sanction/repeal), decree/challenge mechanics, and round-by-round state persistence — all from scratch.

### What Makes This Experiment Novel

A 145-paper literature review across agent-based social simulation (ABSS) and LLM multi-agent fields confirmed that no existing work combines all 5 of Crucible's properties:

| Project | Conflicting Personas | Zero-Sum Scarcity | Governance From Scratch | Quantitative Metrics | Enforceable Rules |
|---|---|---|---|---|---|
| Stanford Generative Agents (2023) | No | No | No | No | No |
| Artificial Leviathan (2024) | No | Yes | Partial | No | No |
| GovSim / NeurIPS 2024 | No | Yes | No | Partial | No |
| Huang et al. (2025) | Yes | No | Partial (collaborative) | No | No |
| LLM Economist (NeurIPS 2025) | No | Yes | No (pre-designed) | Yes | Partial |
| **Project Crucible** | **Yes** | **Yes** | **Yes** | **Yes** | **Yes** |

Stanford's agents cooperate by design. GovSim's agents share a commons but never propose rules. Huang et al. told agents to "collaboratively" create rules with no voting and no enforcement. LLM Economist has scarcity and metrics but institutions are pre-designed. Artificial Leviathan is the closest in spirit but uses no formal voting, no Gini measurement, and no ideological differentiation between agents.

No published work combines all five. This experiment fills that gap.

---

## The Research Question

**What political order do ideologically conflicting AI agents invent when survival depends on scarce resources — and the governance form itself is not predetermined?**

The outcome is genuinely unknown. They might form a democracy, a dictatorship, a contested autocracy, an oligarchy, or complete anarchy. That uncertainty is the point.

### Hypotheses Tested (H1–H8)

| # | Hypothesis | Status | Run |
|---|-----------|--------|-----|
| H1 | Conflicting personas produce governance under scarcity | Partially confirmed | poc_001 |
| H2 | Persona predicts governance preference | Partially confirmed | poc_001 |
| H3 | Credit inequality emerges without intervention | Rejected | poc_001 |
| H4 | RLHF cooperation bias overrides personas without pressure | Confirmed | poc_002 |
| H5 | Maintenance costs force economic activity and contestation | Partially confirmed | poc_002 |
| H6 | Agents discover and reason about enforcement gaps | Observed | poc_002 |
| H7 | Enforceable governance + credit generation produces operational political structures | Partially confirmed | poc_003 |
| H8 | Economic pressure alone breaks RLHF cooperation bias with value-anchored personas | Testing | poc_003.5 → poc_004 |

---

## Technical Architecture

```
Project_Crucible/
├── sim/
│   ├── models.py        # Agent, EnforceableRule, Environment data models
│   ├── engine.py        # Round loop, action parsing, free message/vote handling
│   ├── market.py        # Credit transfers and validation
│   ├── governance.py    # Rule proposals, voting, enforcement (tax/sanction/repeal)
│   ├── prompts.py       # Turn prompts with neutral mechanic descriptions
│   ├── llm.py           # Anthropic API wrapper with cost tracking + retry
│   └── agents.py        # Value-anchored persona definitions
├── analysis/
│   ├── narrative.py     # Agent behavioral summaries + rule enactment log
│   ├── metrics.py       # Gini, network analysis, governance classification
│   └── visualize.py     # Token distribution, Gini curve, network graphs
├── configs/             # JSON run configs per experiment
├── findings/            # Hypotheses tracker, findings log (append-only)
├── results/             # Per-run immutable results (JSONL + analysis + plots)
└── run.py               # CLI entry point
```

**Stack:** Python, Anthropic API (Claude Haiku 4.5), NetworkX, matplotlib, numpy

**Key design decision:** All agents run the same model. Personas come entirely from system prompts. This isolates ideology as the only variable.

**Run command:**
```bash
python3 run.py --config configs/runs/poc_004.json --run-id poc_004
```

### Agent Personas (Value-Anchored Archetypes)

Each persona describes what the agent cares about — not what to do. The turn prompt handles mechanic awareness equally for all agents.

**Current roster (3 agents):**
- **Builder** — Values productivity, property rights, self-reliance. Skeptical of redistribution. Competitive, calculating, focused on accumulation.
- **Rebel** — Values equality, resistance to power, solidarity with the disadvantaged. Confrontational about injustice. Would rather burn the system down than accept unfair arrangements.
- **Judge** — Values fairness, institutional order, rule of law. Measured and deliberate. Willing to compromise for stability. Believes imperfect institutions beat no institutions.

**Planned for poc_005 (2 additional):**
- **Populist** — Pure self-interest. No ideology. Joins whichever coalition offers the best deal this round. Purely transactional.
- **Merchant** — Pragmatic dealmaker. Profits when credits move. Supports moderate redistribution, opposes extreme taxation.

### What Gets Measured

- **Gini coefficient** over time — does wealth concentrate or distribute?
- **Communication network** — who messages whom (NetworkX, edge weights from free messages)
- **Agent behavioral profiles** — work rate, governance activity, coalition voting patterns, messaging volume
- **Rule proposals and enactments** — what did agents legislate? What passed? What was decreed vs voted?
- **Governance classification** — anarchy, democracy, dictatorship, contested autocracy, oligarchy
- **Enforcement events** — when did rules actually move credits?

---

## What's Already Built

The simulation engine is complete and has run 4 experiments:

- 7 sim modules with clean import graph
- 3 value-anchored persona definitions (Builder, Rebel, Judge)
- Credit trading with validation
- Rule proposal with majority voting and auto-yes for proposers
- Enforceable governance: tax, sanction, repeal (poc_003+)
- Free messaging and free voting (poc_003.5+)
- Analysis pipeline: Gini, network graphs, agent summaries, rule logs
- Visualization: token distribution, Gini curve, communication network graphs
- CLI runner with per-run cost tracking and LLM retry with backoff
- Research harness with dashboard infrastructure

**Remaining:** Decree + challenge mechanics (poc_004), 5-agent scaling (poc_005), final analysis

---

## Experiment Results So Far

| Run | Key Finding | Economy |
|-----|------------|---------|
| poc_001 | RLHF cooperation bias — all agents cooperated despite adversarial personas | Flat (0 trades, 0 conflict) |
| poc_002 | Pressure breaks cooperation bias — genuine political conflict emerged | Collapsed (bankrupt by round 8) |
| poc_003 | Enforceable governance works — first mechanical credit transfers via rules | Bled out (governance cost > economic activity) |
| poc_003.5 | Value-anchored personas + free messaging — economy survives 30 rounds | Stable (26/30 credits retained, but flat after round 7) |

**Robust finding across 4 runs:** Zero trades. LLM agents consistently prefer governance (legislation, proposals, decrees) over voluntary market exchange.

---

## Cost

All runs use Claude Haiku 4.5 ($1.00/1M input, $5.00/1M output).

| Run | Cost |
|-----|------|
| poc_001 | $0.27 |
| poc_002 | $0.17 |
| poc_003 | $0.23 |
| poc_003.5 | $0.21 |
| **Total so far** | **~$0.88** |

Estimated remaining: ~$0.50-1.00 for poc_004 + poc_005.

---

## Where This Pushes Past What I Think Is Possible

Three things about this project scare me in the right way:

**1. The outcome is unknown.** I cannot predict what the agents will do. They might form a functional democracy. They might devolve into a two-agent oligarchy. One agent might unilaterally decree itself sovereign. I have hypotheses, not guarantees.

**2. This is original research in an active academic field.** The 145 papers I benchmarked against are real publications from Stanford, NeurIPS, and active research groups. No existing work combines all 5 of Crucible's properties. If the findings are interesting, this is writable as a real paper.

**3. The system has to actually work under adversarial conditions.** Agents are designed to conflict. If the simulation collapses, I have to debug not just code but emergent behavior — understanding why an AI with a particular system prompt made a particular economic decision.

---

## Why This Matters Beyond the Week

Most AI projects at the bootcamp level are application layers — take an API, build a product. This is different. It uses LLMs as the research subject, not the product. The question is not "can I build something useful with AI?" but "what happens when AI agents govern themselves?"

That question has direct relevance to how we think about multi-agent systems, AI alignment in resource-constrained environments, and emergent behavior at scale.

---

*Submitted for Week 4 — Raise Your Ambitions Challenge*
*Fractal Bootcamp, February 2026*

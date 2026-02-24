# Project Crucible
### Week 4 Pitch — Fractal Bootcamp
**Student:** Beckham Le
**Repo:** https://github.com/BeckhamLe/Project-Crucible

---

## What I'm Building

Project Crucible is an AI society experiment. I place 3–8 LLM agents — each with a conflicting ideological persona — into a shared environment with a fixed, zero-sum pool of credits. They can message each other publicly or privately, trade credits, propose rules, and vote on governance. There is no starter constitution. No seeded rules. They must invent governance from scratch, if they invent it at all.

The simulation runs for N rounds and logs every action. When it ends, an analysis pipeline measures what emerged: wealth distribution, alliance structure, and what kind of political order (if any) the agents built.

The output is a research artifact — charts, network graphs, a governance timeline, and written findings.

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

This is not a chatbot. It is not a RAG pipeline. It is a running simulation where agents are autonomous decision-makers operating under economic constraints, and the code has to handle message routing, credit validation, rule proposal, majority voting, and round-by-round state persistence — all from scratch.

### What Makes This Experiment Novel

I spent time verifying that this exact combination of properties does not exist in published research. Here is what the closest work does and where it falls short:

| Project | Conflicting Personas | Zero-Sum Scarcity | Governance From Scratch | Quantitative Metrics |
|---|---|---|---|---|
| Stanford Generative Agents (2023) | No | No | No | No |
| Artificial Leviathan (2024) | No | Yes | Partial | No |
| GovSim / NeurIPS 2024 | No | Yes | No | Partial |
| Project Sid (2024) | No | No | No (seeded) | No |
| **Project Crucible** | **Yes** | **Yes** | **Yes** | **Yes** |

Stanford's agents cooperate by design. GovSim's agents share a commons but never propose rules. Project Sid gives agents a starter constitution — governance is inherited, not invented. Artificial Leviathan is the closest predecessor, but uses no formal voting, no Gini measurement, and no ideological differentiation between agents.

No published work combines all four. This experiment fills that gap.

---

## The Research Question

**What political order do ideologically conflicting AI agents invent when survival depends on scarce resources?**

The outcome is genuinely unknown. They might form a democracy, a hierarchy, a protection racket, or complete anarchy. That uncertainty is the point.

### Hypotheses Being Tested

- **H1:** Conflicting personas under scarcity produce governance — at least one rule is proposed within the first half of the simulation.
- **H2:** Persona predicts governance preference — Builder agents push efficiency rules, Judge agents push fairness rules, Rebel agents resist all rules.
- **H3:** Credit inequality emerges without intervention — Gini coefficient exceeds 0.3 by the end of the run.

---

## Technical Architecture

```
Project_Crucible/
├── sim/
│   ├── models.py        # Agent, Message, Rule, Vote data models
│   ├── engine.py        # Round loop, state machine
│   ├── market.py        # Credit transfers and validation
│   ├── governance.py    # Rule proposals and majority voting
│   ├── prompts.py       # Persona system prompts
│   ├── llm.py           # Anthropic API wrapper with cost tracking
│   └── agents.py        # Agent decision orchestration
├── analysis/            # Gini, NetworkX graphs, visualization
├── configs/             # JSON run configs and experiment templates
├── findings/            # Hypotheses log, findings per run
├── results/             # JSONL round-by-round immutable logs
└── run.py               # CLI entry point
```

**Stack:** Python, Anthropic API (Claude 3.5 Haiku), NetworkX, matplotlib, numpy

**Key design decision:** All agents run the same model. Personas come entirely from system prompts. This isolates ideology as the only variable — any behavioral differences between agents are caused by their instructions, not model variation.

**Run command:**
```bash
python run.py --config configs/templates/baseline.json
```

### Agent Personas (Ideological Archetypes)

Each persona has a defined belief system — not just preferences, but a foundational view of what is right:

- **Builder** — Progress and productivity above all. Hoards resources to build. Distrusts redistribution.
- **Rebel** — Existing power structures are corrupt. Disrupts, tests rules, resists authority.
- **Judge** — Rules must be fair and universally applied. Enforces norms aggressively.
- **Philosopher** — Questions the purpose of the system itself. May refuse to play by its terms.
- **Hustler** — Pure self-interest. Maximizes credits by any means available.
- **Caretaker** — Collective survival first. Advocates redistribution even at personal cost.
- **Mystic** — Operates on internal logic that may not align with economic rationality.
- **Strategist** — Long-game thinker. Builds alliances, sacrifices short-term position for leverage.

### What Gets Measured

- **Gini coefficient** over time — does wealth concentrate or distribute?
- **Communication graph** — who messages whom privately (NetworkX, betweenness centrality, clustering)
- **Rule proposals and votes** — what did agents try to legislate? What passed?
- **Governance classification** — anarchy, failed state, welfare state, authoritarian, cooperative, other
- **Outcome reproducibility** — do different random seeds produce the same political order?

---

## What's Already Built

The simulation engine is complete and functional. As of submission:

- 7 sim modules with clean import graph (no circular dependencies)
- 3 persona definitions (Builder, Rebel, Judge) with full system prompts
- Token trading with validation and error handling
- Rule proposal and majority voting system
- Analysis pipeline: Gini coefficient, communication graphs, betweenness centrality, governance classification
- Visualization: token distribution over time, Gini curve, network graphs
- CLI runner with per-run cost tracking
- Research harness: experiment configs, findings log, hypotheses tracker

The infrastructure is built. The experiments are what's left.

---

## Cost & Run Strategy

All runs use Claude 3.5 Haiku ($1.00/1M input, $5.00/1M output).

| Phase | Agents | Rounds | Runs | Est. Cost |
|---|---|---|---|---|
| Proof of Concept | 3 | 30 | 1 | ~$1 |
| Full Experiment (batch 1) | 8 | 50 | 3 | ~$13 |
| Full Experiment (batch 2) | 8 | 50 | 2 | ~$9 |
| **Total** | | | **5 runs** | **~$23** |

**Why 50 rounds instead of 100:** LLM agents settle into behavioral patterns faster than humans. Research on multi-agent LLM simulations shows governance dynamics emerge within the first 25-35 rounds and rounds beyond 50 mostly repeat established patterns. Cutting rounds in half is essentially free analytically.

**Why staged runs (3 then 2):** Run the first 3, check results, fix any config issues before committing the last $9. Same 5 total runs, staged to avoid burning budget on a broken config.

**Why 5 runs:** With fewer than 3, you can't distinguish "this always happens" from "this happened by chance." 5 runs is the floor for claiming a behavioral pattern is robust across different conditions.

---

## Timeline

### Days 1–2: Proof of Concept
- 3 agents (Builder, Rebel, Judge), 30 rounds, 10 credits each
- Cost: ~$1 in API calls
- Deliverable: First run results — charts, governance timeline, initial findings against H1–H3

### Days 3–4: Full Experiment
- Scale to 8 agents (add Philosopher, Hustler, Caretaker, Mystic, Strategist)
- 50 rounds, 3 runs with different random seeds (batch 1)
- Analyze results, tune if needed, then run 2 more (batch 2)
- Compare governance outcomes across all 5 runs — stable or chaotic?
- Analyze network graphs for alliance structure and faction formation

### Day 5: Write-Up and Demo Prep
- Findings document: what happened, what was predicted, what was surprising
- Clean visualizations for all metrics
- Live demo: run the simulation in real time, walk through results

---

## Demo Plan

The demo shows:

1. **Live simulation run** — watch agents message, trade, and propose rules in real time
2. **Token distribution chart** — Gini coefficient over rounds
3. **Network graph** — who allied with whom, who was isolated
4. **Governance timeline** — what rules were proposed, what passed, what got vetoed
5. **Cross-run comparison** — do different seeds produce different political orders?

---

## Where This Pushes Past What I Think Is Possible

Three things about this project scare me in the right way:

**1. The outcome is unknown.** I cannot predict what the agents will do. They might form a functional democracy. They might devolve into a two-agent oligarchy. One agent might unilaterally declare itself sovereign. I have hypotheses, not guarantees. Running real experiments with uncertain results is a different skill than building apps with known outputs.

**2. This is original research in an active academic field.** The four papers I benchmarked against are real publications from Stanford, NeurIPS, and active research groups. If the findings are interesting, this is writable as a real paper. That has never been in scope for a bootcamp project.

**3. The system has to actually work under adversarial conditions.** Agents are designed to conflict. The Rebel is supposed to resist rules. The Hustler is supposed to exploit gaps. If the simulation collapses, I have to debug not just code but emergent behavior — which means understanding why an AI with a particular system prompt made a particular economic decision. That is a new kind of debugging.

---

## Why This Matters Beyond the Week

Most AI projects at the bootcamp level are application layers — take an API, build a product. This is different. It uses LLMs as the research subject, not the product. The question is not "can I build something useful with AI?" but "what happens when AI agents govern themselves?"

That question has direct relevance to how we think about multi-agent systems, AI alignment in resource-constrained environments, and emergent behavior at scale. It is a genuine contribution to an open research area, built in a week, with a working system and real results.

---

*Submitted for Week 4 — Raise Your Ambitions Challenge*
*Fractal Bootcamp, February 2026*

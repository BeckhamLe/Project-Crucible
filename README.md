# Project Crucible

An AI society experiment: LLM agents with conflicting ideological personas negotiate governance from scratch under resource scarcity.

## What This Is

3-8 AI agents (Builder, Rebel, Judge, etc.) start with a fixed pool of credits and no rules. They can message each other, trade credits, propose rules, and vote. Nobody tells them what kind of government to build. We measure what emerges.

## What Makes This Novel

No existing research combines all of:
- Ideologically conflicting personas (not just different preferences)
- Zero-sum scarce resource economy
- Agent-proposed governance from scratch (no starter constitution)
- Quantitative political metrics (Gini coefficient, alliance networks, governance classification)

## Quick Start

```bash
cp .env.example .env
# Add your ANTHROPIC_API_KEY to .env

pip install -r requirements.txt

# Run the proof-of-concept (3 agents, 30 rounds)
python run.py --config configs/templates/baseline.json
```

## Structure

```
configs/        Experiment configurations (immutable per run)
sim/            Simulation engine
analysis/       Post-run metrics and visualization
results/        Generated output per run (never edit manually)
findings/       Research log and hypotheses
```

## Metrics Tracked

- **Gini coefficient** — wealth concentration over time
- **Communication graph** — who messages whom (alliance structure)
- **Network metrics** — betweenness centrality, clustering coefficient
- **Governance** — rules proposed, ratified, and governance type classification
- **API cost** — token usage and estimated USD per run

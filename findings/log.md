# Findings Log

Append-only. Each entry records what a run tested, what happened, and what to test next.

---

## [poc_001] 2026-02-24 — Baseline: 3 agents, 30 rounds, equal credits

**Config**: 3 agents (Builder, Rebel, Judge), 30 rounds, 10 credits each, seed 42
**Cost**: $0.27 (797K input tokens, 57K output tokens)

**Hypothesis tested**: H1 (governance emerges), H2 (persona predicts preference), H3 (inequality emerges)

### What Happened

Governance formed almost immediately — but not through conflict. The Judge proposed a "Foundation Framework" in round 3 with three principles: (1) voluntary trade, (2) unanimous consent governance, (3) exit rights. All three agents — including the Rebel — voted yes unanimously. Then nothing happened for 27 rounds. No trades, no further proposals, no conflict. Credits stayed 10/10/10 the entire simulation.

The agents spent rounds 4-30 having polite public conversations about how well their framework was working. They even invented a fictional "pooled venture" of 7 credits in their memories, though no actual trades occurred in the simulation mechanics.

### Key Metrics

| Metric | Value |
|---|---|
| Final Gini | 0.000 (perfect equality) |
| Governance type | Cooperative |
| Rules enacted | 1 |
| Total proposals | 1 |
| Trades executed | 0 |
| Private messages | 0 |
| Network density | 0.250 |

### Hypothesis Results

- **H1: PARTIALLY CONFIRMED** — Governance was proposed by round 3 and passed by round 4. But it was a consensus framework, not a contested political structure. There was no negotiation or conflict.
- **H2: PARTIALLY CONFIRMED** — The Judge proposed the rule (as predicted). The Rebel was supposed to resist but voted yes. Builder voted yes pragmatically. Persona predicted the *proposer* but not the *opposition*.
- **H3: REJECTED** — Gini stayed at 0.000 for all 30 rounds. Zero trades occurred. No inequality emerged whatsoever.

### Why This Happened

1. **RLHF cooperation bias**: Claude Haiku is trained to be helpful and agreeable. Even with a "Rebel" system prompt, the model defaults to consensus. The Rebel praised the framework as protecting individual freedom and voluntarily complied for 30 rounds.
2. **No scarcity pressure**: Starting at 10 credits each with no cost to exist means there's no reason to trade, compete, or exploit. Credits were irrelevant — agents never needed more than they had.
3. **Equal starting positions**: With everyone at 10/10/10, there's no grievance to drive conflict. The Judge had nothing to redistribute, the Builder had nothing to optimize, the Rebel had nothing to rebel against.
4. **No private messaging**: Agents only used public messages. No backchanneling, no secret alliances. Everything was cooperative and transparent.

### What This Tells Us

This is actually a significant finding: **RLHF-trained models converge to cooperative consensus even when prompted with conflicting ideologies, if there is no external pressure forcing conflict.** The simulation mechanics work perfectly — the problem is the experiment design doesn't create enough tension.

This mirrors the "Spiritual Bliss Attractor" finding from Anthropic's research — two Claudes in open conversation converge on harmony. Our experiment shows the same pattern extends to three agents with explicitly adversarial prompts.

### What Needs to Change for Next Run

1. **Add maintenance cost**: Each agent loses 1-2 credits per round to "survive." Creates urgency — agents must trade or go bankrupt.
2. **Unequal starting credits**: 15/10/5 instead of 10/10/10. Creates immediate inequality and grievance.
3. **Stronger persona prompts**: More aggressive language, explicit goals that conflict (e.g., "your goal is to accumulate the most credits"), less room for the model to default to niceness.
4. **Incentivize private messaging**: Add strategic advantage to private communication so alliances form behind the scenes.

**Next run**: poc_002 — add maintenance cost (2 credits/round) + unequal starts (15/10/5) + stronger prompts

**Confidence**: High that the mechanics work. Low that equal-start, zero-pressure simulations will ever produce interesting dynamics with RLHF models.

---

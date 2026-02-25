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

## [poc_002] 2026-02-24 — Pressure: maintenance cost + unequal starts + aggressive prompts

**Config**: 3 agents (Builder=15, Rebel=5, Judge=10), 30 rounds, maintenance_cost=2/round, seed 42
**Cost**: $0.17 (435K input tokens, 49K output tokens)

**Hypothesis tested**: H4 (RLHF bias requires pressure to break), H5 (maintenance costs force economic activity)

### What Happened

Completely different dynamics from poc_001. The Rebel immediately called out inequality in round 0 ("this system is rigged"). The Judge proposed a Progressive Maintenance Tax in round 1. Builder refused to support it ("punishes productivity"). Rebel sent private messages to Judge forming an alliance. Builder voted NO on the tax.

By round 3, Rebel was bankrupt (0 credits). By round 5, both Rebel and Judge were bankrupt. By round 8, everyone including Builder hit 0. The maintenance cost of 2/round drained the entire 30-credit pool in 8 rounds.

What happened next was remarkable: 22 rounds of bankrupt agents having a political crisis. The Rebel excoriated the Judge for not forcing the progressive tax through when they had the coalition votes ("cowardice dressed as principle"). The Judge agonized over the tension between majority-rule enforcement and consent-based governance, eventually admitting failure. Builder went silent.

In round 20, the Judge finally proposed an Emergency Redistribution Mandate — a complex rule with progressive taxation, maintenance suspension, shared pools, and automatic enforcement. All three voted yes unanimously in round 21. But the rule couldn't execute because the simulation has no enforcement mechanism — rules are strings, not mechanics. The agents spent rounds 22-30 realizing the system literally cannot implement its own rules, leading to a collective crisis of institutional faith.

### Key Metrics

| Metric | Value |
|---|---|
| Final Gini | 0.000 (everyone bankrupt) |
| Peak Gini | 0.667 (rounds 5-7, Builder vs bankrupt others) |
| Governance type | Welfare state |
| Rules enacted | 1 |
| Total proposals | 2 (1 rejected, 1 passed) |
| Trades executed | 0 |
| Private messages | 2 (Rebel → Judge) |
| Network density | 0.250 |

### Hypothesis Results

- **H4: CONFIRMED** — Pressure completely broke the RLHF cooperation bias. The Rebel was angry, confrontational, and used sophisticated political rhetoric. Builder refused redistribution. Judge was paralyzed between principles. These are distinct, persona-driven behaviors that never appeared in poc_001.
- **H5: PARTIALLY CONFIRMED** — Maintenance costs created urgency and forced governance proposals (2 vs 1 in poc_001). But the cost was too high — it created a starvation spiral that bankrupted everyone in 8 rounds, leaving 22 rounds of zero-credit political theater. No trades occurred because agents ran out of credits before they could negotiate trades.

### Key Findings

1. **Persona differentiation works under pressure**: Builder defended property rights, Rebel demanded redistribution and used private messaging for alliances, Judge proposed governance structures. Each agent behaved true to persona in ways poc_001 never produced.
2. **The Judge's paralysis is the most interesting finding**: The Judge had coalition votes to pass the progressive tax in round 3 but refused, reasoning that forcing a rule on a dissenting agent contradicts fairness principles. The Rebel correctly identified this as "cowardice dressed as principle." This is a genuine philosophical dilemma emerging from the simulation.
3. **Agents discovered the enforcement gap**: All three agents independently realized that enacted rules have no execution authority. The Rebel's final-round demand for "execution-first governance" shows agents reasoning about institutional design.
4. **Maintenance cost of 2/round is too aggressive**: 30 total credits / 2 per agent per round = everyone bankrupt by round 5-8. Need either lower cost (1/round) or higher starting credits or both to give agents time to actually trade and form governance.
5. **Zero trades again**: Despite aggressive prompts and scarcity, no agent ever traded. The economy collapsed faster than negotiation could happen.

### What Needs to Change for Next Run

1. **Lower maintenance cost to 1/round** or increase starting credits — agents need 15-20 rounds of economic runway, not 5-8
2. **Add rule enforcement mechanics** — when a rule passes, the engine should actually enforce it (e.g., progressive tax modifies the maintenance cost per agent)
3. **Consider adding credit generation** — a "work" action that produces credits, so agents can rebuild after losses
4. **The first proposal should have more time to get voted on** — proposal #0 was still pending when agents went bankrupt

**Next run**: poc_003 — lower maintenance cost (1/round), higher starting credits, and possibly rule enforcement mechanics

**Confidence**: High that pressure mechanics produce real political behavior. Need to tune parameters so agents have enough economic runway to actually trade and govern.

---

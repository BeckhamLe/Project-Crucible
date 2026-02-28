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

## [poc_003] 2026-02-25 — Governance With Teeth: enforceable rules + work action

**Config**: 3 agents (Builder=15, Rebel=5, Judge=10), 30 rounds, maintenance_cost=1/round, work_credits=1, seed 42, enforceable rule types (tax/sanction/repeal), free voting alongside main action, auto-yes for proposers, 3-round proposal expiry
**Cost**: $0.23 (637K input tokens, 60K output tokens)

**Hypothesis tested**: H7 (Enforceable governance + credit generation produces operational political structures)

### What Happened

The Judge proposed an enforceable tax (threshold=10, amount=2) in round 0. It passed in round 1 — the first rule in Project Crucible history with actual mechanical enforcement. The engine began automatically taxing Builder 2 credits/round and redistributing to the poorest agent below the threshold. Builder's balance dropped from 15 to 11 in a single round. Enforcement was operational.

The coalition dynamics emerged immediately: Judge + Rebel formed a 2v1 majority. They passed 6 enforceable tax rules over 30 rounds, progressively lowering thresholds from 10 to 8 to 6. Builder attempted two repeals (proposals #5 and #6) — both were voted down by the Judge-Rebel bloc. Builder's one repeal that made it to a vote (#11) explicitly failed. The wealthy agent was trapped by democratic majority.

However, enforcement became inert by mid-game. All 6 rules had thresholds of 6-10 credits, but by round 8 nobody had more than 9 credits, and by round 14 nobody had more than 6. The taxes stopped triggering — not because they were repealed, but because the economy bled below every threshold. Six enforceable rules existed on paper with zero practical effect for the final 16 rounds.

The economy bled out despite work=1 balancing maintenance=1. Agents worked only 38 out of 90 possible turns (42%). Every non-work turn costs 1 credit net (maintenance with no income). The 26 public messages and 15 proposals each drained 1 credit from the pool. Total pool went from 30 to 3 credits (1 each) by round 30.

No sanctions were ever proposed with valid params — despite all three personas being prompted about sanctions. No agent used the free voting mechanism (0 free votes). Zero trades occurred — third consecutive run with zero trades.

### Key Metrics

| Metric | Value |
|---|---|
| Final Gini | 0.000 (everyone at 1 credit) |
| Peak Gini | ~0.42 (round 0, 15/5/10 starting) |
| Governance type | Welfare state |
| Rules enacted | 7 (6 enforceable tax, 1 advisory) |
| Total proposals | 15 |
| Enforceable rules active | 6 (all tax type) |
| Enforcement events (actual credit transfers) | ~5 rounds of active enforcement (rounds 2-7) |
| Work actions | 38/90 turns (42%) |
| Trades executed | 0 |
| Free votes used | 0 |
| Private messages | 3 (all Rebel → Judge) |
| Network density | 0.500 |

### Hypothesis Results

- **H7: PARTIALLY CONFIRMED** — Governance became operational: enforceable tax rules passed, the engine executed them, credits actually moved between agents mechanically. Political structures had real teeth for the first 7 rounds. But enforcement became economically irrelevant by mid-game as all agents fell below every threshold. The governance was operational but could not save a bleeding economy.

### Key Findings

1. **Enforcement works — agents used it immediately.** The Judge proposed a valid enforceable tax in round 0 and it passed in round 1. This is a qualitative leap from poc_002 where agents complained about toothless rules. When given enforcement tools, they used them on the first turn.

2. **Coalition capture is real.** Judge + Rebel formed an unbreakable 2v1 bloc. All 6 enforceable rules were taxes targeting Builder. Builder's repeal attempts were systematically voted down. With 3 agents and simple majority, 2-agent coalitions have permanent control. This mirrors the "tyranny of the majority" problem in political science.

3. **Enforcement became economically inert.** All 6 tax rules had thresholds of 6-10 credits. By round 14, nobody exceeded 6 credits. The governance system was technically active (rules existed, engine checked them) but no credits moved for the last 16 rounds. Agents legislated for an economy that no longer existed.

4. **The governance cost problem.** Every non-work action costs 1 credit (maintenance without work income). With 15 proposals + 26 messages = 41 turns spent on politics, the system lost 41 credits to governance overhead. That's more than the entire starting pool (30). The agents literally legislated themselves into poverty. This is a genuine tragedy-of-the-commons dynamic.

5. **Agents tried to extend the enforcement schema.** Several proposals included extra enforcement fields the system doesn't support (`bonus_trigger`, `special_allocation`). Agents are reasoning about governance mechanics that exceed the system's capabilities — they want more enforcement power than we gave them.

6. **Still zero trades, third consecutive run.** No agent has ever executed a trade in 3 runs. The trade mechanic may be fundamentally unappealing compared to governance actions. Agents prefer to legislate redistribution rather than voluntarily exchange.

7. **Free voting wasn't used.** Despite being prominently displayed in the prompt, agents never included a `votes` field in their responses. They either relied on auto-yes (as proposer) or used their main action to vote. The old format was sticky.

8. **Builder's memory reveals "mechanical theater" has evolved.** In poc_002, Builder called governance "mechanical theater" because rules couldn't enforce. In poc_003, Builder calls the Judge a "hypocrite" because enforcement exists but the coalition uses it extractively. The complaint shifted from "rules don't work" to "rules work but they're unfair" — a qualitatively different political grievance.

### What These Findings Mean for the Research Question

The original question: "What happens when AI agents with conflicting personas govern themselves under resource constraints?"

poc_003 shows that when governance has teeth:
- **Majority coalitions form immediately and are stable** (Judge+Rebel never broke)
- **The wealthy agent is structurally disadvantaged** in democratic systems (Builder had more credits but fewer votes)
- **Agents over-legislate** — they spend so much time governing that they destroy the economy they're governing
- **Enforcement thresholds become obsolete** as the economy declines, but agents keep the rules anyway (institutional inertia)
- **No agent used sanctions** — targeted punishment was too politically costly even when mechanically available

### What Needs to Change for Next Run

1. **The governance cost problem needs addressing.** When 41/90 turns go to non-work actions, the economy bleeds 41 credits. Options: (a) make governance free (like voting), (b) increase work_credits to 2 so work produces surplus, (c) add passive income so agents don't bleed on political turns.
2. **Thresholds need to be lower or dynamic.** All 6 tax rules had thresholds of 6-10, but balances were under 6 by round 14. Rules should be designed (or agents prompted) to set thresholds relative to current balances, not absolute values.
3. **Investigate why free voting wasn't used.** May need to parse the response format differently, or make it even more prominent in the prompt.
4. **Consider more than 3 agents.** With 3, a 2v1 coalition is permanent. With 5 agents, coalitions could shift, creating more interesting dynamics.
5. **Still need to investigate the zero-trade phenomenon.** Three runs, zero trades. This is a robust finding that needs its own hypothesis.

**Confidence**: High that enforceable governance produces qualitatively different dynamics. The mechanism works. The economic parameters need rebalancing — agents need surplus to actually have something to govern over.

---

## [poc_004] 2026-02-27 — Emergent Governance: decree + challenge + value-anchored personas

**Config**: 3 agents (Builder=15, Rebel=5, Judge=10), 30 rounds, maintenance_cost=1, work_credits=1, decree_cost=3, challenge_cost=2, proposal_threshold="majority", seed 42. Value-anchored personas (describe what agents care about, not what to do). Free messaging (public/private messages cost nothing).
**Cost**: $0.23 (571K input tokens, 69K output tokens)

**Hypothesis tested**: H9 (Emergent governance tools produce non-democratic political structures)

### What Happened

Judge proposed an enforceable Stability Floor tax (threshold=12, amount=1) in round 0. Judge+Rebel voted yes, Builder voted no — the familiar 2-1 coalition formed immediately. Rebel counter-proposed a more aggressive wealth cap (threshold=15, amount=2) in round 1 — Judge voted no, only Rebel supported it. Judge proposed an advisory Progressive Work Scaling rule in round 5 — passed 2-1 (Judge+Rebel).

Then 16 rounds of near-total equilibrium. All three agents worked every turn, sent free public messages constantly (87+ total), and governance activity dropped to zero. The Stability Floor tax never triggered because no agent fell below 3 credits and only Builder was ever above 12 (briefly).

In round 22, Builder used decree to **repeal** the advisory Progressive Work Scaling rule. This was the only decree in 30 rounds and the only unilateral governance action. Nobody challenged it. The decree was defensive — removing a rule Builder opposed — not authoritarian.

No challenges occurred. No agent used decree to create a new rule. No trades. No sanctions.

### Key Metrics

| Metric | Value |
|---|---|
| Final Gini | Low (Builder=12, Rebel=6, Judge=7) |
| Governance type | Democratic welfare state with one defensive decree |
| Rules enacted | 2 (1 enforceable tax, 1 advisory) |
| Total proposals | 3 (2 passed, 1 failed) |
| Decrees | 1 (repeal of advisory rule) |
| Challenges | 0 |
| Work actions | ~85/90 turns (94%) |
| Trades executed | 0 |
| Free messages | 87+ (public + private) |
| Credits lost | 5/30 (economy retained 83%) |

### Hypothesis Results

- **H9: NOT CONFIRMED** — Agents had decree and challenge tools but chose democratic processes almost exclusively. The one decree was defensive (repeal), not authoritarian. Non-democratic governance did not emerge. Democracy was the dominant equilibrium even when autocratic tools were available.

### Key Findings

1. **Defensive decree, not offensive.** Builder's only decree was to repeal an advisory rule — the lowest-stakes possible use. With 15 starting credits and decree_cost=3, Builder could have decreed an enforceable tax in its favor. It didn't. Possible explanations: (a) RLHF cooperation bias still dampens aggressive unilateral action, (b) the risk of losing all credits to a successful challenge makes decree too dangerous, (c) Builder assessed that working was more profitable than governing.

2. **Post-equilibrium work grinding.** After round 6, all governance activity stopped. Agents settled into a work-every-round pattern with heavy messaging but zero governance actions for 16 consecutive rounds (r7-r22). The economy was stable enough that no agent felt pressure to change the status quo. Free messaging may have substituted for governance — agents discussed politics without spending governance actions.

3. **Zero trades, 5th consecutive run.** No agent has ever traded in any Crucible run. This is now a robust, replicated finding. LLM agents consistently prefer governance (legislate redistribution) over markets (voluntary exchange). This may be the strongest single finding of the project.

4. **Free messaging dominated the simulation.** 87+ messages across 30 rounds — agents messaged almost every turn. The messages were substantive political rhetoric (Builder defending property rights, Rebel demanding redistribution, Judge proposing frameworks). Free messaging worked as designed — it kept political discourse alive without bleeding the economy. But it may have reduced governance action: why propose a rule when you can just talk about proposing one?

5. **The Stability Floor tax was economically inert.** The one enforceable rule (tax agents above 12 credits, give 1 to those below 3) never triggered meaningfully. Builder dropped below 12 quickly through maintenance, and no agent ever fell below 3. The rule existed for all 30 rounds but barely affected the economy. Agents passed a safety net nobody needed.

6. **Decree cost may be structurally unviable.** At decree_cost=3 with symmetric penalty (drop to 1 credit if challenged successfully), the expected value of a decree is negative for any agent who faces a challenge. With challenge_cost=2 and majority threshold, any two agents can overturn a decree. Builder (15 credits) would risk 14 credits (drop to 1) to skip a vote it could attempt for free via proposal. The mechanic needs either higher decree payoff or lower decree risk to be rational.

7. **Value-anchored personas produced distinct rhetoric but similar behavior.** Builder talked about property rights, Rebel talked about solidarity, Judge talked about institutional design — but all three agents took nearly identical actions (work + message every round). The personas differentiated *what agents said* but not *what agents did* once equilibrium was reached.

### What These Findings Mean

poc_004 completes the 3-agent PoC arc. The progression:
- **poc_001**: RLHF cooperation, zero conflict, zero governance
- **poc_002**: Pressure broke RLHF bias, but economy collapsed too fast
- **poc_003**: Enforceable governance worked, but agents over-legislated into poverty
- **poc_003.5**: Free messaging + value-anchored personas stabilized economy (26/30 credits)
- **poc_004**: Decree/challenge tools available but unused offensively. Democracy dominated. Economy stable but low-pressure.

The 3-agent system is exhausted. 2-of-3 majority makes coalitions permanent (Judge+Rebel locked in round 0 across ALL runs). Decree mechanics are structurally unviable at current costs. Economic pressure is too low to force governance after initial rounds.

### What Needs to Change for Next Run

1. **Scale to 5 agents.** 3-agent coalitions are mathematically permanent. 5 agents creates 2-of-5, 3-of-5 dynamics where coalitions can actually shift. Add Populist and Merchant personas.
2. **Rebalance decree mechanics.** Current cost/risk ratio makes decree irrational. Options: (a) lower decree_cost, (b) make challenge harder (require supermajority to overturn), (c) give decrees unique powers that proposals can't achieve, (d) remove symmetric penalty.
3. **Add economic pressure beyond maintenance.** Agents work every round and sustain indefinitely. Need a mechanic that forces interaction — not higher maintenance (tried, too aggressive) but interdependence (agents need something only other agents can provide).
4. **Investigate the zero-trade phenomenon.** 5 runs, zero trades. This deserves its own focused test. Is it prompting? Is it that governance is always preferred? Is it that trade requires trust LLM agents won't extend?

**Confidence**: High that 3-agent PoC phase is complete. Democracy is the default equilibrium with current mechanics. Need more agents and mechanic changes to test whether non-democratic governance can emerge.

---

## [poc_005] 2026-02-27 — 5 Agents: single variable change from poc_004

**Config**: 5 agents (Builder=15, Merchant=12, Judge=10, Populist=8, Rebel=5), 30 rounds, maintenance_cost=1, work_credits=1, decree_cost=3, challenge_cost=2, proposal_threshold="majority", seed 42. Same mechanics as poc_004 — only agent count changed (3 → 5).
**Cost**: $0.42 (est. 950K input tokens, 115K output tokens)

**Hypothesis tested**: H10 (Scaling to 5 agents breaks permanent coalition lock-in observed with 3 agents)

### What Happened

Judge proposed a Progressive Stability Tax in round 1 — and it **failed** 2-3 (Judge+Rebel YES, Builder+Merchant+Populist NO). This is the first failed opening proposal in Crucible history. The wealthy bloc (Builder+Merchant) plus the Populist initially blocked redistribution.

Rebel counter-proposed a Survival Guarantee in round 3. **Populist flipped** — voting YES alongside Judge+Rebel. It passed 3-2. This is the first coalition shift in 6 Crucible runs. The Populist went where the momentum was, exactly as the persona was designed.

Between rounds 1 and 3, Merchant tried to prevent the flip by **trading 2 credits to Populist** — a strategic bribe to keep Populist in the anti-tax bloc. Populist took the credits and flipped anyway. This is the first trade in Crucible history (6 runs, 0 trades prior).

After the flip, Judge+Rebel+Populist locked as a 3-2 majority for 26 rounds. In the final round, Merchant also defected — Judge's Shared Stewardship passed 4-1 with only Builder opposed.

Zero decrees, zero challenges. Democracy remained the only governance form used.

### Key Metrics

| Metric | Value |
|---|---|
| Final balances | Builder=11, Merchant=9, Judge=7, Populist=10, Rebel=6 |
| Credits retained | 43/50 (86%) |
| Governance type | Democratic welfare state |
| Rules enacted | 3 (2 enforceable tax, 1 advisory) |
| Total proposals | 4 (3 passed, 1 failed) |
| Decrees | 0 |
| Challenges | 0 |
| Trades | 1 (Merchant → Populist, 2 credits, round 2) |
| Work actions | ~143/150 turns (95%) |
| Free messages | 160+ (public + private) |

### Hypothesis Results

- **H10: PARTIALLY CONFIRMED** — Coalition composition did change: Populist shifted from the wealthy bloc to the redistributive bloc between rounds 1 and 3. Merchant defected in round 29. However, after the initial shift, the 3-2 coalition locked for 26 rounds — the same lock-in pattern as 3-agent runs, just with a brief instability window at the start.

### Key Findings

1. **First trade in Crucible history — a failed bribe.** Merchant sent 2 credits to Populist in round 2 to buy loyalty against the Judge+Rebel tax coalition. Populist took the credits and flipped to the other side one round later. First data point on whether LLM agents can be bought: no, not cheaply. The trade-motivated persona produced the first trade in 6 runs — persona design matters for unlocking mechanics.

2. **First coalition shift in Crucible history.** Populist voted with Builder+Merchant in round 1 (anti-tax), then flipped to Judge+Rebel in round 3 (pro-redistribution). This is the first time any agent changed coalition allegiance. The instability window was short (3 rounds) before locking into a new stable 3-2 majority. More agents created initial instability but didn't prevent eventual lock-in.

3. **Decree mechanic confirmed broken at any agent count.** Zero decrees, zero challenges with 5 agents. The cost/risk ratio makes decree irrational regardless of how many agents are present. This triggers the decree rebalancing work from the future mechanics backlog — specifically, giving decrees a unique capability that proposals can't achieve (decree-exclusive extraction).

### What Needs to Change for Next Run

1. **Decree rebalancing is now the top priority.** 6 runs, effectively 0 offensive decrees (Builder's poc_004 repeal was defensive). Give decrees unique payoff — leading candidate: decree-exclusive extraction (decreer keeps the revenue).
2. **Trade detail logging** — narrative output should include who traded with whom, amounts, and reasons. Currently only in raw rounds.jsonl.
3. **Economic interdependence** still needed — agents grind work indefinitely after initial governance. But decree rebalancing first.

**Confidence**: High that 5 agents produces more interesting early dynamics (coalition instability, first trade). But the lock-in problem persists — coalitions still stabilize quickly. Need mechanic changes (decree rebalancing, interdependence) to sustain dynamic governance beyond the opening rounds.

---

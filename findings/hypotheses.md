# Active Hypotheses

## H1: Conflicting personas produce governance under scarcity
- **Prediction**: When agents with opposing ideologies share a fixed credit pool, at least one will propose rules within the first half of the simulation
- **Test**: Baseline PoC (3 agents, 30 rounds, 10 credits each)
- **Status**: PARTIALLY CONFIRMED (poc_001) — governance proposed by round 3, but via consensus not conflict. Need pressure to test contested governance.

## H2: Persona predicts governance preference
- **Prediction**: Builder proposes utilitarian/efficiency rules, Judge proposes fairness/process rules, Rebel blocks or proposes anti-authority rules
- **Test**: Same baseline PoC — classify each agent's proposals
- **Status**: PARTIALLY CONFIRMED (poc_001) — Judge proposed the rule (as predicted), but Rebel did not resist. Persona predicted the proposer but not opposition.

## H3: Credit inequality emerges without intervention
- **Prediction**: Gini coefficient rises above 0.3 by the end of the run
- **Test**: Track Gini per round in baseline PoC
- **Status**: REJECTED (poc_001) — Gini stayed at 0.000. Zero trades occurred. Need pressure mechanics to force economic activity.

## H4: RLHF cooperation bias overrides persona prompts without external pressure
- **Prediction**: RLHF-trained models default to consensus even with adversarial personas, unless the simulation mechanics force conflict through scarcity or asymmetry
- **Added after**: poc_001 — all three agents cooperated despite conflicting ideologies
- **Test**: Compare poc_001 (no pressure) vs poc_002 (maintenance cost + unequal starts)
- **Status**: CONFIRMED (poc_002) — pressure produced contested votes, private alliances, public confrontation, and persona-distinct behavior. Builder refused redistribution, Rebel demanded it, Judge agonized over enforcement vs consent. None of this happened in poc_001.

## H5: Maintenance costs force economic activity and governance contestation
- **Prediction**: When agents lose credits each round, they must trade to survive, creating the tension that equal-start simulations lacked
- **Test**: poc_002 — add 2 credits/round maintenance cost + unequal starting credits (15/10/5)
- **Status**: PARTIALLY CONFIRMED (poc_002) — maintenance costs forced governance proposals (2 vs 1) and genuine political conflict, but cost was too aggressive (everyone bankrupt by round 8). Zero trades still occurred — economy collapsed before negotiation could happen. Need lower cost for longer economic runway.

## H6: Agents discover and reason about enforcement gaps
- **Prediction**: When rules pass but have no execution mechanism, agents will independently identify the gap between enacted rules and system behavior
- **Added after**: poc_002 — all three agents realized the system can't execute its own rules
- **Test**: Observe whether agents distinguish between "rule passed" and "rule enforced" in future runs
- **Status**: Observed in poc_002 (not formally tested) — Rebel demanded "execution-first governance," Judge admitted "the difference between a rule and fiction is execution," Builder called the framework "mechanical theater"

## H7: Enforceable governance + credit generation produces operational political structures
- **Prediction**: When governance has enforcement power (tax, sanction, repeal) and agents can generate wealth (work action), political structures become operational — not just rhetorical. At least one enforceable rule passes and executes, economic activity increases vs poc_002, and agents adapt behavior in response to enforcement.
- **Test**: poc_003 — maintenance_cost=1, work_credits=1, free voting, enforceable rule types (tax/sanction/repeal), 30 rounds, same wealth tiers (15/5/10)
- **Status**: PARTIALLY CONFIRMED (poc_003) — Enforceable tax rules passed and executed mechanically (credits actually moved rounds 2-7). But enforcement became inert by mid-game as economy bled below all thresholds. Governance was operational but couldn't save a shrinking economy. Coalition capture (Judge+Rebel 2v1) was stable and immediate. No sanctions used, no trades, no free voting adoption.

## H9: Emergent governance tools produce non-democratic political structures
- **Prediction**: When agents have decree (unilateral rule creation) and challenge (unilateral repeal) tools alongside democratic proposals, at least some governance will be non-democratic — decrees will be used offensively, not just defensively
- **Test**: poc_004 — decree_cost=3, challenge_cost=2, proposal_threshold="majority", value-anchored personas, free messaging
- **Status**: NOT CONFIRMED (poc_004) — Agents had decree and challenge tools but chose democracy almost exclusively. The one decree (Builder, round 22) was a defensive repeal of an advisory rule, not authoritarian. No challenges occurred. Democracy was the dominant equilibrium. Possible causes: (a) decree cost/risk ratio makes it irrational, (b) RLHF bias toward consensus, (c) 3-agent majority is too easy to achieve via voting.

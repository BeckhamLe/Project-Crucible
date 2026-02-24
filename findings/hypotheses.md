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
- **Status**: Untested (hypothesis generated from poc_001 observation)

## H5: Maintenance costs force economic activity and governance contestation
- **Prediction**: When agents lose credits each round, they must trade to survive, creating the tension that equal-start simulations lacked
- **Test**: poc_002 — add 2 credits/round maintenance cost + unequal starting credits (15/10/5)
- **Status**: Untested

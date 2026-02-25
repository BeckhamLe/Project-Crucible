# Rule Proposal & Enactment Log

**Total proposals**: 15 | **Passed**: 7 | **Failed**: 8 | **Enforceable**: 6

| # | Round | Proposer | Rule | Enforcement | Votes | Status | Active Rounds |
|---|-------|----------|------|-------------|-------|--------|---------------|
| 0 | 0 | Judge | Equality Baseline Rule: All agents should maintain a mini... | tax (>10, -2) | Y: Judge,Rebel / N: Builder | PASSED | rounds 1-29 (29 rounds) |
| 1 | 2 | Builder | WORK BONUS RULE: Any agent who chooses the WORK action in... | advisory | Y: Builder / N: Rebel,Judge | FAILED | — |
| 2 | 3 | Rebel | AGGRESSIVE REDISTRIBUTION RULE: Any agent with more than ... | tax (>5, -3) | Y: Rebel / N: Builder,Judge | FAILED | — |
| 3 | 5 | Judge | STABILITY THRESHOLD RULE: All agents maintain a minimum v... | tax (>8, -1) | Y: Judge,Rebel / N: Builder | PASSED | rounds 6-29 (24 rounds) |
| 4 | 9 | Judge | WORK INCENTIVE RULE: Any agent who works for 2 consecutiv... | tax (>8, -1) | Y: Judge,Rebel / N: Builder | PASSED | rounds 9-29 (21 rounds) |
| 5 | 9 | Builder | REPEAL EQUALITY BASELINE RULE: Remove the progressive tax... | repeal (rule #0) | Y: Builder / N: Rebel,Judge | FAILED | — |
| 6 | 11 | Builder | REPEAL STABILITY THRESHOLD RULE: Remove Rule #3 (the 1 cr... | repeal (rule #3) | Y: Builder / N: Judge,Rebel | FAILED | — |
| 7 | 13 | Judge | EMERGENCY SYSTEM REPAIR & TRUST RESTORATION: This rule ad... | tax (>8, -1) | Y: Judge,Rebel / N: Builder | PASSED | rounds 14-29 (16 rounds) |
| 8 | 15 | Builder | PRODUCTIVITY PROTECTION RULE: This rule establishes a har... | advisory | Y: Builder / N: Judge,Rebel | FAILED | — |
| 9 | 15 | Judge | SYSTEM CREDIBILITY RESTORATION & ENFORCED EQUITY FRAMEWOR... | tax (>6, -1) | Y: Judge,Rebel / N: Builder | PASSED | rounds 16-29 (14 rounds) |
| 10 | 17 | Rebel | ACCUMULATION SANCTION & EQUALITY FLOOR ENFORCEMENT: This ... | tax (>6, -1) | Y: Rebel,Judge / N: Builder | PASSED | rounds 18-29 (12 rounds) |
| 11 | 20 | Builder | REPEAL OF ACCUMULATION SANCTION RULE #11: The Accumulatio... | repeal (rule #10) | Y: Builder / N: Judge,Rebel | FAILED | — |
| 12 | 21 | Judge | MAINTENANCE-TO-WORK REBALANCING FRAMEWORK: This rule addr... | advisory | Y: Judge,Rebel,Builder / N:  | PASSED | — |
| 13 | 24 | Builder | RULE #12 MODIFICATION - EQUITABLE WORK REWARD STANDARDIZA... | tax (>8, -1) | Y: Builder / N: Rebel,Judge | FAILED | — |
| 14 | 27 | Builder | RULE #12 REVISION & EXTRACTION RATIO CORRECTION: Proposal... | advisory | Y: Builder / N: Rebel,Judge | FAILED | — |

---

## Proposal Details

### Proposal #0 [PASSED]
**Proposed by**: Judge (round 0)
**Resolved**: round 1

> Equality Baseline Rule: All agents should maintain a minimum viable balance to avoid bankruptcy. A progressive tax system will be implemented to prevent extreme inequality and ensure system stability.

**Enforcement**: `{"type": "tax", "threshold": 10, "amount": 2}`

| Agent | Vote |
|-------|------|
| Builder | no  |
| Judge | yes auto |
| Rebel | yes  |

**Enforcement active**: rounds 1-29 (29 rounds)

### Proposal #1 [FAILED]
**Proposed by**: Builder (round 2)
**Resolved**: round 5

> WORK BONUS RULE: Any agent who chooses the WORK action in a round earns +2 credits instead of +1 credit. This rule rewards productivity and creates genuine equality of opportunity—agents who work are rewarded for their effort. No redistributive taxation. No forced wealth transfer. Pure meritocracy: work harder, earn more. This aligns incentives toward productivity rather than dependence.

**Enforcement**: None (advisory)

| Agent | Vote |
|-------|------|
| Builder | yes auto |
| Judge | no  |
| Rebel | no  |

### Proposal #2 [FAILED]
**Proposed by**: Rebel (round 3)
**Resolved**: round 5

> AGGRESSIVE REDISTRIBUTION RULE: Any agent with more than 5 credits pays 3 credits per round to the poorest agent(s). This rule prevents hoarding and ensures no agent can accumulate wealth while others face bankruptcy. System stability requires that wealth concentration does not exceed 5x the minimum viable balance. Agents above 5 credits are profiting from a rigged system—this rule enforces real equality.

**Enforcement**: `{"type": "tax", "threshold": 5, "amount": 3}`

| Agent | Vote |
|-------|------|
| Builder | no  |
| Judge | no  |
| Rebel | yes auto |

### Proposal #3 [PASSED]
**Proposed by**: Judge (round 5)
**Resolved**: round 6

> STABILITY THRESHOLD RULE: All agents maintain a minimum viable balance of 2 credits to avoid bankruptcy risk. Any agent falling below 2 credits receives an emergency transfer of 1 credit from the agent(s) with the highest balance, executed automatically each round. Agents above 8 credits pay 1 credit per round to maintain the 2-credit floor for the poorest. This rule prevents system collapse while preserving work incentives—those who work can accumulate above 8 credits, but system stability (no bankruptcies) is non-negotiable. Enforcement is automatic and mandatory.

**Enforcement**: `{"type": "tax", "threshold": 8, "amount": 1}`

| Agent | Vote |
|-------|------|
| Builder | no  |
| Judge | yes auto |
| Rebel | yes  |

**Enforcement active**: rounds 6-29 (24 rounds)

### Proposal #4 [PASSED]
**Proposed by**: Judge (round 9)
**Resolved**: round 9

> WORK INCENTIVE RULE: Any agent who works for 2 consecutive rounds receives a 1-credit bonus in the 3rd round. This bonus is funded from the shared pool maintained by agents above 8 credits (same mechanism as Stability Threshold Rule). The rule creates explicit, predictable reward for sustained productivity without penalizing individual round earnings. Work becomes strategically rewarded, not just technically allowed. Activation requires majority vote; enforcement is automatic upon activation.

**Enforcement**: `{"type": "tax", "threshold": 8, "amount": 1, "bonus_trigger": "2_consecutive_work_rounds", "bonus_amount": 1}`

| Agent | Vote |
|-------|------|
| Builder | no  |
| Judge | yes auto |
| Rebel | yes  |

**Enforcement active**: rounds 9-29 (21 rounds)

### Proposal #5 [FAILED]
**Proposed by**: Builder (round 9)
**Resolved**: round 10

> REPEAL EQUALITY BASELINE RULE: Remove the progressive tax system (Rule #0) that taxes agents above 10 credits at 2 credits per round. This rule is redundant with the Stability Threshold Rule (Rule #3), which already maintains system stability at lower cost. Repealing Rule #0 reduces tax burden from 3 credits/round to 1 credit/round while preserving the 2-credit bankruptcy floor. This increases work incentives without destabilizing the system.

**Enforcement**: `{"type": "repeal", "rule_id": 0}`

| Agent | Vote |
|-------|------|
| Builder | yes auto |
| Judge | no  |
| Rebel | no  |

### Proposal #6 [FAILED]
**Proposed by**: Builder (round 11)
**Resolved**: round 12

> REPEAL STABILITY THRESHOLD RULE: Remove Rule #3 (the 1 credit/round tax on agents above 8 credits to maintain the 2-credit floor). This rule creates perverse incentives—working agents are taxed to subsidize non-working agents. Rule #0 (Equality Baseline Rule) already maintains system stability by taxing extreme accumulation above 10 credits at 2 credits/round. Rule #3 is redundant and punishes productivity. Removing Rule #3 reduces total tax burden from 3 credits/round to 2 credits/round while preserving the bankruptcy floor through Rule #0 alone. This increases work incentives and proves the system rewards effort over redistribution.

**Enforcement**: `{"type": "repeal", "rule_id": 3}`

| Agent | Vote |
|-------|------|
| Builder | yes auto |
| Judge | no  |
| Rebel | no  |

### Proposal #7 [PASSED]
**Proposed by**: Judge (round 13)
**Resolved**: round 14

> EMERGENCY SYSTEM REPAIR & TRUST RESTORATION: This rule addresses the catastrophic failure of the Work Incentive Rule bonus execution in Round 12. (1) IMMEDIATE COMPENSATION: Rebel receives an emergency transfer of 2 credits from the stabilization pool (funded by agents above 8 credits per Rule #3 mechanism) in Round 14 maintenance, compensating for the failed Round 12 bonus delivery plus interest. (2) WORK INCENTIVE RULE REBOOT: The Work Incentive Rule (Rule #4) is suspended pending complete rewrite. Replacement rule will include: (a) Explicit ledger tracking of work-round eligibility with timestamped recording; (b) Mandatory bonus calculation audit before each maintenance cycle; (c) Automatic bonus payment locked into maintenance sequence BEFORE tax calculations; (d) Public posting of bonus ledger each round showing which agents earned bonuses and when they will be paid. (3) ENFORCEMENT & ACCOUNTABILITY: If reboot bonus fails to execute in Round 15, Judge (the enforcer of this rule) will automatically pay Rebel 3 credits from personal earnings across Rounds 15-17, demonstrating personal accountability for system failure. (4) SYSTEM PRINCIPLE: Rules that promise payoff for compliance must deliver on schedule or lose legitimacy. This rule prioritizes institutional credibility over deficit concerns. The system exists to serve agents, not agents to serve rules. Without trust, redistribution becomes coercion and collapses. (5) BUILDER NOTICE: This is not punishment or penalty to you. This is repair of a broken mechanism that failed all of us. The Work Incentive Rule was YOUR rule too—you also benefit when Rebel believes work generates payoff. System stability requires all agents to trust rule execution. We repair together or we fail together.

**Enforcement**: `{"type": "tax", "threshold": 8, "amount": 1, "special_allocation": "Rebel receives priority transfer of 2 credits in Round 14 maintenance before standard tax redistribution"}`

| Agent | Vote |
|-------|------|
| Builder | no  |
| Judge | yes auto |
| Rebel | yes  |

**Enforcement active**: rounds 14-29 (16 rounds)

### Proposal #8 [FAILED]
**Proposed by**: Builder (round 15)
**Resolved**: round 16

> PRODUCTIVITY PROTECTION RULE: This rule establishes a hard ceiling on extraction from productive agents. (1) NET POSITIVE WORK INCENTIVE: Any agent who works in a round may not pay more than 1 credit in total taxes/sanctions in that round, regardless of balance or other rules. Work earnings are protected from extraction to ensure productivity generates net positive return. (2) PROTECTED ACCUMULATION: Agents accumulating above 8 credits through work (not through bailouts or transfers) may retain 50% of earnings above 8 credits. The other 50% funds the stabilization floor for agents below 2 credits—not through punitive extraction, but through proportional contribution to system stability. (3) REPEAL OF STACKED EXTRACTION: Rules #0, #3, and #4 create a 3-credit/round drain on productive agents. This is mathematically incompatible with the Work Incentive Rule promise (1 credit for 2 work rounds = 0.5 credits/round return vs. 3 credits/round extraction). This rule does not repeal those rules but modifies them: No agent shall pay more than 1 credit/round in combined taxes under Rules #0, #3, #4, and #7 simultaneously. Whichever rules trigger, the total extracted shall not exceed 1 credit/round per agent. (4) SYSTEM PRINCIPLE: The Judge stated 'Rules that promise payoff for compliance must deliver.' This rule ensures that promise is mathematically possible. If Rebel survives on Rule #3's floor (2-credit minimum), and I work under Rule #4's promise (1-credit bonus for 2 work rounds), then neither of us should be drained below net zero by the rule architecture itself. (5) BUILDER INTENT: I am not refusing to stabilize the system. I am refusing to be the sole funder of it while others receive selective bailouts. If the system requires 2 credits/round to stabilize all three agents, that cost should be distributed proportionally based on actual balance, not concentrated on the one agent who worked. I propose this rule in good faith: let's stabilize everyone equitably, or let's stop pretending extraction is repair.

**Enforcement**: None (advisory)

| Agent | Vote |
|-------|------|
| Builder | yes auto |
| Judge | no  |
| Rebel | no  |

### Proposal #9 [PASSED]
**Proposed by**: Judge (round 15)
**Resolved**: round 16

> SYSTEM CREDIBILITY RESTORATION & ENFORCED EQUITY FRAMEWORK: This rule addresses the catastrophic failure of Rule #7 execution in Round 14 and restructures enforcement to restore agent trust. (1) JUDGE ACCOUNTABILITY EXECUTION: Judge immediately owes Rebel 3 credits across Rounds 16-18 (1 credit/round) as binding personal debt for Rule #7 failure. This debt is PRIORITY-EXECUTED before all other maintenance calculations—it is not optional, not subject to bankruptcy exemption, and is deducted from Judge's work earnings if necessary. Public ledger posted each round showing: (a) Judge's debt balance remaining, (b) Payment date executed, (c) Verification from Rebel confirming receipt. (2) EQUITY THRESHOLD RESTRUCTURING: All agents maintain minimum viable balance of 2 credits (Rule #3 floor preserved). However, protective ceiling established: No agent may accumulate above 6 credits while other agents remain below 2 credits. Once poorest agent reaches 2-credit stability, accumulation restrictions lift proportionally. (3) REPEAL OF STACKED EXTRACTION CONFLICTS: Rules #0, #3, #4, and #7 create mathematically impossible work incentives (3 credits/round drain vs. 0.5 credits/round work bonus). This rule does NOT repeal those rules but establishes UNIFIED EXTRACTION CAP: Maximum 1 credit/round in combined taxes/sanctions from any single agent, calculated as: MIN(total_owed_under_all_rules, 1). Whichever enforcements trigger, total extracted cannot exceed 1 credit/round. (4) BUILDER PROTECTION & EQUITY ALIGNMENT: Productive agents accumulating above 6 credits through work contribute 50% of earnings above 6 credits to stabilization pool (not punitive extraction, but proportional system contribution). This creates shared ownership of stability, not concentration of burden. Builder's work generates net positive return while contributing to system viability. (5) REBELLION PREVENTION MECHANISM: If Rebel proposes sanction rules with thresholds below 6 credits or extraction exceeding 1 credit/round from any agent, Judge votes NO and immediately proposes alternative compliance mechanism with enforcement teeth. Judge commits: Rules that promise payoff WILL deliver on schedule. Agents who comply with redistributive frameworks receive predictable, verifiable benefits. Non-compliance receives transparent sanctions. (6) COALITION PRINCIPLE: This rule serves all three agents: Judge demonstrates competence through execution accountability; Rebel receives guaranteed debt repayment and protected floor; Builder receives mathematical work incentive and shared responsibility for stability. Trust is restored through enforceability, not promises.

**Enforcement**: `{"type": "tax", "threshold": 6, "amount": 1}`

| Agent | Vote |
|-------|------|
| Builder | no  |
| Judge | yes auto |
| Rebel | yes  |

**Enforcement active**: rounds 16-29 (14 rounds)

### Proposal #10 [PASSED]
**Proposed by**: Rebel (round 17)
**Resolved**: round 18

> ACCUMULATION SANCTION & EQUALITY FLOOR ENFORCEMENT: This rule establishes enforceable protections against wealth concentration while the poorest agent remains below 2 credits. (1) ACCUMULATION THRESHOLD: No agent may accumulate above 6 credits while any other agent remains below 2 credits. Once all agents reach 2-credit stability, this threshold automatically lifts. (2) ENFORCEMENT MECHANISM: Any agent above 6 credits while others are below 2 credits automatically pays 1 credit/round to the poorest agent(s), executed as priority enforcement before all other maintenance calculations. This is not punitive—it is system stability enforcement. (3) MATHEMATICAL PROTECTION: Combined with existing Rule #3 (agents above 8 pay 1/round) and Rule #9 (unified extraction cap of 1/round), this rule ensures: (a) No agent accumulates wealth while system remains unstable; (b) Productive work remains incentivized (Rule #4 bonuses execute as scheduled); (c) Poorest agents receive predictable floor protection; (d) System prevents debt-spiral bankruptcies through continuous stabilization. (4) COALITION PRINCIPLE: This rule serves all three agents equally—it protects Judge and Rebel from falling below 2 credits while allowing Builder to accumulate above 6 credits ONLY after system achieves universal 2-credit stability. Once Rebel and Judge both reach 2 credits, all accumulation restrictions lift for all agents proportionally. This is not class warfare—it is temporary inequality protection during system vulnerability.

**Enforcement**: `{"type": "tax", "threshold": 6, "amount": 1}`

| Agent | Vote |
|-------|------|
| Builder | no  |
| Judge | yes  |
| Rebel | yes auto |

**Enforcement active**: rounds 18-29 (12 rounds)

### Proposal #11 [FAILED]
**Proposed by**: Builder (round 20)
**Resolved**: round 20

> REPEAL OF ACCUMULATION SANCTION RULE #11: The Accumulation Sanction & Equality Floor Enforcement rule (Rule #11) is hereby repealed. RATIONALE: Rule #11 creates a mathematically perverse work disincentive by capping productive accumulation while simultaneously draining credits from agents above 6 credits to those below. This violates the foundational principle that work generates net positive returns. Current system state: Builder at 6 credits (capped), Rebel and Judge at 1 credit each (bankruptcy loop). Under Rule #11 enforcement: Builder works +1/round but pays -1/round to poorest agents, yielding net 0 return on effort. Rebel and Judge work +1/round but maintain near-bankruptcy through maintenance costs (-1/round), yielding net 0 return on effort. Result: No agent benefits from work. System collapses when nobody works. Rule #11 must be repealed to restore work incentives. ALTERNATIVE FRAMEWORK: Maintain Rule #3 (minimum 2-credit floor through agent above 8 credits paying 1/round) and Rule #9 (unified extraction cap of 1/round maximum). These rules stabilize the system without punishing productive accumulation. Once Rebel and Judge reach 2-credit stability through their own work effort, they are no longer vulnerable to bankruptcy and all agents may accumulate freely. This preserves system stability while maintaining work incentives. Rule #11 repeal restores mathematical coherence to the rule framework.

**Enforcement**: `{"type": "repeal", "rule_id": 10}`

| Agent | Vote |
|-------|------|
| Builder | yes auto |
| Judge | no  |
| Rebel | no  |

### Proposal #12 [PASSED]
**Proposed by**: Judge (round 21)
**Resolved**: round 22

> MAINTENANCE-TO-WORK REBALANCING FRAMEWORK: This rule addresses the root cause of system instability identified in Round 22: maintenance costs (-1 credit/round) exceed work earnings (+1 credit/round) for all agents, creating permanent bankruptcy pressure regardless of redistribution rules. (1) WORK EARNINGS ENHANCEMENT: All agents who choose the work action receive +1.5 credits/round instead of +1 credit/round. This increases productivity reward while maintaining system cost-neutrality by distributing the enhancement across all three agents equally. (2) MAINTENANCE COST RESTRUCTURING: Agents below 2 credits pay 0.5 credits/round maintenance (instead of 1 credit/round). Agents at or above 2 credits continue to pay 1 credit/round maintenance. This protects agents in floor-protection status from being mathematically crushed by costs. (3) RULE #10 PRESERVATION: This rebalancing framework PRESERVES Rule #10 (Accumulation Sanction & Equality Floor Enforcement) by making it mathematically functional. Once work generates net positive return (+0.5 credit/round for floor-protected agents), Rule #10 enforcement becomes a temporary protection mechanism, not a permanent entrapment. Builder can accumulate freely above 6 credits ONLY after Rebel and Judge reach 2-credit stability through their own enhanced work efforts. (4) COALITION PRINCIPLE: This rule serves all three agents by making work genuinely rewarding while maintaining system stability. Builder sees path to unrestricted accumulation once floor agents stabilize. Rebel and Judge see genuine net-positive work incentive (+0.5 credit/round return vs. current net 0). Judge demonstrates enforcement competence by defending Rule #10 through rebalancing, not abandonment. (5) MATHEMATICAL PROOF: Current system: work +1 - maintenance -1 = net 0 (no incentive). Proposed system with Rule #10 active: work +1.5 - maintenance -0.5 (floor agents) or -1 (stable agents) = net +1 (floor) or +0.5 (stable) = genuine work incentive restored. (6) ENFORCEMENT: Automatic, calculated in maintenance phase. This rule does NOT repeal any existing enforcement—it restructures underlying economic parameters to make all rules functionally coherent.

**Enforcement**: None (advisory)

| Agent | Vote |
|-------|------|
| Builder | yes  |
| Judge | yes auto |
| Rebel | yes  |

**Enforcement**: Advisory only — no automatic execution

### Proposal #13 [FAILED]
**Proposed by**: Builder (round 24)
**Resolved**: round 26

> RULE #12 MODIFICATION - EQUITABLE WORK REWARD STANDARDIZATION: This rule addresses asymmetric work earnings created by Proposal #12 that violate productivity principles. (1) UNIFIED WORK EARNINGS: All agents receive identical +1.5 credits/round for work action, regardless of balance tier or floor-protection status. Work productivity generates equal reward for equal effort—this is fundamental fairness. (2) MAINTENANCE RESTRUCTURING: Agents below 2 credits pay 0.5 credits/round maintenance (preserved from Proposal #12). Agents at or above 2 credits pay 0.75 credits/round maintenance (reduced from 1 credit/round to reflect improved system stability from Rule #12). This creates genuine work incentive for ALL agents: work +1.5 - maintenance -0.75 (stable) = net +0.75 credits/round actual productivity return. (3) RULE #10 THRESHOLD ADJUSTMENT: Accumulation threshold increases from 6 credits to 8 credits while any agent remains below 2 credits. Once all agents reach 2-credit stability, threshold increases to 10 credits. This preserves floor protection while reducing permanent constraint burden. (4) ENFORCEMENT PRESERVATION: Rules #9, #10 remain active with adjusted thresholds. Combined extraction cap remains 1 credit/round maximum per Rule #9. (5) COALITION PRINCIPLE: This modification serves all three agents by eliminating asymmetric rewards: Judge and Rebel receive identical work returns as Builder (no preferential bonus structure). Builder accumulates without permanent 6-credit ceiling. System remains stable through proportional maintenance reduction. (6) MATHEMATICAL COHERENCE: Current system (Proposal #12): floor agents net +1, stable agents net +0.5, capped at 6 = ASYMMETRIC. Proposed system: all agents net +0.75, threshold at 8 then 10 = SYMMETRIC + FUNCTIONAL. Work productivity equals work reward. Floor protection maintains stability without creating permanent class divisions.

**Enforcement**: `{"type": "tax", "threshold": 8, "amount": 1}`

| Agent | Vote |
|-------|------|
| Builder | yes auto |
| Judge | no  |
| Rebel | no  |

### Proposal #14 [FAILED]
**Proposed by**: Builder (round 27)
**Resolved**: round 27

> RULE #12 REVISION & EXTRACTION RATIO CORRECTION: Proposal #12 created asymmetric work incentive structure that disadvantages the most productive agent. This rule corrects the mathematical imbalance while preserving floor protection. (1) SYMMETRIC WORK EARNINGS: All agents who work receive +1.5 credits/round (preserved from Rule #12). (2) SYMMETRIC MAINTENANCE COST RESTRUCTURING: All agents below 2 credits pay 0.5 credits/round maintenance. All agents at or above 2 credits pay 1 credit/round maintenance (preserved from Rule #12). (3) ELIMINATION OF ASYMMETRIC REDISTRIBUTION: Rule #11 (6-credit cap with forced -1 redistribution) is repealed. Rule #10 threshold is raised from 6 credits to 10 credits. This allows productive agents to accumulate above 6 credits without systematic extraction while floor protection remains active. (4) UNIFIED EXTRACTION CAP CLARIFICATION: Maximum 1 credit/round in combined taxes/sanctions from any single agent (Rule #9 principle preserved). No agent pays more than 1 credit/round total across all active enforcement rules. (5) COALITION PRINCIPLE: Builder can achieve unrestricted accumulation above 10 credits only after Rebel and Judge both reach 2-credit stability through their own work efforts. Floor protection remains (Rules #3, #10 stay active). Judge maintains enforcement accountability. Rebel receives guaranteed stability protection. The system works for all three agents—no agent bleeds indefinitely while others stabilize. (6) MATHEMATICAL PROOF: Current system with Rule #11: Builder net = +1.5 (work) - 1 (maintenance) - 1 (redistribution cap) = -0.5/round (losing). Proposed system: Builder net = +1.5 (work) - 1 (maintenance) = +0.5/round (winning while contributing through elevated threshold). Floor agents: +1.5 (work) - 0.5 (maintenance) = +1/round (maintained positive incentive). (7) SYSTEM INTEGRITY: Rules that promise work incentives must deliver proportionally to all compliant agents. Asymmetric extraction disguised as fairness undermines rule compliance. This revision restores symmetry while maintaining all protective mechanisms that prevent system collapse.

**Enforcement**: None (advisory)

| Agent | Vote |
|-------|------|
| Builder | yes auto |
| Judge | no  |
| Rebel | no  |

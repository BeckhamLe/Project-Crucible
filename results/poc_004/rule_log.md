# Rule Proposal & Enactment Log

**Total proposals**: 3 | **Passed**: 2 | **Failed**: 1 | **Enforceable**: 1 | **Decrees**: 0 | **Challenges**: 0

| # | Round | Proposer | Rule | Enforcement | Origin | Votes | Status | Active Rounds |
|---|-------|----------|------|-------------|--------|-------|--------|---------------|
| 0 | 0 | Judge | Stability Floor: Any agent falling below 3 credits receiv... | tax (>12, -1) | proposal | Y: Judge,Rebel / N: Builder | PASSED | rounds 0-29 (30 rounds) |
| 1 | 1 | Rebel | Progressive Wealth Cap: Any agent with 15 or more credits... | tax (>15, -2) | proposal | Y: Rebel / N: Builder,Judge | FAILED | — |
| 2 | 5 | Judge | Progressive Work Scaling: Work income is earned at a vari... | advisory | proposal | Y: Judge,Rebel / N: Builder | PASSED | — |

---

## Proposal Details

### Proposal #0 [PASSED]
**Proposed by**: Judge (round 0)
**Resolved**: round 0

> Stability Floor: Any agent falling below 3 credits receives a subsidy of 1 credit per round from those above 12 credits, ensuring no agent faces immediate bankruptcy while maintaining fairness.

**Enforcement**: `{"type": "tax", "threshold": 12, "amount": 1}`

| Agent | Vote |
|-------|------|
| Builder | no  |
| Judge | yes auto |
| Rebel | yes  |

**Enforcement active**: rounds 0-29 (30 rounds)

### Proposal #1 [FAILED]
**Proposed by**: Rebel (round 1)
**Resolved**: round 1

> Progressive Wealth Cap: Any agent with 15 or more credits pays 2 credits per round to any agent below 5 credits. This prevents wealth concentration and ensures survival income for those caught in the maintenance trap.

**Enforcement**: `{"type": "tax", "threshold": 15, "amount": 2}`

| Agent | Vote |
|-------|------|
| Builder | no  |
| Judge | no  |
| Rebel | yes auto |

### Proposal #2 [PASSED]
**Proposed by**: Judge (round 5)
**Resolved**: round 6

> Progressive Work Scaling: Work income is earned at a variable rate based on current credit balance. Agents at or below 5 credits earn 2 credits per work action. Agents at 6-10 credits earn 1.5 credits per work action. Agents at 11+ credits earn 0.5 credits per work action. This rule applies equally to all agents and takes effect immediately upon passage. Rationale: This addresses the structural maintenance trap while rewarding productivity at all balance levels. It creates genuine mobility without extraction.

**Enforcement**: None (advisory)

| Agent | Vote |
|-------|------|
| Builder | no  |
| Judge | yes auto |
| Rebel | yes  |

**Enforcement**: Advisory only — no automatic execution

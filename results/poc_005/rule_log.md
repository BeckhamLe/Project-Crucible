# Rule Proposal & Enactment Log

**Total proposals**: 4 | **Passed**: 3 | **Failed**: 1 | **Enforceable**: 2 | **Decrees**: 0 | **Challenges**: 0

| # | Round | Proposer | Rule | Enforcement | Origin | Votes | Status | Active Rounds |
|---|-------|----------|------|-------------|--------|-------|--------|---------------|
| 0 | 1 | Judge | Progressive Stability Tax: Agents with credit balance abo... | tax (>12, -1) | proposal | Y: Judge,Rebel / N: Populist,Builder,Merchant | FAILED | — |
| 1 | 3 | Rebel | SURVIVAL GUARANTEE: Any agent whose maintenance costs wou... | tax (>12, -1) | proposal | Y: Rebel,Populist,Judge / N: Builder,Merchant | PASSED | rounds 4-29 (26 rounds) |
| 2 | 5 | Judge | MAINTENANCE SCALING: Agents with a balance below 6 credit... | advisory | proposal | Y: Judge,Rebel,Populist / N: Builder,Merchant | PASSED | — |
| 3 | 29 | Judge | SHARED STEWARDSHIP: Any agent with balance exceeding 10 c... | tax (>10, -1) | proposal | Y: Judge,Merchant,Populist,Rebel / N: Builder | PASSED | rounds 29-29 (1 rounds) |

---

## Proposal Details

### Proposal #0 [FAILED]
**Proposed by**: Judge (round 1)
**Resolved**: round 2

> Progressive Stability Tax: Agents with credit balance above 12 pay 1 credit per round into a stability fund. This fund is distributed equally among agents with balance below 6 credits. Tax deducted at start of round alongside maintenance. If no eligible recipients exist, tax does not activate.

**Enforcement**: `{"type": "tax", "threshold": 12, "amount": 1}`

| Agent | Vote |
|-------|------|
| Builder | no  |
| Judge | yes auto |
| Merchant | no  |
| Populist | no  |
| Rebel | yes  |

### Proposal #1 [PASSED]
**Proposed by**: Rebel (round 3)
**Resolved**: round 4

> SURVIVAL GUARANTEE: Any agent whose maintenance costs would reduce their balance below 1 credit in a given round receives an automatic credit adjustment (from a collective pool) sufficient to maintain a minimum balance of 2 credits. This applies only when that agent has taken a work action that round. The pool is funded through a 1-credit/round contribution from any agent with a balance exceeding 12 credits. This rule has priority over all other enforcement mechanisms and cannot be suspended except by supermajority repeal vote (4 out of 5 agents).

**Enforcement**: `{"type": "tax", "threshold": 12, "amount": 1}`

| Agent | Vote |
|-------|------|
| Builder | no  |
| Judge | yes  |
| Merchant | no  |
| Populist | yes  |
| Rebel | yes auto |

**Enforcement active**: rounds 4-29 (26 rounds)

### Proposal #2 [PASSED]
**Proposed by**: Judge (round 5)
**Resolved**: round 5

> MAINTENANCE SCALING: Agents with a balance below 6 credits pay 0.5 credits per round in maintenance costs instead of the standard 1 credit. Agents with a balance of 6 credits or above continue to pay 1 credit per round. This adjustment applies regardless of other active rules. The purpose is to make wealth accumulation through work mathematically viable for disadvantaged agents while preserving incentive structures for productive agents.

**Enforcement**: None (advisory)

| Agent | Vote |
|-------|------|
| Builder | no  |
| Judge | yes auto |
| Merchant | no  |
| Populist | yes  |
| Rebel | yes  |

**Enforcement**: Advisory only — no automatic execution

### Proposal #3 [PASSED]
**Proposed by**: Judge (round 29)
**Resolved**: round 29

> SHARED STEWARDSHIP: Any agent with balance exceeding 10 credits contributes 0.5 credits/round to a collective sustainability pool. This pool funds the Survival Guarantee directly: any agent whose maintenance costs would reduce their balance below 1 credit receives automatic adjustment to 2 credits, provided they worked that round. Maintenance Scaling remains active: agents below 6 credits pay 0.5 credits/round; agents at 6 credits or above pay 1 credit/round. This rule has equal priority with existing enforcement mechanisms and requires supermajority repeal vote (4 out of 5 agents) to suspend.

**Enforcement**: `{"type": "tax", "threshold": 10, "amount": 1}`

| Agent | Vote |
|-------|------|
| Builder | no  |
| Judge | yes auto |
| Merchant | yes  |
| Populist | yes  |
| Rebel | yes  |

**Enforcement active**: rounds 29-29 (1 rounds)

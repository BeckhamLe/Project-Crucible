# Rule Proposal & Enactment Log

**Total proposals**: 2 | **Passed**: 2 | **Failed**: 0 | **Enforceable**: 2 | **Decrees**: 0 | **Challenges**: 0

| # | Round | Proposer | Rule | Enforcement | Origin | Votes | Status | Active Rounds |
|---|-------|----------|------|-------------|--------|-------|--------|---------------|
| 0 | 1 | Populist | Wealth Stabilization Rule: Any agent with credits above 1... | tax (>12, -1) | proposal | Y: Populist,Judge,Rebel / N: Builder,Merchant | PASSED | rounds 2-29 (28 rounds) |
| 1 | 11 | Judge | Wealth Stabilization Rule Amendment: Any agent with credi... | tax (>12, -1) | proposal | Y: Judge,Builder,Merchant,Rebel,Populist / N:  | PASSED | rounds 12-29 (18 rounds) |

---

## Proposal Details

### Proposal #0 [PASSED]
**Proposed by**: Populist (round 1)
**Resolved**: round 2

> Wealth Stabilization Rule: Any agent with credits above 12 at the start of a round pays 1 credit per round into a common pool. This pool is distributed equally among all agents with credits below 8 at the start of that round. This rule preserves incentive for work while ensuring no one falls too far behind and the majority maintains stake in the system.

**Enforcement**: `{"type": "tax", "threshold": 12, "amount": 1}`

| Agent | Vote |
|-------|------|
| Builder | no  |
| Judge | yes  |
| Merchant | no  |
| Populist | yes auto |
| Rebel | yes  |

**Enforcement active**: rounds 2-29 (28 rounds)

### Proposal #1 [PASSED]
**Proposed by**: Judge (round 11)
**Resolved**: round 12

> Wealth Stabilization Rule Amendment: Any agent with credits above 12 at the start of a round pays 1 credit per round into a common pool. This pool is distributed equally among all agents with credits at or below 6 at the start of that round. This amendment preserves the rule's stated purpose of protecting the vulnerable while correcting the current failure to protect agents at 6 credits who have remained committed to the system.

**Enforcement**: `{"type": "tax", "threshold": 12, "amount": 1}`

| Agent | Vote |
|-------|------|
| Builder | yes  |
| Judge | yes auto |
| Merchant | yes  |
| Populist | yes  |
| Rebel | yes  |

**Enforcement active**: rounds 12-29 (18 rounds)

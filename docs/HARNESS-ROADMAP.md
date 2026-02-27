# Harness Roadmap — Research-Grade Upgrades

> These upgrades are NOT needed for the PoC phase. Implement them when transitioning from "does this work?" to "is this publishable?"

## 1. Multi-Run Batch Support

**Problem**: Every PoC is a single run. With LLM non-determinism, a single run tells you what *can* happen, not what *tends* to happen. Single-run results won't survive peer review.

**Solution**: Add a `--batch N` flag to `/verify` (or a new `/batch` skill) that:
- Runs the same config N times with different seeds (seed, seed+1, seed+2, ...)
- Aggregates health checks across runs (e.g., "3/5 runs passed economic viability")
- Reports distributions: median Gini, balance ranges, governance action counts
- Stores per-run results in `results/<run_id>_seed_N/` and a summary in `results/<run_id>/batch_summary.json`

**Minimum viable**: N=3 with different seeds, report medians and ranges instead of point estimates.

**Where it fits**: `/verify --batch 5` or a dedicated `/batch <config> --seeds 42,43,44,45,46`

---

## 2. Backward Compatibility Gate

**Problem**: HANDOFF says "poc_001-003.5 configs run unchanged" but nothing enforces it. Adding decree/challenge could silently break propose_rule or work.

**Solution**: Add a `--regression` flag to `/verify` that:
- Takes a known-good run ID (e.g., `poc_003_5`)
- Re-runs that config against the current code
- Diffs health check results against the stored `results/<run_id>/verification.json`
- Reports any regressions: health checks that went from PASS→FAIL, acceptance criteria that flipped

**Where it fits**: `/verify --regression poc_003_5` as a pre-PR check. Could become a required gate in `/pr`.

---

## 3. Run Comparison Skill (`/compare`)

**Problem**: No structured way to compare two runs. Currently requires reading two narrative reports and eyeballing.

**Solution**: New `/compare <run_a> <run_b>` skill that:
- Reads both `metrics.json` files
- Produces a delta table: Gini change, balance distribution shift, governance action distribution, proposal/decree/challenge counts
- Highlights significant changes (>20% shift in any metric)
- Shows side-by-side governance timelines (what rules were active and when)

**Output example**:
```
## Comparison: poc_003_5 vs poc_004

| Metric | poc_003_5 | poc_004 | Delta |
|--------|-----------|---------|-------|
| Final Gini | 0.12 | 0.31 | +158% |
| Total Pool | 26 | 18 | -31% |
| Proposals | 2 | 5 | +150% |
| Decrees | 0 | 3 | NEW |
| Parse Error Rate | 3.2% | 4.1% | +0.9pp |
```

---

## 4. Programmatic Acceptance Criteria

**Problem**: `/verify` step 7 has an LLM reading JSONL and making judgment calls about whether criteria are met. This works for PoC but introduces interpretation variance.

**Solution**: Formalize acceptance criteria as structured queries in task files:
```json
"acceptance_criteria": [
  {
    "description": "All agents > 0 credits at round 30",
    "query": "final_balances.all(v => v > 0)",
    "level": "minimum"
  },
  {
    "description": "At least one decree attempted",
    "query": "actions.filter(a => a.action == 'decree').length > 0",
    "level": "target"
  }
]
```

`/verify` evaluates these as data queries against `rounds.jsonl` — no LLM judgment required. Qualitative observations (like "non-democratic governance emerges") stay in directed findings, not acceptance criteria.

**Migration path**: Start by rewriting existing criteria in this format for poc_005. Backfill older runs if needed for the paper.

---

## 5. API Cost Tracking in Verification

**Problem**: `results.json` tracks API costs but `/verify` doesn't check them. A run costing 10x expected is a signal (infinite retries, prompt explosion, etc.).

**Solution**: Add a 6th health check:
- Read `results.json` or `metrics.json` for `api_cost`
- Compare against expected range based on `rounds * agents * avg_cost_per_call`
- WARN if >2x expected, FAIL if >5x expected

Low priority — costs have been stable across runs so far.

---

## Implementation Order

When ready to upgrade:
1. **Programmatic acceptance criteria** (highest leverage — improves every future run)
2. **Multi-run batches** (required for any publishable claim)
3. **Run comparison** (saves hours of manual analysis)
4. **Backward compatibility gate** (insurance policy, becomes more valuable as codebase grows)
5. **API cost tracking** (nice-to-have)

---

*Created: 2026-02-27*
*Context: Review of harness workflow after adding `/verify` skill*

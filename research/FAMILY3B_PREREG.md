# FAMILY 3B PRE-REGISTRATION — rotation breadth check (single confirmatory shot)

**Frozen:** 2026-08-15, before computation.

## Honesty header
Family 3 (rotation, 3 assets) was REJECTED at VALIDATION 2019-2022 (ledger 0010). This experiment draws on that SAME window a second time for the same mechanism family. That is a disclosed multiple-testing cost, mitigated as follows:
- **NO grid search. Exactly ONE pre-frozen configuration is run. Zero tuning.**
- The bar is raised: must beat BOTH passive benchmarks by Sharpe ≥ +0.3 (family 3 needed only >).
- Whatever the result, no further rotation variants will be tested on 2019-2022. This closes the mechanism either way.

## Rationale (why this isn't dredging)
Cross-sectional momentum is theoretically breadth-hungry: with 3 assets the "cross-section" is nearly a coin flip. The new validated universe (BTC, ETH, LTC, XRP, DOGE, ADA, BNB — 7 assets, all ≥2018 history) is a genuinely new input (reopening condition #3, ledger 0010), not a parameter tweak.

## The one configuration (frozen from family 3's already-frozen candidate)
- Universe: all 7 assets with data at each date (dynamic entry as histories begin)
- Rank by 30d return, rebalance every 10 days, hold TOP-2 equal-weight (top-1 of 7 would be concentration; top-2 is the pre-declared breadth analogue)
- Absolute-momentum cash gate ON, vol-target ON (30d, 0.6 per sleeve)
- Costs: 50 bps/side (75 for LTC/DOGE thin books), 10%/yr financing
- Window: 2019-01-01 → 2022-12-31; benchmarks: equal-weight B&H of the 7, vol-targeted EW control

## Verdict rule
PASS = all 5 standard checks AND Sharpe gap ≥ +0.3 vs BOTH benchmarks → then (and only then) plan the locked TEST shot.
FAIL = rotation mechanism closed permanently at daily granularity.

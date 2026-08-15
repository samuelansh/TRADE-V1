# DATA SPLIT POLICY (frozen 2026-08-15)

Chronological only (Master Prompt §7). BTC/USD priced data: 2010-07-18 → 2026-05-24.

| Segment | Range | Use |
|---|---|---|
| BURN-IN | 2010-07-18 → 2011-12-31 | indicator warm-up only; low-trust early data, never scored |
| TRAIN | 2012-01-01 → 2018-12-31 | hypothesis exploration, parameter regions |
| VALIDATION | 2019-01-01 → 2022-12-31 | model/rule selection, walk-forward tuning checks |
| **TEST (LOCKED)** | 2023-01-01 → 2026-05-24 | touched ONCE per frozen strategy, never optimized on |

Same boundaries for ETH (priced from 2015-07-30; its TRAIN is 2016-01-01 → 2018-12-31).

Rules:
1. No statistic from TEST may be looked at until a strategy is frozen and logged in the ledger.
2. A strategy gets ONE test-set evaluation. Modifying it afterwards = new strategy = new ledger entry, and the test result is tainted (flagged `REUSED_TEST` and discounted).
3. Multiple-testing count is tracked in the ledger: every configuration evaluated on VALIDATION increments the trial counter used for selection-bias haircuts.

# Ledger 0011 — Family 2R (mean reversion @ spot costs): REJECTED AT TRAIN

**Date:** 2026-08-15 · **Protocol:** `research/FAMILY2R_PREREG.md` · Table: `research/f2r_train_results.csv`.

## Question answered
Was family 2's death (ledger 0009) just the CFD cost structure? **No.**

## Result
Identical 52-config grid at 10 bps/side and 26 bps/side, zero financing:
- **0 / 52 pass the gate at either tier.** Best cell: Sharpe 0.78 (lowvol z=2.0 m=3) at 10 bps — still under the 0.8 bar, and a lone cell, not a region.
- Cost reduction from 50→10 bps lifted the best Sharpe only 0.58→0.78: the mechanism is weak, not merely cost-starved.

## Significance for the program conclusion
The null result of ledger 0010 is now **cost-robust**: daily-bar mean reversion fails even under the best realistic execution venue. Reopening condition #2 (spot costs) is hereby tested and CLOSED. Remaining reopening conditions: intraday data (#1), new asset classes (#3), accumulated forward data (#4).

## Trial accounting (cumulative program)
Structures searched: 220 (F1 120, F2 52, F3 48) + 0 new in F2R (cost re-pricing only, 104 re-runs disclosed). Validation shots: 2. Test shots: 1. Contaminated holdouts: none.

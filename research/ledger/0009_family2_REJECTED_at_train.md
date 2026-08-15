# Ledger 0009 — Family 2 (short-horizon mean reversion): REJECTED AT TRAIN

**Date:** 2026-08-15 · **Phase:** BASELINE · **Protocol:** `research/FAMILY2_PREREG.md` (frozen before computation) · Full table: `research/f2_train_results.csv`.

## Result
52 configs (z-score entries, n-down-day entries, low-vol regime filter) at cfd_stress 50 bps/side + 10%/yr financing, BTC TRAIN 2012-2018:
- **0 of 52 pass the pre-declared gate** (Sharpe > 0.8 AND positive return; gate required ≥4 adjacent passes).
- Best config: zscore k=3, z=2.5, m=5 → Sharpe 0.58. Whole regions are negative (ndown n=3 loses -79% total).
- The regime-filtered variant (panic-in-calm hypothesis) was no better (max Sharpe 0.57).

## Interpretation
- Costs did exactly what was predicted in the pre-registration: high-turnover MR on daily BTC bars cannot clear 50 bps/side + financing. Even the best cell earns ~1% per position-day *before* enough trades compound the costs.
- Note this gate was run on the SAME TRAIN window where TSMOM showed Sharpe 2+: the data supports trend persistence, not short-horizon reversal, at daily granularity. Consistent with the lag-1 autocorrelation (+0.02) from market discovery.
- VALIDATION and the ETH test market remain **untouched** by family 2 — the budget survives for family 3.

## Research Director — updated map
Tested & rejected: (1) daily trend/TSMOM — TEST fail; (2) daily mean reversion — TRAIN fail.
Remaining honest options at daily granularity are thin:
- **Cross-asset relative strength (BTC vs ETH vs LTC rotation)** — different mechanism (cross-sectional momentum), feasible with current data; family 3 candidate.
- Intraday mechanisms — BLOCKED on data (USER_TODO #2).
- Accepting the null: at daily bars + retail CFD costs, no deployable edge may exist for a single retail account. This remains the most probable end-state and saying so is part of the job.

## Trial accounting (cumulative)
F1: 120 TRAIN + 1 VAL + 1 TEST · F2: 52 TRAIN. Holdouts iterated: zero.

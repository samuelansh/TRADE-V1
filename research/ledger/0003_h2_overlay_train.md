# Ledger 0003 — H2 vol-target overlay, TRAIN only

**Date:** 2026-08-15 · **Phase:** BASELINE · **Data:** TRAIN only.
**Trials:** +90 configs (cumulative trials on TRAIN: 120). Full table `research/h2_train_results.csv`.

## Result (cfd_stress costs)
Overlay (weight = signal × min(1, tgt_vol/realized_vol)) improves Sharpe at EVERY lookback (e.g. lb=250: 2.61→2.88 median overlay) and cuts MaxDD (median -0.71→-0.54). Worst overlay config ≈ no-overlay reference → broad stable region across vol_win {20,30,60} × tgt_vol {0.4,0.6,0.8}.
Control: overlay on buy-and-hold improves little (1.74→1.78) → effect is not "vol-scaling helps anything long".

## Backtester validation (Backtest Auditor requirement)
`tests/test_backtest.py`: 5 known-outcome scenarios PASS (zero-weight, cost-of-entry, no-lookahead, cost-turnover scaling, long-only clip).

## Decision
H1+H2 family advances to VALIDATION under the pre-registered protocol in `research/VALIDATION_PREREG.md`. H3 (breakout) deprioritized: overlapping mechanism with H1; will only be tested if H1 fails validation. H4 unchanged (low prior).

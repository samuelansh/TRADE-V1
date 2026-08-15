# Ledger 0002 — H1 TSMOM baseline, TRAIN only (2012-2018)

**Date:** 2026-08-15 · **Phase:** BASELINE · **Data touched:** TRAIN only. VALIDATION/TEST untouched.
**Trials logged for multiple-testing count:** 10 lookbacks × 3 cost presets = 30 configurations (all on TRAIN; selection haircut applies when we move to VALIDATION).

## Setup
Long-only TSMOM: weight=1 if close > close[N days ago] else 0. Next-bar execution (no look-ahead). Costs per side: 10/25/50 bps. Benchmark: buy-and-hold with identical cost model. Engine: `src/backtest.py`; experiment: `src/experiment_h1_train.py`; full table: `research/h1_train_results.csv`.

## Results summary (stress costs, 50 bps/side)
- Buy-and-hold: Sharpe 1.74, MaxDD -85%
- TSMOM: Sharpe 1.64-2.61 across ALL 10 lookbacks; MaxDD -69% to -82%; broad region (no cliff between adjacent lookbacks); survives 50 bps stress with all lookbacks profitable.

## Skeptic notes (Master Prompt §13/§16 — impressive result ⇒ more suspicion)
1. **Era effect dominates:** 2012-2018 BTC rose ~700×. ANY long-biased rule looks brilliant. Sharpe 2+ here proves almost nothing by itself.
2. The honest comparison is *risk-adjusted vs benchmark*: TSMOM improves Sharpe and cuts drawdown vs B&H at most lookbacks — consistent with the known literature, not evidence of a novel edge.
3. Early-period data (2012-2013) is from thin markets; fills at reference price are optimistic there.
4. Real verdict comes from VALIDATION (2019-2022: includes a full bear market) — NOT run yet, deliberately.

## Decision
H1 passes the TRAIN sanity bar (broad stable region, cost-robust, beats benchmark risk-adjusted). Proceed next session to: H2 vol-targeting overlay on TRAIN, then a single pre-registered walk-forward pass onto VALIDATION for the surviving configuration family (lookback region 60-250, not a single N).

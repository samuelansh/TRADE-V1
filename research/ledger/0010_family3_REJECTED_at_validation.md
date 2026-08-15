# Ledger 0010 — Family 3 (cross-sectional rotation): REJECTED AT VALIDATION

**Date:** 2026-08-15 · **Protocol:** `research/FAMILY3_PREREG.md` (frozen first) · Scripts: `experiment_f3_train.py`, `experiment_f3_validation.py` · Tables: `f3_train_results.csv`.

## TRAIN (2016-2018, 48 configs)
Gate passed: 9/48 configs, including a 6-adjacent cluster at r=30 (Sharpe up to 3.8 vs EW-benchmark 2.44). Candidate frozen from region MEDIAN structure (r=30, b=10, cash-gate ON, vol-target ON) — not the best cell.

## VALIDATION (2019-2022) — one shot
| | Sharpe | AnnRet | MaxDD | TotRet |
|---|---|---|---|---|
| Strategy | 0.31 | 17.6% | -77.3% | 91% |
| EW buy&hold | 0.46 | 38.0% | -80.2% | 263% |
| EW vol-target control | **0.53** | 31.2% | -73.7% | 196% |

Checks: FAIL, FAIL, PASS, PASS, PASS → **VERDICT: FAIL.** No second attempt, no tweaks. Locked TEST never touched (stays clean).

## Interpretation
- TRAIN Sharpe 3.8 → VALIDATION 0.31: near-total decay. 2016-2018 cross-crypto rotation profits (mostly riding ETH/LTC alt-season) did not persist into 2019+. 2022 alone destroyed the strategy (-0.998 log return ≈ -63%) — rotation kept it in whatever was falling least-slowly while the cash gate lagged.
- Both failures of checks 1-2 are against *passive* references — the family didn't just underperform, it was worse than doing nothing intelligent.

## PROGRAM CONCLUSION — daily-bar crypto, retail conditions
Three mechanism families, all falsified under pre-registered protocols:
| Family | Mechanism | Died at | Ledger |
|---|---|---|---|
| 1 | Time-series trend + vol targeting | locked TEST | 0005 |
| 2 | Short-horizon mean reversion | TRAIN (0/52) | 0009 |
| 3 | Cross-sectional rotation | VALIDATION | 0010 |

**Formal null result:** with daily bars, long-only retail CFD cost structure (50 bps/side + financing), and the 2023+ regime, no deployable edge was found across the three major mechanism families. Evidence quality: high (no holdout contamination anywhere in the program; trial counts logged: 120+52+48 TRAIN configs, 2 validation shots, 1 test shot).

**This is the deliverable the Master Prompt defines as success:** the system determined, rigorously and cheaply, that these edges do not survive — before any money (even demo money) was risked. NO TRADE is the correct output.

## What could reopen research (all require new inputs)
1. Intraday data (USER_TODO #2) → different mechanism space (microstructure, session effects).
2. Lower cost structure (spot exchange API instead of CFDs) → re-test family 2 at 10 bps.
3. New asset classes with usable daily data.
4. Accumulating forward data: v1 paper trading continues; ETH/portfolio TEST windows remain virgin for any future family.

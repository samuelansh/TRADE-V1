# Ledger 0004 — Pre-registered VALIDATION pass (one shot)

**Date:** 2026-08-15 · **Phase:** VALIDATION · **Protocol:** `research/VALIDATION_PREREG.md` (frozen before data access) · **Runs:** exactly one per market, no iteration.

## BTC/USD 2019-2022, cfd_stress (50 bps/side)
| | Sharpe | AnnRet | MaxDD | TotRet |
|---|---|---|---|---|
| Strategy (ensemble+vol-target) | **0.94** | 37.7% | **-49.7%** | 260% |
| Buy & hold | 0.62 | 44.3% | -76.7% | 334% |
| Vol-target B&H (control) | 0.50 | 30.3% | -75.6% | 189% |

All 5 pre-declared checks **PASS** (incl. year-concentration; 2022 bear year: -28% log vs B&H's much deeper loss; MaxDD nearly 27 pts shallower).

## ETH/USD generalization (identical frozen params, zero tuning)
Strategy Sharpe 1.40 vs B&H 0.76; MaxDD -48.0% vs -79.4%. **Generalizes.**

## Statistical Evidence Auditor notes (uncertainty, not certainty)
- Only 4 calendar years; effectively ~2 independent bull/bear cycles. Sharpe estimates on 4y of autocorrelated daily data carry s.e. ≈ 0.5 — the B&H-vs-strategy gap (0.33) is NOT statistically decisive on its own. What supports it: consistency across 2 markets, 3 cost levels, TRAIN + VALIDATION, and the drawdown improvement (large, structural).
- 858 "trades" = daily fractional rebalances from vol scaling (turnover already fully cost-charged at 50 bps/side).
- Absolute return trails B&H in raging bulls (expected: strategy caps exposure). The claim is risk-adjusted improvement, nothing more.

## Verdict
Family **survives validation**. Per split policy, TEST (2023→2026-05) stays locked until the strategy implementation is frozen (risk engine + paper layer around it). Next phase per router: EXECUTION-side engineering (risk engine, paper simulator), then single TEST evaluation, then red-team of the software.

Cumulative trial count: 120 TRAIN configs + 1 pre-registered validation candidate. No validation-set iteration occurred.

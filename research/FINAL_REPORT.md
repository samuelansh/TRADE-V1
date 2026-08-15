# TRADE-V1 — RESEARCH PROGRAM REPORT (daily-bar crypto phase)

**Date:** 2026-08-15 · **Mode throughout:** research/paper only; no demo or live execution ever occurred.

## Executive summary
Under the governance package (Master Prompt + auditors), three strategy families were taken through pre-registered train/validation/test pipelines on 10-16 years of validated data. **All three were falsified.** The program's formal conclusion is a **null result**: no deployable edge at daily granularity under retail CFD costs was found. Per the prime directive, discovering this *before* risking capital is the system succeeding, not failing.

## What was tested and how it died
| # | Family | Best in-sample | Died at | Why |
|---|---|---|---|---|
| 1 | TSMOM trend + vol targeting | Sharpe 2.6 (TRAIN), passed 5-check VALIDATION | **Locked TEST 2023-26** | edge decayed; no timing skill left (signal-fwd corr ≈ 0; P(better than B&H)=32%) |
| 2 | Short-horizon mean reversion | Sharpe 0.58 | **TRAIN gate** (0/52) | costs+financing devour high turnover; daily BTC shows persistence, not reversal |
| 3 | BTC/ETH/LTC rotation | Sharpe 3.8 (TRAIN) | **VALIDATION** (0.31 vs 0.53 passive control) | 2016-18 alt-season profits didn't persist; 2022 fatal |

## Methodology integrity (the part that holds up regardless of results)
- Every holdout touched exactly once; zero tuning-after-seeing anywhere (ledgers 0002-0010).
- Pre-registration before every phase transition; kill criteria declared in advance; failures recorded verbatim.
- Backtester + risk engine + paper trader: 13 known-outcome and red-team tests, paper/vectorized consistency verified.
- Data: validated with manifests/hashes; one dataset (SOL) rejected; source-splice route with seam checks.
- Trial accounting: 220 train configs, 2 validation shots, 1 test shot — all logged for multiple-testing honesty.

## Standing assets
- Strategy-agnostic research/execution stack (`src/`): backtester (w/ financing costs), risk engine with kill-switches, paper trader, data pipelines.
- Untouched holdouts for any future family: ETH 2023-26, portfolio-level 2023-26.
- v1 forward paper experiment running (post-TEST bars only): currently -6.4% vs BTC -18.5%.

## Addendum (2026-08-15, same day): two reopening conditions already tested
- **Spot costs (family 2R, ledger 0011):** mean reversion re-priced at 10 and 26 bps/side, zero financing — still 0/52 configs pass (best Sharpe 0.78, lone cell). The mechanism is weak, not cost-starved. Condition CLOSED.
- **Wider universe (family 3B, ledger 0012):** rotation re-tested with 7 validated assets (added XRP/DOGE/ADA/BNB), one pre-frozen confirmatory config, raised bar — Sharpe 0.14 vs 0.94 passive. Breadth made it worse. Mechanism CLOSED permanently.

The null result is therefore robust to both cost structure and universe breadth. Remaining reopening conditions: intraday data, fundamentally new instruments, accumulated forward evidence.

## What would reopen research
1. **Intraday data** (user-provided bulk download) → microstructure/session mechanism space.
2. **Spot-exchange cost structure** (~10 bps) → family 2 becomes re-testable; needs exchange API access or user-run execution.
3. New instruments with long daily histories.

## Scope limitations (added after adversarial self-review, ledger 0014)
The null result applies to: LONG-ONLY strategies, DAILY bars, single-account retail cost structures, and a survivor-biased universe (coins alive in 2026 — note survivorship inflates backtests, so the null is conservative). Untested spaces: shorting, pairs/spreads, cross-exchange arbitrage, funding-rate carry, order-book signals, intraday mechanisms (now under study as Family 4).

## Recommendation to the user
Do not fund an MT5 demo for any current strategy — nothing earned it. If you want to continue: the highest-value contribution is bulk intraday data (USER_TODO #2). The second-best: accept the program's finding, keep the paper experiment running, and revisit quarterly as forward data accumulates.

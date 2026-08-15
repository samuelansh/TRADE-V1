# Ledger 0015 — Family 4 (intraday/candlestick): REJECTED AT TRAIN — all three sub-families

**Date:** 2026-08-15 · **Protocol:** `research/FAMILY4_PREREG.md` (frozen before computation) · Table: `research/f4_train_results.csv` · Data caveat: single-venue wicks (ledger 0014).

## Result (BTC 1h, TRAIN 2016-2020, judged at 26 bps/side; benchmark B&H Sharpe 1.64)

**4A — Candlestick patterns: 0/18 pass.** THE DEFINITIVE ANSWER TO THE OWNER'S QUESTION.
- Short holds (4h) after hammer/engulfing/doji: catastrophic — Sharpe -1.8 to -2.7, total ruin (-99%+) from costs on 3-6k signals.
- Only 24h holds go positive (best: doji/24h Sharpe 1.22) — but still under B&H (1.64), i.e. the "pattern" is just diluted market exposure. Requiring a downtrend context made everything WORSE.
- With 2,700-6,100 signal instances per pattern, sample size is NOT the issue. The patterns genuinely carry no exploitable information at hourly scale after fees.

**4B — Session/time-of-day: 0/10 pass.** All single-session exposures lose to costs (daily entry+exit × 26 bps compounds ruinously). The in-train-selected "best 8 hours of 2016-17" portfolio: Sharpe -2.0 out of those years — hour-of-day 'edges' are pure noise that inverts immediately.

**4C — Breakout + ATR stops: 0/12 pass.** Structural finding: stop-only variants degenerate into ~buy-and-hold (3-7 trades in 5 years, matching B&H exactly = breakouts recur before stops trigger). Timed exits create real trading and real losses vs B&H. At 10 bps some timed configs reach Sharpe 1.7-2.05 vs B&H 1.64 — marginal, non-adjacent, and evaporating at 26 bps. No stable region.

## Interpretation
Intraday long-only technical mechanisms on BTC: falsified at TRAIN under honest costs. The candlestick answer is now evidence-based, not literature-based: **patterns humans "see" in candles had no tradable edge across 93,822 hourly bars.** VALIDATION (2021-23) and TEST (2024-25) remain untouched.

## Path A feasibility (checked same session)
Kraken Futures public API serves hourly historical funding rates via the fetch route (verified: PF_XBTUSD, data from 2025-08 onward, ~1 year, 127 chunks). Bybit/Binance blocked. GitHub mirrors: none found. **Conclusion: funding-carry research is data-feasible but only with ~1 year of history** — enough for descriptive analysis (average carry level, sign persistence, crash behavior), NOT enough for a validated strategy pipeline. Framed accordingly in next steps.

## Trial accounting (cumulative)
F1 120 · F2 52 (+104 re-priced) · F3 48 · F3B 1 · F4 40. Validation shots 2, test shots 1. Contaminated holdouts: none.

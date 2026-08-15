# Ledger 0005 — LOCKED TEST evaluation: FAIL (candidate v1 rejected for demo)

**Date:** 2026-08-15 · **Phase:** FINAL VALIDATION · **One-shot rule respected:** this was the first and only touch of 2023→2026-05 data. TEST is now consumed for this strategy family; any modified variant evaluated on it will be flagged REUSED_TEST and discounted.

## Result (BTC/USD 2023-01-01 → 2026-05-24, cfd_stress)
| | Sharpe | AnnRet | MaxDD | TotRet |
|---|---|---|---|---|
| Strategy v1 | 1.05 | 36.6% | **-26.5%** | 188% |
| Buy & hold | **1.21** | 57.0% | -49.1% | 361% |
| Vol-target B&H | **1.23** | 56.3% | -49.1% | 355% |

Checks: 1 FAIL, 2 FAIL, 3 PASS, 4 PASS, 5 PASS → **VERDICT: FAIL** (criteria pre-declared in `VALIDATION_PREREG.md`; pass required all 5).

## Honest interpretation
- The strategy did what it was designed to do mechanically (cut drawdown roughly in half, stayed profitable, no year-concentration) but **did not beat passive exposure risk-adjusted** in 2023-2026.
- 2023-2026 was a persistent grind-up regime with shallower crashes than 2019-2022; trend filters mostly cost upside without earning their keep. The failure of check 2 is the sharpest signal: in this window even naive vol-scaling matched B&H — the TSMOM component added nothing.
- This is consistent with the prior stated in MARKET_DISCOVERY.md: daily-bar crypto momentum is heavily mined and its edge has plausibly decayed. The validation-period result (ledger 0004) was real but regime-dependent.
- Per the prime directive: **a strategy that fails robustness testing is a failure, and finding that out before demo/live money is a successful system behavior.**

## Risk-engine observation (separate, positive)
Paper replay over TEST with default limits: equity 10,000 → 20,891, then HALT on the 25% trailing-drawdown kill-switch (2025 drawdown), final weight 0. The safety wrapper works as designed — it stopped a strategy that had stopped working. The halt-no-resume behavior is confirmed in live-path code, not just tests.

## Decision
1. **Candidate v1 is REJECTED for MT5 demo deployment.** No parameter tweaks to "fix" the test result — that would be test-set mining.
2. Software stack (backtester, strategy interface, risk engine, paper trader, 13 passing tests) is retained — it is strategy-agnostic and validated.
3. Research returns to the hypothesis backlog. Honest options, in Research Director priority order:
   a. **H4 / different mechanism families** (mean reversion, regime filters) — new pre-registration; note TEST is consumed, so a future family needs either fresh out-of-time data (accumulating live via Kraken route) or ETH/LTC as untouched test markets under a new split policy.
   b. **Forward paper trading** of v1 with the risk engine, zero capital commitment, to gather true out-of-sample evidence at no cost.
   c. Accept the strongest surviving claim — vol-targeted exposure control cuts tail risk — and treat trading as risk management rather than alpha (defensible, modest).

## Trial accounting
TRAIN configs: 120 · VALIDATION evaluations: 1 (pass) · TEST evaluations: 1 (fail). No holdout iteration occurred at any stage.

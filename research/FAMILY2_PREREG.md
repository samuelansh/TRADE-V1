# FAMILY 2 PRE-REGISTRATION — short-horizon mean reversion (H4 lineage)

**Frozen:** 2026-08-15, before any family-2 computation.

## Data budget (BTC TEST is consumed — ledger 0005)
- TRAIN: BTC 2012-2018 · VALIDATION: BTC 2019-2022
- **LOCKED TEST: ETH 2023-01-01 → 2026-05-24** (never evaluated by anyone: family 1 touched ETH only on 2019-2022). One shot, all-must-pass, same discipline as before.
- BTC 2023+ may never be used for family-2 selection (tainted).

## Mechanism under test
After sharp short-term declines, part of the move is liquidation/panic flow, not information, and partially retraces within days.
- Entry signal: z-score of k-day return vs rolling history below -z (k ∈ {1,2,3}), or n consecutive down days
- Exit: fixed holding m ∈ {1,2,3,5} days
- Regime filter variant: signal only active when 30d realized vol < its rolling median (panic-in-calm-market hypothesis)

## Cost realism (corrective action #4 from ledger 0006)
All judged at cfd_stress 50 bps/side PLUS overnight financing 10%/yr on held notional (long CFD financing). MR is high-turnover: costs are expected to be the killer — that is precisely what we're testing.

## Kill criteria (pre-declared)
- TRAIN gate: after stressed costs+financing, positive expectancy AND Sharpe > 0.8 across a contiguous parameter region (≥4 adjacent configs), else family REJECTED at TRAIN (no validation touch).
- VALIDATION gate (only if TRAIN passes): same 5-check protocol as family 1 vs buy-and-hold benchmarks.
- Trial budget: ≤ 60 TRAIN configs, logged.

## Expectation (honest prior)
P(family survives to demo) is LOW (~10-15%). The purpose is cheap, clean falsification; a well-documented negative result is a success of the process.

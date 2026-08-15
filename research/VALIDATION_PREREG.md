# PRE-REGISTERED VALIDATION PROTOCOL — frozen BEFORE any VALIDATION data access

**Frozen:** 2026-08-15, prior to reading any post-2019 returns. One shot; no iteration on VALIDATION results is permitted for this family. If it fails, the family is rejected (back to hypothesis backlog, new ledger entry).

## Candidate (fixed now, no tuning later)
To avoid selecting a single lucky parameter, the candidate is the **equal-weight ensemble** across the stable region found on TRAIN:
- Signal: TSMOM long-only, lookbacks {60, 90, 120, 180, 250}, each contributing weight 1/5
- Overlay: vol targeting with vol_win=30d, tgt_vol=0.6 (median of the stable grid — NOT the best cell)
- Final weight = (mean of 5 binary signals) × min(1, 0.6/realized_vol30), capped at 1, long-only
- Costs: cfd_stress 50 bps/side (primary judgment), cfd_base 25 bps reported alongside
- Execution: next-bar close, engine `src/backtest.py` @ commit of this file

## Evaluation window
VALIDATION = 2019-01-01 → 2022-12-31 (includes 2022 bear). Burn-in from pre-2019 data for indicators only.

## Pre-declared PASS criteria (all must hold, cfd_stress)
1. Sharpe(strategy) > Sharpe(buy-and-hold) on VALIDATION
2. Sharpe(strategy) > Sharpe(vol-targeted buy-and-hold, same overlay params) — controls for "overlay alone"
3. MaxDD(strategy) shallower than MaxDD(buy-and-hold)
4. Positive total return after costs
5. No single calendar year contributes >80% of total log-return (concentration check)

## Pre-declared reporting (whatever the outcome)
- Yearly breakdown, trade count, turnover, exposure
- Result recorded in ledger regardless of pass/fail; failed = family rejected, no re-tries with "small tweaks"

## Multiple-testing context (honesty note)
~120 configurations were examined on TRAIN before this pre-registration. The ensemble-over-region choice mitigates but does not eliminate selection effects; the LOCKED TEST set (2023→) remains the final arbiter and is still untouched.

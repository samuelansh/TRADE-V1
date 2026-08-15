# Ledger 0012 — Family 3B (7-asset rotation, confirmatory shot): REJECTED

**Date:** 2026-08-15 · **Protocol:** `research/FAMILY3B_PREREG.md` — ONE pre-frozen config, zero tuning, raised bar, disclosed second use of the 2019-2022 window.

## New data validated first
XRP (11.8y), DOGE (12.3y), ADA (8.5y), BNB (8.9y) daily — all pass integrity checks (1 interior null each, trimmed leading nulls). Universe expanded 3 → 7 assets.

## Result (2019-2022, stressed costs)
| | Sharpe | AnnRet | MaxDD | TotRet |
|---|---|---|---|---|
| Top-2-of-7 rotation (frozen cfg) | 0.14 | 6.6% | -68.0% | 29% |
| EW buy&hold (7 assets) | **0.94** | 81.5% | -79.5% | 985% |
| EW vol-target control | 0.69 | 38.5% | -68.2% | 268% |

3 of 6 checks failed, including both benchmark comparisons by huge margins. **Breadth made it WORSE, not better** (3-asset version scored 0.31). Chasing 30d winners among alts was systematically buying tops through 2019-2022.

## Mechanism status
**Cross-sectional rotation at daily bars: CLOSED PERMANENTLY** (as pre-declared, regardless of direction of failure). No further variants will be evaluated on any historical window.

## Program status after today
Mechanisms tested and closed: trend (TEST-fail), mean reversion (TRAIN-fail at CFD AND spot costs), cross-sectional rotation (VALIDATION-fail ×2, incl. breadth). The daily-bar null result now covers every family feasible with available data, at both realistic cost structures, with expanded universe. Reopening requires: intraday data, or fundamentally new instruments, or accumulated forward evidence.

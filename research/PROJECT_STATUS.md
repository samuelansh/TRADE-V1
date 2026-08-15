# PROJECT STATUS

**Updated:** 2026-08-15 · **Active mode:** RESEARCH (no execution of any kind yet)

| Component | State |
|---|---|
| Environment | ✅ Audited (see `BOOT_01_ENVIRONMENT_AUDIT.md`) — Linux sandbox, Python 3.11, 2 CPU / 3.8 GB RAM |
| Skills | ✅ Master Prompt + Router. Phase history: DISCOVERY → BASELINE → VALIDATION → EXECUTION-safety → FINAL REVIEW (TEST). Auditors used per phase: Backtest, Overfitting/Multiple-Testing, Statistical Evidence, Red Team, Execution Safety, Self-Evaluation. |
| Tools | ✅ Git/GitHub, PyPI, page-fetch (Kraken data route). ❌ No broker, no MT5 terminal here. |
| Data | ✅ Acquired + validated (BTC 15.8y, ETH 10.8y, LTC 13.1y daily; gold/S&P monthly). SOL REJECTED (99.7% nulls). Manifest with hashes: `data/MANIFEST.json`. Kraken live-update route verified. |
| Markets | ✅ Ranked (`research/MARKET_DISCOVERY.md`): BTC/USD primary, ETH/USD generalization check, LTC held out, gold/S&P context only |
| Strategies | 🔴 Candidate v1 (TSMOM ensemble × vol-target) **REJECTED at locked TEST** (ledger 0005): Sharpe 1.05 vs B&H 1.21 on 2023-2026. Drawdown halved, but pre-declared criteria required beating passive — it didn't. No tweaking-to-pass allowed; TEST consumed. |
| Backtester | ✅ v1 validated (5 known-outcome tests) |
| Risk Engine | ✅ Built + red-teamed (`src/risk_engine.py`): daily-loss/drawdown/equity kill-switches (halt, no silent resume), stale-data + abnormal-move NO TRADE, weight clipping, error→NO TRADE. Confirmed live in paper replay (halted correctly in 2025 drawdown). |
| Portfolio Engine | ⬜ UNNECESSARY (single instrument; no strategy approved) |
| ML | 🚫 GATED (no surviving baseline to beat) |
| MT5 | ⏸️ Execution layer NOT built — no strategy is approved for demo, so building it now would be waste. Stack is ready to wrap a future approved strategy. |
| Demo | 🔴 BLOCKED by ledger 0005 rejection (correct behavior, not a bug) |
| Monitoring | 🟡 Trade journal CSV via paper trader; sufficient for paper mode |

**Current hypothesis:** none surviving. Family 4 (intraday: candle patterns 4A, sessions 4B, breakout 4C) REJECTED AT TRAIN — 0/40 configs (ledger 0015). The candlestick question is now answered with evidence: no edge after costs, 93,822 bars, thousands of pattern instances.
**Current experiment:** v1 forward paper (neutral reporting). Funding-carry study COMPLETE (ledger 0016): mechanism REAL (+6.3%/yr gross, 77% positive hours) but NO-GO — nets ~+5.2%/yr vs the pre-registered 8% bar. Correctly priced, not exploitable at current levels.
**Current strategy version:** none approved.
**Known failures/closures:** ledgers 0005-0016. Seven mechanism families tested end-to-end (trend, mean reversion ×2 cost regimes, rotation ×2 universes, candlesticks, sessions, breakouts, funding carry), zero survivors, all pre-registered.
**Current blockers:** research exhausted within reachable data/mechanisms. Reopens on: sustained funding spike >15-20%/yr (one API call to check), new user data, or new instruments.
**Highest-value next action:** owner's call. (Guardian bot rejected by owner 2026-08-15.) Machine idles honestly rather than mining noise.
**Self-evaluation:** ledger 0006 — overall 6.5/10; methodology strong (9), breadth thin (5), execution readiness low (4, deliberately). All 4 corrective actions tracked; 3 of 4 closed same-day.

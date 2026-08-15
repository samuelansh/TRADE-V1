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

**Current hypothesis:** none active. Family 1 (trend) rejected at TEST (0005); **family 2 (mean reversion) rejected at TRAIN (0009): 0/52 configs survive stressed costs+financing** — validation/test budgets preserved.
**Current experiment:** v1 forward paper collection continues (0008): -6.4% vs BTC -18.5% since 2026-05-25.
**Current strategy version:** none approved. v1 paper-only.
**Known failures:** SOL dataset; validator null bug (fixed); F1 TEST FAIL (0005/0007); F2 TRAIN FAIL (0009).
**Current blockers:** intraday mechanisms need bulk data from user (USER_TODO #2); everything else unblocked.
**Highest-value next action:** family 3 candidate = cross-sectional BTC/ETH/LTC relative-strength rotation (last untested mechanism family feasible with current data). Honest alternative if it fails: accept the null — daily bars + retail costs may hold no deployable edge, and reporting that is a valid project outcome.
**Self-evaluation:** ledger 0006 — overall 6.5/10; methodology strong (9), breadth thin (5), execution readiness low (4, deliberately). All 4 corrective actions tracked; 3 of 4 closed same-day.

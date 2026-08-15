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

**Current hypothesis:** none active. H1+H2 family rejected at TEST (ledger 0005) despite passing pre-registered VALIDATION (ledger 0004) — regime-dependent edge, decayed post-2022.
**Current experiment:** none. Research Director options listed in ledger 0005 §Decision.
**Current strategy version:** v1 REJECTED for deployment. Software stack (backtester+strategy interface+risk engine+paper trader, 13 tests passing) retained, strategy-agnostic.
**Known failures:** SOL dataset (nulls); validator null-check bug (fixed); **candidate v1 failed locked TEST — recorded, not hidden, not tuned around**.
**Current blockers:** none for research; MT5 items (`USER_TODO.md`) moot until a strategy survives a full pipeline.
**Highest-value next action (Research Director):** start forward paper trading of v1 via Kraken route (free out-of-sample evidence, zero risk) while pre-registering the next hypothesis family (mean-reversion/regime filters) with ETH as the untouched test market under a new split policy.

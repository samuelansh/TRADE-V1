# PROJECT STATUS

**Updated:** 2026-08-15 · **Active mode:** RESEARCH (no execution of any kind yet)

| Component | State |
|---|---|
| Environment | ✅ Audited (see `BOOT_01_ENVIRONMENT_AUDIT.md`) — Linux sandbox, Python 3.11, 2 CPU / 3.8 GB RAM |
| Skills | ✅ Loaded: Master Prompt + Research Router. Phase = DISCOVERY → active skills: Research Director, Source Verification, Data Integrity, Strategy Research. All other auditors NOT ACTIVE yet (router anti-rigidity rule). |
| Tools | ✅ Git/GitHub, PyPI, page-fetch (Kraken data route). ❌ No broker, no MT5 terminal here. |
| Data | ✅ Acquired + validated (BTC 15.8y, ETH 10.8y, LTC 13.1y daily; gold/S&P monthly). SOL REJECTED (99.7% nulls). Manifest with hashes: `data/MANIFEST.json`. Kraken live-update route verified. |
| Markets | ✅ Ranked (`research/MARKET_DISCOVERY.md`): BTC/USD primary, ETH/USD generalization check, LTC held out, gold/S&P context only |
| Strategies | 🟢 H1+H2 ensemble PASSED pre-registered VALIDATION (ledger 0004): BTC Sharpe 0.94 vs B&H 0.62, MaxDD -50% vs -77% @ stressed costs; generalizes to ETH untuned (1.40 vs 0.76). TEST still locked. |
| Backtester | ✅ v1 `src/backtest.py` + 5 known-outcome validation tests (`tests/test_backtest.py`) all passing |
| Risk Engine | ⬜ NOT BUILT |
| Portfolio Engine | ⬜ NOT BUILT — likely UNNECESSARY until >1 instrument survives validation |
| ML | 🚫 GATED — no baseline exists, so ML is not permitted yet |
| MT5 | ❌ MISSING in this environment — deliverable-only (code for user's own Windows/VPS demo account) |
| Demo | ❌ Not reachable from sandbox — internal PAPER simulator is the ceiling here |
| Monitoring | ⬜ NOT BUILT |

**Current hypothesis:** H1+H2 (TSMOM ensemble {60..250} × vol-target 30d/0.6) — survived pre-registered VALIDATION on BTC and untuned ETH.
**Current experiment:** validation complete (ledgers 0003, 0004). Next phase: EXECUTION engineering.
**Current strategy version:** candidate v1 (params frozen in `research/VALIDATION_PREREG.md`); not yet TEST-evaluated.
**Known failures:** SOL dataset rejected; validator null-check bug (fixed); Sharpe gap on 4y not statistically decisive alone (see ledger 0004 uncertainty notes).
**Current blockers:** broker specs + MT5 machine needed only for DEMO phase — `research/USER_TODO.md`.
**Highest-value next action:** build independent risk engine + paper-trading layer around frozen candidate → single locked TEST evaluation → software red-team → MT5 deliverable package.

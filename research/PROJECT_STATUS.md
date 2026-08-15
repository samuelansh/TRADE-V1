# PROJECT STATUS

**Updated:** 2026-08-15 · **Active mode:** RESEARCH (no execution of any kind yet)

| Component | State |
|---|---|
| Environment | ✅ Audited (see `BOOT_01_ENVIRONMENT_AUDIT.md`) — Linux sandbox, Python 3.11, 2 CPU / 3.8 GB RAM |
| Skills | ✅ Loaded: Master Prompt + Research Router. Phase = DISCOVERY → active skills: Research Director, Source Verification, Data Integrity, Strategy Research. All other auditors NOT ACTIVE yet (router anti-rigidity rule). |
| Tools | ✅ Git/GitHub, PyPI, page-fetch (Kraken data route). ❌ No broker, no MT5 terminal here. |
| Data | ✅ Acquired + validated (BTC 15.8y, ETH 10.8y, LTC 13.1y daily; gold/S&P monthly). SOL REJECTED (99.7% nulls). Manifest with hashes: `data/MANIFEST.json`. Kraken live-update route verified. |
| Markets | ✅ Ranked (`research/MARKET_DISCOVERY.md`): BTC/USD primary, ETH/USD generalization check, LTC held out, gold/S&P context only |
| Strategies | 🟡 H1 TSMOM baseline run on TRAIN only (ledger 0002). Hypotheses pre-registered: `research/HYPOTHESIS_BACKLOG.md`. Split policy frozen: `research/DATA_SPLIT_POLICY.md`. |
| Backtester | ✅ v1 `src/backtest.py` — next-bar execution, per-side cost presets 10/25/50 bps. Event-driven upgrade later if intraday data arrives. |
| Risk Engine | ⬜ NOT BUILT |
| Portfolio Engine | ⬜ NOT BUILT — likely UNNECESSARY until >1 instrument survives validation |
| ML | 🚫 GATED — no baseline exists, so ML is not permitted yet |
| MT5 | ❌ MISSING in this environment — deliverable-only (code for user's own Windows/VPS demo account) |
| Demo | ❌ Not reachable from sandbox — internal PAPER simulator is the ceiling here |
| Monitoring | ⬜ NOT BUILT |

**Current hypothesis:** H1 TSMOM (BTC daily) — passed TRAIN sanity bar; VALIDATION not yet touched.
**Current experiment:** next = H2 vol-targeting overlay on TRAIN, then pre-registered walk-forward onto VALIDATION.
**Current strategy version:** none frozen.
**Known failures:** SOL dataset rejected (nulls); validator initially let it pass (fixed); Binance/Yahoo/Stooq/Drive blocked (worked around).
**Current blockers:** none for research. MT5/broker items need the user — see `research/USER_TODO.md`.
**Highest-value next action:** H2 overlay on TRAIN → single walk-forward pass to VALIDATION for the 60-250 lookback family → red-team + multiple-testing haircut before any TEST touch.

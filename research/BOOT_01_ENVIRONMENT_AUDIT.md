# BOOT 01 — ENVIRONMENT AUDIT

**Date:** 2026-08-15 · **Mode:** RESEARCH (no execution) · **Status:** COMPLETE
**Rule applied:** *Do not claim a capability until verified.* Every item below was tested with a real command/request, not assumed.

---

## 1. Compute & OS

| Item | Status | Evidence |
|---|---|---|
| OS | **AVAILABLE** | Debian GNU/Linux 12 (bookworm), x86_64, kernel 6.1 |
| CPU | **AVAILABLE (limited)** | 2 cores |
| RAM | **AVAILABLE (limited)** | 3.8 GiB total |
| Disk | **AVAILABLE** | ~20 GiB free |
| GPU | **MISSING** | none — deep learning impractical; fine for rules/stats/tree models |
| Background processes | **AVAILABLE** | sandbox supports long-running processes |

**Implication:** compute is enough for vectorized backtesting of daily/hourly bars and classical ML. Not enough for large tick datasets or neural network training. This aligns with the prompt's "simple models first" directive anyway.

## 2. Languages & Packages

| Item | Status | Evidence |
|---|---|---|
| Python 3.11.2 + pip | **AVAILABLE** | verified |
| PyPI access | **AVAILABLE** | pandas 3.0.5, numpy 2.4.6, scipy, scikit-learn, statsmodels, matplotlib installed and imported successfully |
| Node.js 22 / npm | **AVAILABLE** | verified (not needed yet) |
| torch / tensorflow | **UNNECESSARY** (installable but no GPU; blocked by ML Gate anyway) |
| Git / GitHub (`git`, `gh`) | **AVAILABLE** | repo cloned, remote reachable, API 200 |

## 3. Network & Data Sources — the critical constraint

The sandbox has an **HTTP allowlist**. Verified results:

| Source | Direct from sandbox | Via page-fetch tool | Verdict |
|---|---|---|---|
| GitHub (clone, raw via redirect, API) | ✅ 200 | ✅ | **AVAILABLE** — primary bulk-data channel |
| PyPI | ✅ 200 | — | **AVAILABLE** |
| Kraken public API (OHLC, trades) | ❌ blocked | ✅ **real JSON returned** (BTC/USD daily OHLC verified) | **PARTIAL** — works through fetch tool; ~720 candles per timeframe per request |
| Binance API / binance.vision | ❌ blocked | ❌ geo-restricted (451-style refusal) | **MISSING** |
| Yahoo Finance | ❌ blocked | untested reliability | **PARTIAL at best** |
| Stooq | ❌ blocked | ❌ "Access denied" | **MISSING** |
| CryptoCompare | ❌ | ❌ API key required | **MISSING** |
| CoinGecko | ❌ blocked | untested | **UNKNOWN** |
| Google Drive | ❌ blocked | ❌ | **MISSING** |

**Verified data routes, in order of preference:**
1. **GitHub-hosted datasets** (git clone) — long daily histories: S&P 500 (1871→, verified 1,868 rows), gold, FX daily repos, BTC daily history repos. Bulk, reproducible, versionable.
2. **Kraken public API via fetch tool** — live/recent crypto OHLC, any interval, ~720 bars per call (≈2 years of daily, ≈30 days of hourly). Good for recent data + keeping datasets current.
3. **User-supplied files** — via GitHub branch upload (proven working this session).

## 4. Broker / Execution

| Item | Status | Notes |
|---|---|---|
| MetaTrader 5 terminal | **MISSING** | MT5 is a Windows application; this is a headless Linux sandbox. The official `MetaTrader5` Python package only works alongside a running Windows terminal. |
| MT5 Python integration | **MISSING** (here) | Can be *coded and tested with a mock*, then handed to the user to run on their own Windows/VPS machine with a demo account. |
| Broker demo API (REST) | **MISSING** | typical broker API hosts are not on the allowlist |
| Paper trading (internal simulator) | **AVAILABLE** | we can build our own paper-execution layer fed by Kraken data via the fetch tool |

**Honest consequence:** in this environment the achievable execution ladder is
**BACKTEST → PAPER (internal simulator)** here, and **DEMO (MT5)** only as *deliverable code the user runs on their own machine*. I will not pretend otherwise.

## 5. AI / Tooling

| Item | Status |
|---|---|
| Web search & page fetching | **AVAILABLE** (for research & the Kraken data route) |
| Skill package (70+ files) | **AVAILABLE** — extracted at `FINAL_TRADING_AI_COMPLETE_TEXT_PACKAGE/` |
| Scheduling / cron across sessions | **PARTIAL** — processes live only while the sandbox lives |

---

## Summary box

```
AVAILABLE   : Python scientific stack, Git/GitHub, GitHub datasets,
              Kraken public data (via fetch tool), internal backtest/paper engines,
              2 CPU / 3.8 GB RAM / 20 GB disk
PARTIAL     : intraday data depth (~720 bars/interval from Kraken),
              scheduling persistence
MISSING     : MT5 terminal, broker connectivity, Binance/Yahoo/Stooq,
              GPU, Google Drive
UNNECESSARY : deep learning frameworks (blocked by ML gate until justified),
              RL (blocked by RL gate), Node.js (for now)
```

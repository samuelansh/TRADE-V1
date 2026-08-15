# Ledger 0013 — INTRADAY DATA ACQUIRED SELF-SERVICE · PROGRAM REOPENED

**Date:** 2026-08-15 · **Phase:** DISCOVERY (new cycle)

## How it was obtained (user asked: "can't you download resources yourself?")
Searched GitHub (the one bulk channel available to the sandbox). Routes tried and failed honestly: LFS-hosted dataset (content server blocked from sandbox; fetch tool can read it but 2,048 chunks is impractical), Actions-workflow downloader (App lacks `workflows` permission), Bitfinex API direct (blocked). **Success:** `Julian-Andres-Thomas/BTC-USD` — plain CSV in-repo, cloned directly.

## Dataset: `data/raw/btc_1h_bitstamp.csv` (committed as .gz, 2.1 MB)
- **93,822 hourly OHLCV candles, 2015-01-01 → 2025-09-14** (~10.7 years)
- Provenance: Bitstamp exchange (minute data → 1h), via Kaggle mczielinski, cleaned upstream
- Validation run TODAY: 0 duplicates, monotonic, 0 nulls, 0 nonpositive prices, **0 OHLC-consistency violations** (High/Low bound checks), 1 gap (19h), 1 hourly move >20% (max 22.8% — plausible for 2015-era BTC)
- **Cross-source check** against our validated CoinMetrics daily closes: median divergence 0.42%, max 2.1% (different exchanges; acceptable)

## What this changes
Reopening condition #1 from ledger 0010 is now MET. New research space, previously untestable:
- True candlestick anatomy (wicks, bodies, gaps) — the user's explicit interest
- Time-of-day / session effects (Asia/EU/US hours)
- Intraday breakout/reversal with proper H/L data
- 24× more observations per year than daily bars (~8,760 vs 365)

## Constraints to respect in the next pre-registration
- Single exchange (Bitstamp) — findings need robustness framing
- Ends 2025-09-14: leaves 2024-09→2025-09 as a natural final holdout, and our live Kraken route can extend forward
- 2 CPU sandbox: hourly grid searches are ~100k-row vectorized ops — fine
- Multiple-testing discipline unchanged: pre-registered families, budgeted trials, one-shot holdouts

## Next step
Pre-register FAMILY 4: candlestick/intraday mechanisms on 1h bars, with split policy frozen BEFORE any exploration of the new file beyond the integrity checks above.

# Ledger 0001 — Data pipeline + market discovery

**Date:** 2026-08-15 · **Phase:** DISCOVERY

## What was done
- Acquired datasets (GitHub route): coinmetrics daily BTC/ETH/LTC/SOL, datasets/gold-prices monthly, datasets/s-and-p-500 monthly. Verified Kraken OHLC live route for future updates (`src/kraken_fetch.py` converts saved responses).
- Built `src/validate_data.py`: timestamps, monotonicity, duplicates, gaps, null prices, extreme returns → `data/MANIFEST.json` with sha256 + source pins.

## Findings / failures (recorded, not hidden)
- **SOL dataset REJECTED**: coinmetrics `ReferenceRateUSD` null for 2228/2235 rows (only 7 priced days). File deleted; validator now enforces `priced_rows >= 500` and `null_price_ratio <= 5%`.
- Validator originally passed SOL (bug: counted nulls but didn't fail on them) — fixed. Lesson: validation checks must have teeth, not just print counts.
- LTC has a 204% daily move (2013-era illiquidity); early LTC data flagged low-trust.
- BTC leading nulls 2009-01..2010-07 are legitimate (no market existed); validator trims leading nulls, judges priced segment.

## Decision
BTC/USD daily = primary market; ETH/USD = generalization check; LTC held out; gold/S&P monthly = context only. Rationale in `research/MARKET_DISCOVERY.md`.

## Next
Data split policy → hypothesis backlog → baseline (rules) strategies → realistic-cost backtester.

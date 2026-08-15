# MARKET DISCOVERY & RANKING

**Date:** 2026-08-15 · Stats computed by `src/market_discovery.py` from validated datasets (see `data/MANIFEST.json`). Numbers in `research/market_stats.csv`.

## Candidates considered
Constraint applied first: we can only research markets we have **verified data + a verified update route** for. That eliminates Forex intraday, individual stocks, futures, and commodities intraday for now (sources blocked — see BOOT_01). Remaining candidates:

| Market | Daily data | Live updates | Ann. vol | Trade hours | Costs (typical retail) |
|---|---|---|---|---|---|
| BTC/USD | 15.8y ✅ | Kraken route ✅ | 90% | 24/7 | spread ~1-5 bps spot; higher as CFD |
| ETH/USD | 10.8y ✅ | Kraken route ✅ | 102% | 24/7 | similar |
| LTC/USD | 13.1y ✅ | Kraken route ✅ | 120% | 24/7 | wider spread, thinner book |
| Gold | monthly only ❌ | none | 10% | sessioned | n/a at monthly granularity |
| S&P 500 | monthly only ❌ | none | 14% | sessioned | n/a at monthly granularity |

## Ranking

1. **BTC/USD — primary research market.**
   - Longest usable history (5,788 daily returns), highest liquidity of any crypto pair, tightest spreads, 24/7 (no session/gap modeling needed), updateable via verified Kraken route, available as CFD on most MT5 brokers for the eventual demo phase.
   - Slight positive lag-1 autocorrelation (+0.02) vs negative for ETH/LTC — weak but consistent with the momentum/trend literature on BTC.
2. **ETH/USD — secondary / cross-validation market.** 10.8y of data; use to test whether any BTC edge generalizes (robustness requirement §14), not as an independent strategy target initially.
3. **LTC/USD — held out.** Thinner market, wildest tails (-90% day, 2011 era data quality suspect: a 204% daily move passed basic validation but is from the illiquid early period). Usable only as an additional generalization check on post-2017 data.
4. **Gold / S&P 500 — rejected for trading research.** Monthly granularity produces ~20-60 signals per decade — statistically hopeless for validating an edge. Kept only as context/benchmark data.

## Honest caveats
- Daily-bar crypto is one of the most heavily mined markets in existence; prior probability of finding a *new* edge is low. The realistic goal is testing whether **known, published effect families (trend/momentum/vol-scaling)** survive realistic costs out-of-sample — not discovering something novel.
- All three crypto series are **spot reference prices**, not the broker feed we would eventually trade on MT5 (CFD spreads are wider). Cost stress tests must use pessimistic spreads (item 4 in `USER_TODO.md`).
- No intraday data yet → research is restricted to daily-bar strategies (holding periods of days-weeks). This is also the right fit for 2-CPU compute.

## Decision
**Proceed with BTC/USD daily as primary, ETH/USD as generalization check.**
Next: chronological data split policy + hypothesis backlog (documented before any strategy code), then baseline strategies + realistic backtester.

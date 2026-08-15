# NOT DONE — needs YOU (do later)

Things I cannot do from this sandbox. Nothing here blocks current research work.

1. **MT5 demo account + Windows/VPS machine** — needed only at the EXECUTION phase.
   - Create a demo account with any MT5 broker (e.g. ICMarkets, Pepperstone, FTMO-style broker).
   - Have a Windows machine or Windows VPS where MT5 terminal + Python 3.11 can run.
   - I will hand you a ready execution package (`MetaTrader5` Python code) to run there.

2. **Intraday historical data (if we go below 1h timeframe)** — Kraken via my fetch route only gives ~720 bars per interval (~30 days of 1h).
   - If validation demands years of 1h/15m data: download it yourself (e.g. Binance Data portal https://data.binance.vision, or Kraken CSV export https://support.kraken.com OHLCVT files) and push the ZIP/CSV to a branch of this repo (the `By-the-user` method — it worked).

3. **API keys (optional, only if we need a richer data source)** — e.g. free CryptoCompare/CoinDesk key, Alpha Vantage key, or Polygon.io key. Not required yet.

4. **Broker choice constraints** — tell me later: which broker/symbols your MT5 demo actually offers (crypto CFDs? gold? indices?), and its typical spread/commission. Needed before the execution layer is finalized, because cost assumptions in backtests must match your broker.

5. **Decision checkpoint (later, after validation results exist)** — you approve/reject moving a frozen strategy from PAPER to your MT5 DEMO.

# DONE / IN PROGRESS — mine
- [x] BOOT 01 environment audit
- [x] Project scaffolding + status board
- [ ] Data pipeline (acquire, validate, version) — in progress
- [ ] Market discovery & ranking
- [ ] Hypothesis backlog → baseline strategies → realistic backtester → validation

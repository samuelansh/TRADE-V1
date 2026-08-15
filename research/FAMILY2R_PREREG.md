# FAMILY 2R PRE-REGISTRATION — mean reversion re-test at SPOT costs

**Frozen:** 2026-08-15, before computation. Reopening condition #2 from ledger 0010 exercised: family 2 died at TRAIN under CFD costs (50 bps + financing). Question: does the mechanism survive at SPOT-exchange costs? This matters because execution on a spot exchange (e.g. Kraken, taker fee ~0.25%→~10-26 bps with volume, no overnight financing) is a realistic alternative to MT5 CFDs and is the venue our data actually comes from.

## Cost model
- 10 bps/side, zero financing (long spot, no leverage) — optimistic spot tier
- 26 bps/side sensitivity (Kraken starter taker tier) — must ALSO pass for deployment-grade verdict

## Data budget
- Same TRAIN (BTC 2012-2018) — TRAIN is exploratory budget, reuse disclosed; this is a cost-model change, not a new mechanism search.
- Same config grid as family 2 (52 configs, unchanged — no new degrees of freedom).
- TRAIN gate unchanged: Sharpe > 0.8 AND positive, ≥4 adjacent configs, at BOTH cost tiers.
- If TRAIN passes → single VALIDATION shot (BTC 2019-2022, 5-check protocol vs B&H).
- **ETH 2023-26 TEST remains locked** for the final shot if validation passes.

## Trial accounting note
Grid identical to family 2 (already logged 52). New evaluations: same 52 at 2 new cost levels = disclosed as 104 additional backtest runs but ZERO new strategy structures.

## Prior
Mechanism showed max Sharpe 0.58 at 50 bps. Removing ~40 bps/side on ~50-300 round trips over 7 years could plausibly add 0.3-0.8 Sharpe to high-turnover cells. P(TRAIN pass) ~25%; P(survive through validation) ~8%.

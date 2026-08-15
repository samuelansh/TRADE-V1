# HYPOTHESIS BACKLOG (pre-registered before any strategy code)

Prioritized by Expected Information Gain × Impact × Feasibility. Daily bars, close-only data → holding periods days-weeks. Each entry follows Master Prompt §8 format.

## H1 — Time-series momentum / trend following on BTC (PRIORITY 1)
- **Hypothesis:** BTC daily returns exhibit medium-term (2-12 week) positive serial dependence exploitable long-only.
- **Mechanism:** herding + slow capital diffusion + reflexive adoption cycles; documented in academic literature (Moskowitz et al. TSMOM; multiple crypto replications).
- **Data:** BTC daily close (have). 
- **Expected failure:** post-2021 institutionalization may have arbitraged it away; fails in ranging regimes.
- **Cost sensitivity:** low turnover (~5-30 trades/yr) → robust to spread. Must survive 2× pessimistic CFD costs.
- **Falsification:** VALIDATION Sharpe ≤ buy-and-hold's with same vol, or negative expectancy after stressed costs, across the stable parameter region.

## H2 — Volatility-targeted position sizing overlay (PRIORITY 2)
- **Hypothesis:** scaling exposure inverse to trailing volatility improves risk-adjusted return vs fixed size (vol clustering is the best-documented crypto regularity).
- **Mechanism:** volatility persistence (GARCH-type clustering); crashes cluster in high-vol states.
- **Falsification:** no drawdown/Sharpe improvement over H1 baseline on VALIDATION.

## H3 — Breakout (Donchian-style) entries (PRIORITY 3)
- **Hypothesis:** N-day-high breakouts carry positive drift for days-weeks after.
- **Mechanism:** same trend mechanism as H1, different trigger; stop-driven feedback.
- **Falsification:** underperforms H1 on VALIDATION with overlapping exposure (then it adds nothing — drop, don't stack).

## H4 — Short-term mean reversion (PRIORITY 4, low prior)
- **Hypothesis:** 1-3 day reversals after large down moves in low-vol regimes.
- **Expected failure:** high turnover → cost-fragile; likely dies at realistic spread. Test mainly to document the negative result.

## Explicitly NOT pursued now
- ML/RL/LLM signals (gated: no baseline exists yet)
- Intraday anything (no data)
- Cross-market signals from monthly gold/S&P (granularity mismatch)
- Short selling (spot data; CFD short financing costs unknown until broker info arrives — USER_TODO #4)

**Benchmark for everything: buy-and-hold BTC, and vol-matched buy-and-hold.** A "strategy" that loses to its own passive benchmark is dead regardless of its absolute numbers.

# FAMILY 4 PRE-REGISTRATION — candlestick & intraday mechanisms (1h bars)

**Frozen:** 2026-08-15, before ANY strategy computation on the hourly file (only integrity checks performed so far — ledger 0013).

## Split policy (chronological, frozen)
| Segment | Range | Use |
|---|---|---|
| BURN-IN | 2015-01-01 → 2015-12-31 | warm-up only |
| TRAIN | 2016-01-01 → 2020-12-31 | exploration |
| VALIDATION | 2021-01-01 → 2023-12-31 | one pre-registered shot |
| **TEST (LOCKED)** | 2024-01-01 → 2025-09-14 | one shot, only for a validation survivor |

## Mechanisms (three sub-families, budgets fixed)
**4A — Classic candlestick patterns (the user's question, answered properly)** · ≤24 configs
Patterns coded objectively: hammer, shooting star, bullish/bearish engulfing, doji-reversal. Hold {4, 12, 24} bars after signal. Long-only entries for bullish patterns; bearish patterns tested as EXIT/avoid filters (no shorting).
**4B — Time-of-day / session effects** · ≤16 configs
Hour-of-day and day-of-week return structure; session-conditional exposure (e.g. hold only during specific sessions). Selection on TRAIN, judged out-of-sample.
**4C — Intraday range breakout (uses true H/L)** · ≤24 configs
N-bar high breakout entries with ATR-scaled stops; N ∈ {24, 72, 168}, stop {1, 2}×ATR(24), hold-to-stop vs timed exit.

Total budget: 64 configs. No additions after seeing results.

## Costs
Spot model (venue-matched: Bitstamp/Kraken): 10 bps/side primary + 26 bps stress. No financing (spot, long-only, no leverage). Hourly turnover makes costs bite harder — that's realistic and intended.

## Gates
- TRAIN gate per sub-family: after 26 bps stress, Sharpe > 1.0 across ≥4 adjacent configs AND beats buy-and-hold Sharpe on TRAIN. Sub-families failing at TRAIN die there.
- VALIDATION: standard 5-check protocol vs B&H + vol-targeted B&H, single shot for at most ONE frozen candidate per surviving sub-family.
- TEST: single shot, raised bar (gap ≥ +0.2), only if validation passes.

## Prior (honest)
4A: literature says classic patterns carry ~no edge after costs — P(survive) <10%; the value is answering the question definitively for the user.
4B: session effects are real in FX/equities; crypto is 24/7 so weaker prior — P ~15%.
4C: intraday breakout is trend's cousin; family 1 died but hourly granularity + real stops is a different animal — P ~15%.

# Ledger 0016 — Funding carry study: mechanism REAL but NO-GO at current levels

**Date:** 2026-08-15 · **Protocol:** `FUNDING_CARRY_STUDY_PREREG.md` (frozen first) · Script: `src/study_funding_carry.py` · Data: `data/raw/funding_btc_sampled.csv` (Kraken Futures PF_XBTUSD, 9 systematic windows Aug-2025→Aug-2026, 157 obs — sampling disclosed in script header).

## The pre-declared answers
1. **Gross carry: +6.3%/yr** average (short-perp receives). Range across windows: -3.0% (Apr-26) to +14.6% (Aug-25). Funding is real, mostly positive, regime-dependent.
2. **Sign persistence: 77% of hours positive; 8/9 windows positive.** The mechanism works as the textbooks say.
3. **Tail bound: worst sampled window ≈ -0.25% per 30d** — mild (but sampled, not exhaustive; a true crash week could be worse).
4. **Net after costs: +5.2%/yr at 12-month hold** (round-trip on both legs eats 1%/yr; shorter holds get eaten alive: 3-month hold nets just +2.1%).
5. **Go/no-go: NO-GO.** Net +5.2% fails the pre-registered bar of risk-free+3pp (8%). One check of three failed; criteria are criteria.

## Honest interpretation
- The carry trade WORKS mechanically — it's the first mechanism we've studied where the income is structural rather than predictive. But at 2025-26 funding levels it pays roughly **what a US treasury pays, plus ~0-1pp**, for meaningfully more operational risk (exchange risk, margin management on the short leg, negative-funding stretches like Apr-2026).
- In 2021-era bull manias funding averaged 20-40%/yr and this trade printed money. Today's calmer market has compressed it. The mechanism isn't dead — it's **correctly priced**, which is what efficient-ish markets do.
- No strategy will be built on this at current levels. The study cost nothing and closes the question with numbers instead of vibes.

## Program state after this
Mechanisms now tested end-to-end: trend, mean reversion (2 cost regimes), rotation (2 universes), candlesticks, sessions, breakouts, funding carry. **Seven mechanism families, zero survivors, every verdict pre-registered.** This is a complete, honest research record.

## Standing recommendation
Monitor, don't trade: if funding levels ever spike back above ~15-20%/yr sustained (visible in one API call), the carry question reopens with a real edge margin. Until then: forward paper accumulation and whatever new inputs arrive.

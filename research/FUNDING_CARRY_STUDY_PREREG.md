# FUNDING CARRY — DESCRIPTIVE STUDY PRE-REGISTRATION

**Frozen:** 2026-08-15, before downloading beyond the 1 feasibility page.

## Type of study (honest framing)
DESCRIPTIVE, not a strategy validation. ~1 year of data cannot feed our
train/validation/test pipeline. Output = measured facts + a go/no-go on
continuing to collect data forward. No trading decision may cite this study
as validation evidence.

## Mechanism under study
Perpetual futures funding: longs pay shorts when relativeFundingRate > 0.
The delta-neutral harvest ("cash-and-carry"): long spot BTC + short equal
notional PF_XBTUSD perp → price risk ≈ 0, collect funding when positive.
Yield source: leverage demand, not prediction.

## Data
Kraken Futures public API `/api/v4/historicalfundingrates?symbol=PF_XBTUSD`
(hourly relativeFundingRate). Also ETH (PF_ETHUSD) if reachable. Full
available history (~Aug 2025 → Aug 2026) via paged fetch-tool reads.

## Pre-declared questions (all answered regardless of what they show)
1. Gross annualized carry: mean funding × 8760, full period + monthly.
2. Sign persistence: % hours positive; longest negative streak (hours).
3. Tail risk: worst 1-day and worst 30-day cumulative funding.
4. Net yield after realistic costs: entry/exit both legs (4×26 bps round
   trip total, amortized over holding period), assume no basis P&L.
5. Comparison: net yield vs ~5% USD risk-free. Carry must beat it to matter.

## Pre-declared go/no-go
GO (continue collecting data monthly toward a future validated family) if:
net carry > risk-free + 3pp AND positive-funding hours > 65% AND worst
30-day cumulative funding > -1%.
NO-GO otherwise: mechanism documented and shelved.

## Known limitations (stated up front)
- 1 venue, 1 year, likely bull-period biased (funding is regime-dependent).
- Ignores basis convergence P&L, margin calls on the short leg during
  spikes, and borrow limits. A real implementation needs all three studied.
- Kraken Futures may not be accessible to the owner's jurisdiction/age —
  this is research about the mechanism, not a deployment plan.

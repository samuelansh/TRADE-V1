# FAMILY 3 PRE-REGISTRATION — cross-sectional relative-strength rotation

**Frozen:** 2026-08-15, before any family-3 computation.

## Mechanism under test
Cross-sectional momentum: capital rotates between crypto assets; the recent
relative winner among BTC/ETH/LTC continues to outperform the others for
weeks. Distinct from family 1 (time-series trend on one asset) — here the
bet is RELATIVE, always/mostly invested in the strongest asset, with a cash
fallback only when everything is in drawdown.

## Universe & data budget
- Universe: BTC, ETH, LTC daily USD (validated datasets).
- TRAIN: 2016-01-01 → 2018-12-31 (first year all three assets are liquid).
- VALIDATION: 2019-01-01 → 2022-12-31.
- **LOCKED TEST: 2023-01-01 → 2026-05-24 on the PORTFOLIO level.**
  Honesty note: family 1 consumed BTC 2023-26 as a single-asset test and its
  post-mortem analyzed it; ETH 2023-26 is untouched. The portfolio test is
  therefore *partially* informed for the BTC leg. This is disclosed, and the
  pass bar is raised (below) to compensate.

## Strategy space (≤48 TRAIN configs, logged)
- Rank assets by r-day return, r ∈ {30, 60, 90, 120}.
- Hold top-1 asset, rebalanced every b days, b ∈ {5, 10, 20}.
- Cash rule variants: (a) none — always hold top-1; (b) hold cash when the
  top asset's own r-day return < 0 (absolute-momentum gate).
- Sizing variants: full weight 1.0, or vol-targeted (30d, tgt 0.6).
- 4 × 3 × 2 × 2 = 48 configs.

## Costs
cfd_stress 50 bps/side + 10%/yr financing. LTC realism penalty: 75 bps/side
on any LTC entry/exit (thinner book).

## Gates (pre-declared)
- TRAIN gate: Sharpe > 1.0 AND beats equal-weight buy-and-hold portfolio
  (same costs) on Sharpe AND MaxDD, across ≥6 adjacent configs.
- VALIDATION gate: the 5-check protocol vs equal-weight B&H benchmark +
  vol-targeted equal-weight control.
- TEST gate (one shot, raised bar due to partial BTC contamination):
  ALL validation checks PLUS Sharpe gap vs equal-weight B&H ≥ +0.2.
- Trial budget: 48. No config added after seeing results.

## Prior
P(survive to demo) ~10%. Cross-sectional crypto momentum is heavily
documented pre-2021; decay risk mirrors family 1. Cheap falsification is
the goal; a null here closes the daily-bar research program (see ledger
0009 options map).

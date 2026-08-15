# Ledger 0007 — Post-mortem of v1 TEST failure

**Date:** 2026-08-15 · Analysis of already-consumed TEST data (failure analysis, not tuning; any idea born here must prove itself on other markets/future data). Script: `src/analysis_test_postmortem.py`.

## Findings
1. **Regime attribution:** strategy beat B&H in the trending half of TEST (+1.42 vs +1.03 log-ret) but bled badly in the choppy half (-0.36 vs +0.50). Classic TSMOM failure mode: chop whipsaws.
2. **No timing skill remained:** ensemble signal vs 5-day-forward return correlation on TEST = **+0.019 ≈ 0**.
3. **How decisive was the FAIL:** moving-block bootstrap 90% CI on the Sharpe gap (strat − B&H) = **[-0.53, +0.35], P(gap>0) = 32%**. The point estimate favors B&H; the CI shows v1 was never demonstrably better — the VALIDATION pass was within noise + regime luck.
4. **The "surviving claim" also weakened:** vol-target overlay alone vs B&H on TEST: gap CI [-0.03, +0.04], P>0 = 62% — i.e. **neutral**. On 2023-26, vol-targeting neither helped nor hurt (its MaxDD was identical to B&H at -49%). The drawdown halving of v1 came from trend exits, which also destroyed the upside. Option (c) from ledger 0005 is therefore DOWNGRADED: vol-targeting's tail-risk benefit is regime-dependent too.

## Updated beliefs (Research Director)
- Daily-bar BTC long-only trend: no deployable edge at retail costs, 2023+. Confidence: moderate-high.
- Any next family needs a *different mechanism*, not a trend variant. And expectations must be modest: the honest prior is that most families will fail; the pipeline exists to prove failure cheaply.

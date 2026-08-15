# Ledger 0008 — Forward paper trading started + update pipeline live

**Date:** 2026-08-15 · **Phase:** PAPER (v1, zero capital) · Scripts: `src/update_pipeline.py`, `src/paper_forward.py`.

## Pipeline
- Kraken daily closes (fetched 2026-08-15) spliced onto history: seam clean (hist ends 05-23, updates start 05-24, no gap, no divergence check needed — zero overlap), 5,872 rows through **2026-08-14**. Splice aborts on >2% overlap divergence or >3-day seam hole.
- Forward window starts **2026-05-25** — strictly after the consumed TEST window; no optimization ever saw these bars.

## First forward reading (82 bars, 2026-05-25 → 2026-08-14)
- BTC buy & hold: **-18.5%** (June crash ~77k → ~61k, partial recovery, August fade)
- Paper v1 (risk engine active): **-6.4%**, currently flat (weight 0), not halted, avg weight 0.06 — trend signals died early in the drop and kept it mostly out.
- Read honestly: ONE quarter, ONE regime (a crash — TSMOM's favorable case). This is consistent with "cuts tail risk" and says nothing about the failure mode TEST exposed (chop). Keep collecting; re-run `update_pipeline.py` + `paper_forward.py` whenever new Kraken data is appended.

## Self-evaluation follow-through (ledger 0006 corrective actions)
1. Bootstrap CIs — DONE (ledger 0007): the FAIL was fair; v1 was never demonstrably better (P(gap>0)=32%).
2. Regime post-mortem — DONE (ledger 0007): loss concentrated in chop; signal-forward-return corr ≈ 0 on TEST.
3. Kraken route end-to-end — DONE (this ledger).
4. Financing-cost stress in next pre-registration — PENDING (next family).

## Next research step (needs fresh session budget)
Pre-register hypothesis family 2 (short-horizon mean reversion / regime-filtered variants, H4 lineage) with: BTC TRAIN/VAL only, **ETH as untouched test market**, financing-cost stress included, expectation-managed (most families should fail; cheap falsification is the goal).

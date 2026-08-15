"""Post-mortem of v1's TEST failure (allowed: TEST is already consumed for
this family; this is failure analysis, not tuning — any NEW strategy ideas
arising here must be validated on other markets/future data, never on this
window again).

Questions:
1. WHERE did TSMOM lose vs passive: which regimes (trend vs chop)?
2. Did the vol-target overlay (the surviving claim) add value on TEST alone?
3. Bootstrap CI on the Sharpe gap: how decisive was the FAIL?
"""
from pathlib import Path

import numpy as np
import pandas as pd

import backtest
import strategy

ROOT = Path(__file__).resolve().parents[1]
TEST_START, TEST_END = "2023-01-01", "2026-05-24"


def load():
    df = pd.read_csv(ROOT / "data" / "raw" / "btc.csv")
    s = pd.Series(pd.to_numeric(df["PriceUSD"], errors="coerce").values,
                  index=pd.to_datetime(df["time"])).dropna()
    return s[s > 0]


def main():
    close = load()
    seg = pd.concat([close.loc[:TEST_START].tail(strategy.MIN_HISTORY + 40),
                     close.loc[TEST_START:TEST_END]])
    seg = seg[~seg.index.duplicated()]
    bps = backtest.COST_PRESETS_BPS["cfd_stress"]

    w_strat = strategy.target_weight_series(seg)
    rv = seg.pct_change().rolling(30).std() * np.sqrt(365)
    w_vt = (0.6 / rv).clip(upper=1.0).fillna(0.0)

    r_strat = backtest.run(seg, w_strat, bps).equity.loc[TEST_START:].pct_change().dropna()
    r_bh = backtest.run(seg, pd.Series(1.0, index=seg.index), bps).equity.loc[TEST_START:].pct_change().dropna()
    r_vt = backtest.run(seg, w_vt, bps).equity.loc[TEST_START:].pct_change().dropna()

    # 1. regime attribution: trending vs choppy months (|90d net move| / gross)
    ret = seg.pct_change()
    trendiness = ret.rolling(90).sum().abs() / ret.abs().rolling(90).sum()
    trending = (trendiness.loc[r_strat.index] > trendiness.loc[r_strat.index].median())
    for name, r in [("strategy", r_strat), ("buy_hold", r_bh)]:
        lt = np.log1p(r[trending]).sum()
        lc = np.log1p(r[~trending]).sum()
        print(f"{name:9s} log-ret trending-half={lt:+.3f} choppy-half={lc:+.3f}")

    # 2. ensemble signal usefulness on TEST: avg weight when subsequently up vs down
    fwd5 = seg.pct_change(5).shift(-5).loc[r_strat.index]
    sig = (w_strat.loc[r_strat.index])
    ic = sig.corr(fwd5)
    print(f"\nsignal->5d-forward-return correlation on TEST: {ic:+.4f} (≈0 ⇒ no timing skill)")

    # 3. moving-block bootstrap of Sharpe gap (strategy - buy&hold)
    rng = np.random.default_rng(42)
    n, block = len(r_strat), 20
    gaps = []
    idx = np.arange(n)
    for _ in range(2000):
        starts = rng.integers(0, n - block, size=n // block + 1)
        take = np.concatenate([idx[s:s + block] for s in starts])[:n]
        rs, rb = r_strat.values[take], r_bh.values[take]
        sh_s = rs.mean() / rs.std() * np.sqrt(365)
        sh_b = rb.mean() / rb.std() * np.sqrt(365)
        gaps.append(sh_s - sh_b)
    gaps = np.array(gaps)
    lo, hi = np.percentile(gaps, [5, 95])
    print(f"Sharpe gap (strat-B&H) bootstrap 90% CI: [{lo:+.2f}, {hi:+.2f}], "
          f"P(gap>0)={np.mean(gaps > 0):.2%}")

    # bonus: same CI for the VT overlay alone vs B&H
    gaps2 = []
    for _ in range(2000):
        starts = rng.integers(0, n - block, size=n // block + 1)
        take = np.concatenate([idx[s:s + block] for s in starts])[:n]
        rs, rb = r_vt.values[take], r_bh.values[take]
        gaps2.append(rs.mean() / rs.std() * np.sqrt(365) - rb.mean() / rb.std() * np.sqrt(365))
    lo2, hi2 = np.percentile(gaps2, [5, 95])
    print(f"VT-overlay-only gap 90% CI:              [{lo2:+.2f}, {hi2:+.2f}], "
          f"P(gap>0)={np.mean(np.array(gaps2) > 0):.2%}")


if __name__ == "__main__":
    main()

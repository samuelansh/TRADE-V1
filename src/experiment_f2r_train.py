"""FAMILY 2R — mean reversion re-test at SPOT costs (10 and 26 bps, no
financing). Pre-registered: research/FAMILY2R_PREREG.md.
Identical 52-config grid to family 2 — only the cost model changes.
Gate: Sharpe>0.8 AND positive at BOTH tiers, >=4 adjacent configs.
"""
from pathlib import Path

import numpy as np
import pandas as pd

import backtest
from experiment_f2_train import (load_btc, hold_weight, train_stats,
                                 TRAIN_START, TRAIN_END, BURN_IN)

ROOT = Path(__file__).resolve().parents[1]


def all_weights(seg):
    """Reproduce the exact family-2 grid (52 configs)."""
    ret = seg.pct_change()
    out = []
    for k in [1, 2, 3]:
        rk = seg.pct_change(k)
        z = (rk - rk.rolling(90).mean()) / rk.rolling(90).std()
        for zt in [1.5, 2.0, 2.5]:
            entry = (z < -zt).astype(float)
            for m in [1, 2, 3, 5]:
                out.append((f"zscore k={k} z={zt} m={m}",
                            hold_weight(entry, m)))
    down = (ret < 0).astype(int)
    for n in [3, 4, 5]:
        streak = down.rolling(n).sum()
        entry = (streak == n).astype(float)
        for m in [1, 2, 3, 5]:
            out.append((f"ndown n={n} m={m}", hold_weight(entry, m)))
    rv = ret.rolling(30).std() * np.sqrt(365)
    lowvol = (rv < rv.rolling(180).median()).astype(float)
    r1 = seg.pct_change(1)
    z1 = (r1 - r1.rolling(90).mean()) / r1.rolling(90).std()
    for zt in [1.5, 2.0]:
        for m in [1, 3]:
            entry = ((z1 < -zt) & (lowvol > 0)).astype(float)
            out.append((f"lowvol z={zt} m={m}", hold_weight(entry, m)))
    return out


def main():
    close = load_btc()
    seg = pd.concat([close.loc[:TRAIN_START].tail(BURN_IN),
                     close.loc[TRAIN_START:TRAIN_END]])
    seg = seg[~seg.index.duplicated()]
    grid = all_weights(seg)
    rows = []
    for name, w in grid:
        r10 = train_stats(backtest.run(seg, w, 10.0, financing_annual=0.0))
        r26 = train_stats(backtest.run(seg, w, 26.0, financing_annual=0.0))
        rows.append({"config": name,
                     "sharpe10": r10["sharpe"], "ret10": r10["total_return"],
                     "sharpe26": r26["sharpe"], "ret26": r26["total_return"],
                     "dd10": r10["max_drawdown"], "trades": r10["trades"]})
    df = pd.DataFrame(rows)
    df.to_csv(ROOT / "research" / "f2r_train_results.csv", index=False)
    gate = (df.sharpe10 > 0.8) & (df.ret10 > 0) & \
           (df.sharpe26 > 0.8) & (df.ret26 > 0)
    print(df.sort_values("sharpe26", ascending=False).head(15).to_string(index=False))
    print(f"\npassing gate at BOTH tiers: {gate.sum()} / {len(df)} (need >=4 adjacent)")
    if gate.any():
        print(df[gate].to_string(index=False))
    print("TRAIN GATE:", "check adjacency" if gate.sum() >= 4 else
          "FAIL — family 2R rejected at TRAIN")


if __name__ == "__main__":
    main()

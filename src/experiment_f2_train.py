"""FAMILY 2 — short-horizon mean reversion. TRAIN only (BTC 2012-2018).

Pre-registered in research/FAMILY2_PREREG.md. Costs: cfd_stress 50 bps/side
+ 10%/yr financing on held notional.

Configs (<=60 budget):
  A) z-score entry: k in {1,2,3} x z in {1.5, 2.0, 2.5} x hold m in {1,2,3,5} = 36
  B) n-down-days entry: n in {3,4,5} x hold m in {1,2,3,5}                    = 12
  C) regime-filtered best-structure subset: z(k=1) x {1.5,2.0} x m {1,3} x
     low-vol filter                                                           = 4
  Total = 52 (logged).
TRAIN gate: Sharpe > 0.8 AND positive expectancy after costs across >=4
adjacent configs, else family rejected without touching VALIDATION.
"""
from pathlib import Path

import numpy as np
import pandas as pd

import backtest

ROOT = Path(__file__).resolve().parents[1]
TRAIN_START, TRAIN_END = "2012-01-01", "2018-12-31"
BURN_IN = 400
BPS = backtest.COST_PRESETS_BPS["cfd_stress"]
FIN = 0.10


def load_btc():
    df = pd.read_csv(ROOT / "data" / "raw" / "btc.csv")
    s = pd.Series(pd.to_numeric(df["PriceUSD"], errors="coerce").values,
                  index=pd.to_datetime(df["time"])).dropna()
    return s[s > 0]


def hold_weight(entry: pd.Series, m: int) -> pd.Series:
    """weight 1 for m bars after each entry signal (overlapping entries extend)."""
    w = entry.astype(float)
    for i in range(1, m):
        w = np.maximum(w, entry.shift(i).fillna(0.0))
    return pd.Series(w, index=entry.index)


def train_stats(res):
    eq = res.equity.loc[TRAIN_START:]
    r = eq.pct_change().dropna()
    st = backtest.compute_stats(r, eq / eq.iloc[0], 365)
    st["trades"] = res.trades
    # expectancy per trade-day in position
    days_in = int((res.weights.loc[TRAIN_START:] > 0).sum())
    st["days_in_pos"] = days_in
    st["ret_per_pos_day"] = round(
        (eq.iloc[-1] / eq.iloc[0]) ** (1 / max(days_in, 1)) - 1, 6)
    return st


def main():
    close = load_btc()
    seg = pd.concat([close.loc[:TRAIN_START].tail(BURN_IN),
                     close.loc[TRAIN_START:TRAIN_END]])
    seg = seg[~seg.index.duplicated()]
    ret = seg.pct_change()

    rows = []
    # A) z-score entries
    for k in [1, 2, 3]:
        rk = seg.pct_change(k)
        z = (rk - rk.rolling(90).mean()) / rk.rolling(90).std()
        for zt in [1.5, 2.0, 2.5]:
            entry = (z < -zt).astype(float)
            for m in [1, 2, 3, 5]:
                w = hold_weight(entry, m)
                st = train_stats(backtest.run(seg, w, BPS, financing_annual=FIN))
                st.update(variant="zscore", k=k, z=zt, m=m, filt="none")
                rows.append(st)
    # B) consecutive down days
    down = (ret < 0).astype(int)
    for n in [3, 4, 5]:
        streak = down.rolling(n).sum()
        entry = (streak == n).astype(float)
        for m in [1, 2, 3, 5]:
            w = hold_weight(entry, m)
            st = train_stats(backtest.run(seg, w, BPS, financing_annual=FIN))
            st.update(variant="ndown", k=n, z=None, m=m, filt="none")
            rows.append(st)
    # C) low-vol regime filter on zscore k=1
    rv = ret.rolling(30).std() * np.sqrt(365)
    lowvol = (rv < rv.rolling(180).median()).astype(float)
    r1 = seg.pct_change(1)
    z1 = (r1 - r1.rolling(90).mean()) / r1.rolling(90).std()
    for zt in [1.5, 2.0]:
        for m in [1, 3]:
            entry = ((z1 < -zt) & (lowvol > 0)).astype(float)
            w = hold_weight(entry, m)
            st = train_stats(backtest.run(seg, w, BPS, financing_annual=FIN))
            st.update(variant="zscore_lowvol", k=1, z=zt, m=m, filt="lowvol")
            rows.append(st)

    df = pd.DataFrame(rows)[["variant", "k", "z", "m", "filt", "sharpe",
                             "ann_return", "max_drawdown", "total_return",
                             "trades", "days_in_pos", "ret_per_pos_day"]]
    df.to_csv(ROOT / "research" / "f2_train_results.csv", index=False)
    print(df.to_string(index=False))
    n_pass = (df.sharpe > 0.8) & (df.total_return > 0)
    print(f"\nconfigs: {len(df)} | passing Sharpe>0.8 & positive: {n_pass.sum()}")
    print("TRAIN GATE:", "PASS (region check needed)" if n_pass.sum() >= 4
          else "FAIL — family rejected at TRAIN")


if __name__ == "__main__":
    main()

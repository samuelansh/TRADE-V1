"""Generalization check (pre-declared in MARKET_DISCOVERY.md): identical
frozen candidate applied to ETH/USD on the VALIDATION window. No tuning.
"""
from pathlib import Path

import numpy as np
import pandas as pd

import backtest

ROOT = Path(__file__).resolve().parents[1]
VAL_START, VAL_END = "2019-01-01", "2022-12-31"
BURN_IN_DAYS = 400
LOOKBACKS = [60, 90, 120, 180, 250]
VOL_WIN, TGT_VOL = 30, 0.6


def load(fname, pcol):
    df = pd.read_csv(ROOT / "data" / "raw" / fname)
    s = pd.Series(pd.to_numeric(df[pcol], errors="coerce").values,
                  index=pd.to_datetime(df["time"])).dropna()
    return s[s > 0]


def main():
    close = load("eth.csv", "PriceUSD")
    pre = close.loc[:VAL_START].tail(BURN_IN_DAYS)
    seg = pd.concat([pre, close.loc[VAL_START:VAL_END]])
    ret = seg.pct_change()
    rv = ret.rolling(VOL_WIN).std() * np.sqrt(365)
    scale = (TGT_VOL / rv).clip(upper=1.0).fillna(0.0)
    ens = sum((seg > seg.shift(lb)).astype(float) for lb in LOOKBACKS) / len(LOOKBACKS)

    bps = backtest.COST_PRESETS_BPS["cfd_stress"]
    for name, w in [("strategy", (ens * scale).clip(0, 1)),
                    ("buy_hold", pd.Series(1.0, index=seg.index))]:
        res = backtest.run(seg, w, bps)
        eq = res.equity.loc[VAL_START:VAL_END]
        r = eq.pct_change().dropna()
        st = backtest.compute_stats(r, eq / eq.iloc[0], 365)
        print(f"ETH [{name:9s}] Sharpe={st['sharpe']:6.3f} AnnRet={st['ann_return']:7.2%} "
              f"MaxDD={st['max_drawdown']:7.2%} TotRet={st['total_return']:8.2%}")


if __name__ == "__main__":
    main()

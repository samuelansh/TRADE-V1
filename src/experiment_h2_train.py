"""H2 — volatility-targeted sizing overlay on H1 TSMOM. TRAIN only (2012-2018).

weight = tsmom_signal * min(1, target_vol / realized_vol)
Long-only, capped at 1 (no leverage). Compared against H1 binary weights with
identical costs. Also runs the overlay on buy-and-hold to separate "overlay
helps trend signal" from "overlay helps anything long".
Trials logged: lookbacks {60,90,120,180,250} x vol windows {20,30,60} x
target vols {0.4,0.6,0.8} x 2 base signals x 1 cost preset (cfd_stress) = 90.
"""
from pathlib import Path

import numpy as np
import pandas as pd

import backtest

ROOT = Path(__file__).resolve().parents[1]
TRAIN_START, TRAIN_END = "2012-01-01", "2018-12-31"
BURN_IN_DAYS = 400
COST = "cfd_stress"  # judge under stress only; easier presets already known


def load_btc():
    df = pd.read_csv(ROOT / "data" / "raw" / "btc.csv")
    s = pd.Series(pd.to_numeric(df["PriceUSD"], errors="coerce").values,
                  index=pd.to_datetime(df["time"])).dropna()
    return s[s > 0]


def train_stats(res):
    eq = res.equity.loc[TRAIN_START:]
    r = eq.pct_change().dropna()
    st = backtest.compute_stats(r, eq / eq.iloc[0], 365)
    st["trades"] = res.trades
    st["turnover"] = round(res.turnover, 1)
    return st


def main():
    close = load_btc()
    pre = close.loc[:TRAIN_START].tail(BURN_IN_DAYS)
    seg = pd.concat([pre, close.loc[TRAIN_START:TRAIN_END]])
    ret = seg.pct_change()
    bps = backtest.COST_PRESETS_BPS[COST]

    rows = []
    for base_name, base in [("tsmom", None), ("buy_hold", None)]:
        for lb in ([60, 90, 120, 180, 250] if base_name == "tsmom" else [None]):
            sig = ((seg > seg.shift(lb)).astype(float) if base_name == "tsmom"
                   else pd.Series(1.0, index=seg.index))
            # reference: no overlay
            r0 = train_stats(backtest.run(seg, sig, bps))
            r0.update(base=base_name, lookback=lb, vol_win=None, tgt_vol=None)
            rows.append(r0)
            for vw in [20, 30, 60]:
                rv = ret.rolling(vw).std() * np.sqrt(365)
                for tv in [0.4, 0.6, 0.8]:
                    scale = (tv / rv).clip(upper=1.0).fillna(0.0)
                    w = sig * scale
                    st = train_stats(backtest.run(seg, w, bps))
                    st.update(base=base_name, lookback=lb, vol_win=vw, tgt_vol=tv)
                    rows.append(st)

    df = pd.DataFrame(rows)[["base", "lookback", "vol_win", "tgt_vol",
                             "ann_return", "ann_vol", "sharpe", "sortino",
                             "max_drawdown", "trades", "turnover"]]
    df.to_csv(ROOT / "research" / "h2_train_results.csv", index=False)
    # compact report: per base/lookback, no-overlay vs best & median overlay
    for (b, lb), g in df.groupby(["base", "lookback"], dropna=False):
        ref = g[g.vol_win.isna()].iloc[0]
        ov = g[g.vol_win.notna()]
        print(f"{b} lb={lb}: no-overlay Sharpe={ref.sharpe:.2f} DD={ref.max_drawdown:.2f} | "
              f"overlay Sharpe med={ov.sharpe.median():.2f} min={ov.sharpe.min():.2f} max={ov.sharpe.max():.2f} "
              f"DD med={ov.max_drawdown.median():.2f}")


if __name__ == "__main__":
    main()

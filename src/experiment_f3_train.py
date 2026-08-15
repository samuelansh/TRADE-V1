"""FAMILY 3 — cross-sectional rotation BTC/ETH/LTC. TRAIN only (2016-2018).
Pre-registered: research/FAMILY3_PREREG.md. 48 configs, gates pre-declared.
"""
from pathlib import Path

import numpy as np
import pandas as pd

import backtest

ROOT = Path(__file__).resolve().parents[1]
TRAIN_START, TRAIN_END = "2016-01-01", "2018-12-31"
BURN_IN = 200
BPS, BPS_LTC, FIN = 50.0, 75.0, 0.10
ASSETS = ["btc", "eth", "ltc"]


def load_all(start, end):
    closes = {}
    for a in ASSETS:
        df = pd.read_csv(ROOT / "data" / "raw" / f"{a}.csv")
        s = pd.Series(pd.to_numeric(df["PriceUSD"], errors="coerce").values,
                      index=pd.to_datetime(df["time"])).dropna()
        closes[a] = s[s > 0]
    px = pd.DataFrame(closes).dropna()
    pre = px.loc[:start].tail(BURN_IN)
    return pd.concat([pre, px.loc[start:end]]).loc[lambda d: ~d.index.duplicated()]


def portfolio_run(px, weights, start):
    """weights: DataFrame same shape as px, target weight per asset decided at
    close t, applied next bar. Cost per side: 50bps (75 for LTC) + financing."""
    ret = px.pct_change().fillna(0.0)
    w_held = weights.shift(1).fillna(0.0).clip(0.0, 1.0)
    dw = w_held.diff().abs()
    dw.iloc[0] = w_held.iloc[0]
    side_bps = pd.Series({a: (BPS_LTC if a == "ltc" else BPS) for a in px.columns})
    cost = (dw * side_bps / 1e4).sum(axis=1) + w_held.sum(axis=1) * (FIN / 365)
    r = (w_held * ret).sum(axis=1) - cost
    eq = (1 + r).cumprod()
    eq = eq.loc[start:]
    rr = eq.pct_change().dropna()
    st = backtest.compute_stats(rr, eq / eq.iloc[0], 365)
    st["turnover"] = round(float(dw.sum().sum()), 1)
    return st


def rotation_weights(px, r_look, reb, cash_gate, vol_target):
    mom = px.pct_change(r_look)
    valid = mom.notna().all(axis=1)
    rank_top = pd.Series(None, index=px.index, dtype=object)
    rank_top[valid] = mom[valid].idxmax(axis=1)
    w = pd.DataFrame(0.0, index=px.index, columns=px.columns)
    current = None
    for i, t in enumerate(px.index):
        if i < r_look:
            continue
        if current is None or i % reb == 0:
            top = rank_top.iloc[i]
            if isinstance(top, str):
                if cash_gate and mom.iloc[i][top] < 0:
                    current = None
                else:
                    current = top
        if current is not None:
            w.loc[t, current] = 1.0
    if vol_target:
        rv = px.pct_change().rolling(30).std() * np.sqrt(365)
        scale = (0.6 / rv).clip(upper=1.0)
        w = (w * scale).fillna(0.0)
    return w


def main():
    px = load_all(TRAIN_START, TRAIN_END)
    # benchmarks
    ew = pd.DataFrame(1 / 3, index=px.index, columns=px.columns)
    bench = portfolio_run(px, ew, TRAIN_START)
    print(f"benchmark equal-weight B&H: Sharpe={bench['sharpe']:.2f} "
          f"MaxDD={bench['max_drawdown']:.2f} TotRet={bench['total_return']:.2%}\n")

    rows = []
    for r_look in [30, 60, 90, 120]:
        for reb in [5, 10, 20]:
            for cash_gate in [False, True]:
                for vt in [False, True]:
                    w = rotation_weights(px, r_look, reb, cash_gate, vt)
                    st = portfolio_run(px, w, TRAIN_START)
                    st.update(r=r_look, b=reb, cash=cash_gate, vt=vt)
                    rows.append(st)
    df = pd.DataFrame(rows)[["r", "b", "cash", "vt", "sharpe", "ann_return",
                             "max_drawdown", "total_return", "turnover"]]
    df.to_csv(ROOT / "research" / "f3_train_results.csv", index=False)
    print(df.to_string(index=False))
    gate = (df.sharpe > 1.0) & (df.sharpe > bench["sharpe"]) & \
           (df.max_drawdown > bench["max_drawdown"])
    print(f"\nconfigs passing TRAIN gate: {gate.sum()} / {len(df)} (need >=6 adjacent)")
    print(df[gate].to_string(index=False) if gate.any() else "NONE")


if __name__ == "__main__":
    main()

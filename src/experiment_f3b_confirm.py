"""FAMILY 3B — single confirmatory shot (research/FAMILY3B_PREREG.md).
One config, zero tuning, raised bar. Closes the rotation mechanism either way.
"""
from pathlib import Path

import numpy as np
import pandas as pd

import backtest

ROOT = Path(__file__).resolve().parents[1]
VAL_START, VAL_END = "2019-01-01", "2022-12-31"
BURN_IN = 200
ASSETS = ["btc", "eth", "ltc", "xrp", "doge", "ada", "bnb"]
THIN = {"ltc", "doge"}
FIN = 0.10


def load_universe():
    closes = {}
    for a in ASSETS:
        df = pd.read_csv(ROOT / "data" / "raw" / f"{a}.csv")
        s = pd.Series(pd.to_numeric(df["PriceUSD"], errors="coerce").values,
                      index=pd.to_datetime(df["time"])).dropna()
        closes[a] = s[s > 0]
    px = pd.DataFrame(closes)  # NaN where asset not yet priced
    pre = px.loc[:VAL_START].tail(BURN_IN)
    return pd.concat([pre, px.loc[VAL_START:VAL_END]]).loc[
        lambda d: ~d.index.duplicated()]


def portfolio_run(px, weights):
    ret = px.pct_change().fillna(0.0)
    w_held = weights.shift(1).fillna(0.0).clip(0.0, 1.0)
    dw = w_held.diff().abs(); dw.iloc[0] = w_held.iloc[0]
    side = pd.Series({a: (75.0 if a in THIN else 50.0) for a in px.columns})
    cost = (dw * side / 1e4).sum(axis=1) + w_held.sum(axis=1) * (FIN / 365)
    r = (w_held * ret).sum(axis=1) - cost
    eq = (1 + r).cumprod().loc[VAL_START:]
    rr = eq.pct_change().dropna()
    st = backtest.compute_stats(rr, eq / eq.iloc[0], 365)
    return st, eq


def main():
    px = load_universe()
    mom = px.pct_change(30)
    rv = px.pct_change().rolling(30).std() * np.sqrt(365)
    scale = (0.6 / rv).clip(upper=1.0)

    w = pd.DataFrame(0.0, index=px.index, columns=px.columns)
    held = []
    for i, t in enumerate(px.index):
        if i >= 30 and i % 10 == 0:
            m = mom.iloc[i].dropna()
            m = m[m > 0]                      # absolute-momentum cash gate
            held = list(m.nlargest(2).index)  # top-2 of available
        for a in held:
            w.loc[t, a] = 0.5
    w = (w * scale).fillna(0.0)

    avail = px.notna()
    ew = avail.div(avail.sum(axis=1), axis=0).fillna(0.0)
    ew_vt = (ew * scale).fillna(0.0)

    res = {}
    for name, wt in [("strategy", w), ("ew_bh", ew), ("ew_voltarget", ew_vt)]:
        st, eq = portfolio_run(px, wt)
        res[name] = (st, eq)
        print(f"{name:13s} Sharpe={st['sharpe']:6.3f} AnnRet={st['ann_return']:7.2%} "
              f"MaxDD={st['max_drawdown']:7.2%} TotRet={st['total_return']:8.2%}")

    s, bh, vt = res["strategy"][0], res["ew_bh"][0], res["ew_voltarget"][0]
    eq = res["strategy"][1]
    lr = np.log(eq / eq.shift(1)).dropna()
    yl = lr.groupby(lr.index.year).sum()
    pos = yl[yl > 0].sum()
    conc = float(yl.max() / pos) if pos > 0 else np.nan
    print("\nYearly log-returns (strategy):"); print(yl.round(3).to_string())
    checks = {
        "1 Sharpe > EW B&H": s["sharpe"] > bh["sharpe"],
        "2 Sharpe > EW vol-target": s["sharpe"] > vt["sharpe"],
        "3 MaxDD shallower than EW B&H": s["max_drawdown"] > bh["max_drawdown"],
        "4 positive total return": s["total_return"] > 0,
        "5 concentration <= 0.8": bool(conc <= 0.8),
        "6 RAISED BAR gap>=+0.3 vs both":
            (s["sharpe"] - bh["sharpe"] >= 0.3) and
            (s["sharpe"] - vt["sharpe"] >= 0.3),
    }
    print()
    for k, v in checks.items():
        print(f"{'PASS' if v else 'FAIL'}  {k}")
    print("\nF3B VERDICT:", "PASS" if all(checks.values()) else
          "FAIL — rotation mechanism closed permanently at daily bars")


if __name__ == "__main__":
    main()

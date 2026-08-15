"""FAMILY 3 — single pre-registered VALIDATION pass (2019-2022).

Candidate frozen from TRAIN stable region (r=30 cluster, 6 adjacent passes),
using region-median structure, NOT the best cell:
  rank lookback r=30, rebalance b=10 (median of {5,10,20}),
  cash gate ON (absolute-momentum), vol-target ON (30d, 0.6 — consistent
  with the family-1 sizing philosophy; the conservative variant).
Benchmarks: equal-weight B&H, vol-targeted equal-weight (control).
5 checks as pre-registered in FAMILY3_PREREG.md. One shot.
"""
from pathlib import Path

import numpy as np
import pandas as pd

import backtest
from experiment_f3_train import load_all, portfolio_run, rotation_weights

ROOT = Path(__file__).resolve().parents[1]
VAL_START, VAL_END = "2019-01-01", "2022-12-31"


def main():
    px = load_all(VAL_START, VAL_END)

    w_strat = rotation_weights(px, 30, 10, True, True)
    ew = pd.DataFrame(1 / 3, index=px.index, columns=px.columns)
    rv = px.pct_change().rolling(30).std() * np.sqrt(365)
    ew_vt = (ew * (0.6 / rv).clip(upper=1.0)).fillna(0.0)

    res = {}
    for name, w in [("strategy", w_strat), ("ew_bh", ew), ("ew_voltarget", ew_vt)]:
        st = portfolio_run(px, w, VAL_START)
        res[name] = st
        print(f"{name:13s} Sharpe={st['sharpe']:6.3f} AnnRet={st['ann_return']:7.2%} "
              f"MaxDD={st['max_drawdown']:7.2%} TotRet={st['total_return']:8.2%}")

    # yearly concentration for strategy
    ret = px.pct_change().fillna(0.0)
    w_held = w_strat.shift(1).fillna(0.0).clip(0.0, 1.0)
    dw = w_held.diff().abs(); dw.iloc[0] = w_held.iloc[0]
    side = pd.Series({a: (75.0 if a == "ltc" else 50.0) for a in px.columns})
    cost = (dw * side / 1e4).sum(axis=1) + w_held.sum(axis=1) * (0.10 / 365)
    r = ((w_held * ret).sum(axis=1) - cost).loc[VAL_START:]
    eq = (1 + r).cumprod()
    lr = np.log1p(r)
    yl = lr.groupby(lr.index.year).sum()
    pos = yl[yl > 0].sum()
    conc = float(yl.max() / pos) if pos > 0 else np.nan
    print("\nYearly log-returns (strategy):")
    print(yl.round(3).to_string())

    s, bh, vt = res["strategy"], res["ew_bh"], res["ew_voltarget"]
    checks = {
        "1 Sharpe > equal-weight B&H": s["sharpe"] > bh["sharpe"],
        "2 Sharpe > vol-target EW control": s["sharpe"] > vt["sharpe"],
        "3 MaxDD shallower than EW B&H": s["max_drawdown"] > bh["max_drawdown"],
        "4 positive total return": s["total_return"] > 0,
        "5 no year >80% of positive log-ret": bool(conc <= 0.8),
    }
    print()
    for k, v in checks.items():
        print(f"{'PASS' if v else 'FAIL'}  {k}")
    print("\nVALIDATION VERDICT:", "PASS" if all(checks.values()) else "FAIL")


if __name__ == "__main__":
    main()

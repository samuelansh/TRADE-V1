"""SINGLE pre-registered VALIDATION pass (see research/VALIDATION_PREREG.md).

Candidate: equal-weight TSMOM ensemble {60,90,120,180,250} x vol-target
(win=30, tgt=0.6), long-only, cap 1. Judged at cfd_stress; cfd_base reported.
Benchmarks: buy-and-hold, vol-targeted buy-and-hold.
This script is run ONCE for this family. Results go to the ledger as-is.
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


def load_btc():
    df = pd.read_csv(ROOT / "data" / "raw" / "btc.csv")
    s = pd.Series(pd.to_numeric(df["PriceUSD"], errors="coerce").values,
                  index=pd.to_datetime(df["time"])).dropna()
    return s[s > 0]


def window_stats(res, start, end):
    eq = res.equity.loc[start:end]
    r = eq.pct_change().dropna()
    st = backtest.compute_stats(r, eq / eq.iloc[0], 365)
    st["trades"] = res.trades
    return st, eq


def yearly_logret(eq):
    lr = np.log(eq / eq.shift(1)).dropna()
    return lr.groupby(lr.index.year).sum()


def main():
    close = load_btc()
    pre = close.loc[:VAL_START].tail(BURN_IN_DAYS)
    seg = pd.concat([pre, close.loc[VAL_START:VAL_END]])
    ret = seg.pct_change()
    rv = ret.rolling(VOL_WIN).std() * np.sqrt(365)
    scale = (TGT_VOL / rv).clip(upper=1.0).fillna(0.0)

    ens = sum((seg > seg.shift(lb)).astype(float) for lb in LOOKBACKS) / len(LOOKBACKS)
    w_strat = (ens * scale).clip(0, 1)
    w_bh = pd.Series(1.0, index=seg.index)
    w_bhvt = scale.clip(0, 1)

    out = {}
    for costs in ["cfd_stress", "cfd_base"]:
        bps = backtest.COST_PRESETS_BPS[costs]
        for name, w in [("strategy", w_strat), ("buy_hold", w_bh),
                        ("bh_voltarget", w_bhvt)]:
            res = backtest.run(seg, w, bps)
            st, eq = window_stats(res, VAL_START, VAL_END)
            out[(costs, name)] = (st, eq)
            print(f"[{costs}] {name:13s} Sharpe={st['sharpe']:6.3f} "
                  f"AnnRet={st['ann_return']:7.2%} MaxDD={st['max_drawdown']:7.2%} "
                  f"TotRet={st['total_return']:8.2%} trades={st['trades']}")

    # pre-declared checks at cfd_stress
    s, bh, bhvt = (out[("cfd_stress", k)][0] for k in
                   ["strategy", "buy_hold", "bh_voltarget"])
    eq_s = out[("cfd_stress", "strategy")][1]
    yl = yearly_logret(eq_s)
    total_pos_log = yl[yl > 0].sum()
    conc = float(yl.max() / total_pos_log) if total_pos_log > 0 else np.nan
    print("\nYearly log-returns (strategy, cfd_stress):")
    print(yl.round(3).to_string())
    checks = {
        "1 Sharpe > buy&hold": s["sharpe"] > bh["sharpe"],
        "2 Sharpe > vol-target B&H": s["sharpe"] > bhvt["sharpe"],
        "3 MaxDD shallower than B&H": s["max_drawdown"] > bh["max_drawdown"],
        "4 positive total return": s["total_return"] > 0,
        "5 no year >80% of positive log-ret": bool(conc <= 0.8),
    }
    print()
    for k, v in checks.items():
        print(f"{'PASS' if v else 'FAIL'}  {k}")
    print("\nVERDICT:", "PASS" if all(checks.values()) else "FAIL")

    pd.DataFrame({f"{c}_{n}": st for (c, n), (st, _) in out.items()}
                 ).to_csv(ROOT / "research" / "validation_pass1_results.csv")


if __name__ == "__main__":
    main()

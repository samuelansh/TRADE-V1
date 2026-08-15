"""SINGLE LOCKED TEST EVALUATION — 2023-01-01 .. 2026-05-24.

Run ONCE for frozen candidate v1 (strategy.py, params per VALIDATION_PREREG).
Same benchmarks and checks as validation. Also replays the paper trader
(risk engine active) over TEST to report what the safety wrapper does.
Result is final for this strategy version: any later modification = new
strategy = tainted TEST (flagged REUSED_TEST).
"""
from pathlib import Path

import numpy as np
import pandas as pd

import backtest
import strategy
from paper_trader import replay
from risk_engine import RiskLimits

ROOT = Path(__file__).resolve().parents[1]
TEST_START, TEST_END = "2023-01-01", "2026-05-24"
BURN_IN = strategy.MIN_HISTORY + 40


def load(fname="btc.csv"):
    df = pd.read_csv(ROOT / "data" / "raw" / fname)
    s = pd.Series(pd.to_numeric(df["PriceUSD"], errors="coerce").values,
                  index=pd.to_datetime(df["time"])).dropna()
    return s[s > 0]


def stats_on(res, start):
    eq = res.equity.loc[start:]
    r = eq.pct_change().dropna()
    return backtest.compute_stats(r, eq / eq.iloc[0], 365), eq


def main():
    close = load()
    seg = pd.concat([close.loc[:TEST_START].tail(BURN_IN),
                     close.loc[TEST_START:TEST_END]])
    seg = seg[~seg.index.duplicated()]
    ret = seg.pct_change()
    rv = ret.rolling(strategy.VOL_WIN).std() * np.sqrt(365)
    scale = (strategy.TGT_VOL / rv).clip(upper=1.0)

    w_strat = strategy.target_weight_series(seg)
    w_bh = pd.Series(1.0, index=seg.index)
    w_bhvt = scale.clip(0, 1).fillna(0.0)

    out = {}
    for costs in ["cfd_stress", "cfd_base"]:
        bps = backtest.COST_PRESETS_BPS[costs]
        for name, w in [("strategy", w_strat), ("buy_hold", w_bh),
                        ("bh_voltarget", w_bhvt)]:
            st, eq = stats_on(backtest.run(seg, w, bps), TEST_START)
            out[(costs, name)] = (st, eq)
            print(f"[{costs}] {name:13s} Sharpe={st['sharpe']:6.3f} "
                  f"AnnRet={st['ann_return']:7.2%} MaxDD={st['max_drawdown']:7.2%} "
                  f"TotRet={st['total_return']:8.2%}")

    s, bh, bhvt = (out[("cfd_stress", k)][0] for k in
                   ["strategy", "buy_hold", "bh_voltarget"])
    eq_s = out[("cfd_stress", "strategy")][1]
    lr = np.log(eq_s / eq_s.shift(1)).dropna()
    yl = lr.groupby(lr.index.year).sum()
    pos = yl[yl > 0].sum()
    conc = float(yl.max() / pos) if pos > 0 else np.nan
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
    print("\nTEST VERDICT:", "PASS" if all(checks.values()) else "FAIL")

    # Paper trader with ACTIVE risk engine over the same window
    print("\n--- paper trader replay (risk engine active, default limits) ---")
    pt = replay(seg, 10_000,
                ROOT / "research" / "paper_journal_test.csv",
                RiskLimits())
    print("paper summary:", pt.summary())

    pd.DataFrame({f"{c}_{n}": st for (c, n), (st, _) in out.items()}
                 ).to_csv(ROOT / "research" / "test_final_results.csv")


if __name__ == "__main__":
    main()

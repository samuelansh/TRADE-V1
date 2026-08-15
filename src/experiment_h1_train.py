"""H1 (TSMOM) — TRAIN segment only (2012-2018). No VALIDATION/TEST access.

Long-only: weight 1 if close > close N days ago, else 0. Parameter sweep over
N to find whether a broad stable region exists (not a single best N).
Benchmarks: buy-and-hold on the same segment, same costs at entry.
"""
from pathlib import Path

import pandas as pd

import backtest

ROOT = Path(__file__).resolve().parents[1]

TRAIN_START, TRAIN_END = "2012-01-01", "2018-12-31"
BURN_IN_DAYS = 400  # indicator warm-up taken from before TRAIN_START


def load_btc():
    df = pd.read_csv(ROOT / "data" / "raw" / "btc.csv")
    s = pd.Series(pd.to_numeric(df["PriceUSD"], errors="coerce").values,
                  index=pd.to_datetime(df["time"])).dropna()
    return s[s > 0]


def main():
    close = load_btc()
    pre = close.loc[:TRAIN_START].tail(BURN_IN_DAYS)
    seg = pd.concat([pre, close.loc[TRAIN_START:TRAIN_END]])

    rows = []
    for cost_name, bps in backtest.COST_PRESETS_BPS.items():
        # buy & hold benchmark
        bh_w = pd.Series(1.0, index=seg.index)
        res = backtest.run(seg, bh_w, bps)
        r = trim_stats(res, seg)
        r.update(strategy="buy_hold", lookback=None, costs=cost_name)
        rows.append(r)
        for n in [10, 20, 30, 45, 60, 90, 120, 180, 250, 365]:
            w = (seg > seg.shift(n)).astype(float)
            res = backtest.run(seg, w, bps)
            r = trim_stats(res, seg)
            r.update(strategy=f"tsmom", lookback=n, costs=cost_name)
            rows.append(r)

    df = pd.DataFrame(rows)[["strategy", "lookback", "costs", "ann_return",
                             "ann_vol", "sharpe", "sortino", "max_drawdown",
                             "trades", "total_return"]]
    out = ROOT / "research" / "h1_train_results.csv"
    df.to_csv(out, index=False)
    print(df.to_string(index=False))


def trim_stats(res, seg):
    """Recompute stats on TRAIN window only (drop burn-in)."""
    eq = res.equity.loc[TRAIN_START:]
    r = eq.pct_change().dropna()
    st = backtest.compute_stats(r, eq / eq.iloc[0], 365)
    st["trades"] = res.trades
    return st


if __name__ == "__main__":
    main()

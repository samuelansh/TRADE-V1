"""FAMILY 4 — TRAIN runs (2016-2020, hourly bars). Prereg: FAMILY4_PREREG.md.
4A candlestick patterns (18 cfg) · 4B sessions (11 cfg) · 4C breakout+ATR stops (12 cfg)
Costs: 10 bps/side primary, 26 bps stress (gate judged at 26). No financing (spot).
Gate per sub-family: Sharpe>1.0 across >=4 adjacent configs AND beats B&H Sharpe.
Data caveat carried: single-venue wicks (ledger 0014).
"""
from pathlib import Path

import numpy as np
import pandas as pd

import backtest

ROOT = Path(__file__).resolve().parents[1]
TRAIN_START, TRAIN_END = "2016-01-01", "2020-12-31"
PPY = 8760


def load():
    df = pd.read_csv(ROOT / "data" / "raw" / "btc_1h_bitstamp.csv")
    df.index = pd.to_datetime(df["Date"]).dt.tz_localize(None)
    df = df[["Open", "High", "Low", "Close", "Volume"]].astype(float)
    pre = df.loc[:TRAIN_START].tail(2000)
    return pd.concat([pre, df.loc[TRAIN_START:TRAIN_END]]).loc[
        lambda d: ~d.index.duplicated()]


def hold_weight(entry, m):
    w = entry.astype(float).values.copy()
    out = w.copy()
    for i in range(1, m):
        out = np.maximum(out, np.roll(w, i))
        out[:i] = w[:i]
    return pd.Series(out, index=entry.index)


def stats_of(close, w, bps):
    res = backtest.run(close, w, bps, periods_per_year=PPY)
    eq = res.equity.loc[TRAIN_START:]
    r = eq.pct_change().dropna()
    st = backtest.compute_stats(r, eq / eq.iloc[0], PPY)
    st["trades"] = res.trades
    return st


def run_4a(df, rows):
    O, H, L, C = df.Open, df.High, df.Low, df.Close
    body = (C - O).abs()
    rng = (H - L).replace(0, np.nan)
    up_w = H - np.maximum(O, C)
    lo_w = np.minimum(O, C) - L
    down24 = C.pct_change(24) < 0
    pats = {
        "hammer": (lo_w >= 2 * body) & (up_w <= 0.3 * rng) & (body > 0),
        "bull_engulf": (C > O) & (C.shift(1) < O.shift(1)) &
                       (C >= O.shift(1)) & (O <= C.shift(1)),
        "doji_rev": (body <= 0.1 * rng),
    }
    for pname, sig in pats.items():
        for ctx_name, ctx in [("any", pd.Series(True, index=df.index)),
                              ("downtrend", down24)]:
            entry = (sig & ctx).fillna(False)
            for m in [4, 12, 24]:
                w = hold_weight(entry, m)
                st26 = stats_of(C, w, 26.0)
                st10 = stats_of(C, w, 10.0)
                rows.append({"fam": "4A", "config": f"{pname}/{ctx_name}/h{m}",
                             "sharpe26": st26["sharpe"], "ret26": st26["total_return"],
                             "sharpe10": st10["sharpe"], "dd26": st26["max_drawdown"],
                             "trades": st26["trades"],
                             "n_signals": int(entry.loc[TRAIN_START:].sum())})


def run_4b(df, rows):
    C = df.Close
    hr, dow = df.index.hour, df.index.dayofweek
    cfgs = {
        "asia_00_08": (hr >= 0) & (hr < 8),
        "eu_08_16": (hr >= 8) & (hr < 16),
        "us_16_24": (hr >= 16),
        "weekday": dow < 5,
        "weekend": dow >= 5,
        "asia_weekday": ((hr >= 0) & (hr < 8)) & (dow < 5),
        "eu_weekday": ((hr >= 8) & (hr < 16)) & (dow < 5),
        "us_weekday": (hr >= 16) & (dow < 5),
    }
    # top/bottom-8 hours selected on 2016-2017 only (disclosed in-train selection)
    r = C.pct_change()
    sel = r.loc["2016":"2017"]
    hr_mean = sel.groupby(sel.index.hour).mean()
    top8 = set(hr_mean.nlargest(8).index)
    bot8 = set(hr_mean.nsmallest(8).index)
    cfgs["top8h_1617"] = pd.Index(hr).isin(list(top8))
    cfgs["bot8h_1617"] = pd.Index(hr).isin(list(bot8))
    for name, mask in cfgs.items():
        w = pd.Series(np.where(mask, 1.0, 0.0), index=df.index)
        st26 = stats_of(C, w, 26.0)
        st10 = stats_of(C, w, 10.0)
        rows.append({"fam": "4B", "config": name,
                     "sharpe26": st26["sharpe"], "ret26": st26["total_return"],
                     "sharpe10": st10["sharpe"], "dd26": st26["max_drawdown"],
                     "trades": st26["trades"], "n_signals": int(mask.sum())})


def run_4c(df, rows):
    H, L, C = df.High.values, df.Low.values, df.Close.values
    idx = df.index
    tr = np.maximum(H - L, np.maximum(abs(H - np.roll(C, 1)),
                                      abs(L - np.roll(C, 1))))
    atr = pd.Series(tr, index=idx).rolling(24).mean().values
    for N in [24, 72, 168]:
        roll_hi = pd.Series(H, index=idx).rolling(N).max().shift(1).values
        for k in [1.0, 2.0]:
            for timed in [0, 72]:
                w = np.zeros(len(C))
                in_pos, stop, bars = False, 0.0, 0
                for i in range(1, len(C)):
                    if in_pos:
                        bars += 1
                        if L[i] <= stop or (timed and bars >= timed):
                            in_pos = False
                        else:
                            w[i] = 1.0
                    if not in_pos and not np.isnan(roll_hi[i]) and \
                            C[i] > roll_hi[i] and not np.isnan(atr[i]):
                        in_pos, stop, bars = True, C[i] - k * atr[i], 0
                        w[i] = 1.0
                ws = pd.Series(w, index=idx)
                st26 = stats_of(df.Close, ws, 26.0)
                st10 = stats_of(df.Close, ws, 10.0)
                rows.append({"fam": "4C",
                             "config": f"N{N}/stop{k}ATR/{'timed'+str(timed) if timed else 'stop-only'}",
                             "sharpe26": st26["sharpe"], "ret26": st26["total_return"],
                             "sharpe10": st10["sharpe"], "dd26": st26["max_drawdown"],
                             "trades": st26["trades"], "n_signals": None})


def main():
    df = load()
    C = df.Close
    bh = stats_of(C, pd.Series(1.0, index=df.index), 26.0)
    print(f"BENCHMARK buy&hold (26bps): Sharpe={bh['sharpe']:.2f} "
          f"TotRet={bh['total_return']:.1%} MaxDD={bh['max_drawdown']:.1%}\n")
    rows = []
    run_4a(df, rows)
    run_4b(df, rows)
    run_4c(df, rows)
    out = pd.DataFrame(rows)
    out.to_csv(ROOT / "research" / "f4_train_results.csv", index=False)
    print(out.to_string(index=False))
    for fam in ["4A", "4B", "4C"]:
        g = out[out.fam == fam]
        ok = (g.sharpe26 > 1.0) & (g.sharpe26 > bh["sharpe"]) & (g.ret26 > 0)
        print(f"\n{fam}: {int(ok.sum())}/{len(g)} configs pass gate "
              f"(need >=4 adjacent + beat B&H {bh['sharpe']:.2f})")
        if ok.any():
            print(g[ok].to_string(index=False))


if __name__ == "__main__":
    main()

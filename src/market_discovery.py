"""Market discovery (Master Prompt §5): quantitative comparison of candidate
markets on the data we actually have. Writes research/MARKET_DISCOVERY.md.
"""
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"


def load(fname, tcol, pcol):
    df = pd.read_csv(RAW / fname)
    t = pd.to_datetime(df[tcol])
    p = pd.to_numeric(df[pcol], errors="coerce")
    s = pd.Series(p.values, index=t).dropna()
    return s[s > 0]


def stats(s, periods_per_year):
    r = np.log(s / s.shift(1)).dropna()
    ann_vol = r.std() * np.sqrt(periods_per_year)
    # simple trendiness proxy: |sum of returns| vs sum of |returns| over rolling windows
    win = min(90, max(20, len(r) // 20))
    roll = r.rolling(win).sum().abs() / r.abs().rolling(win).sum()
    autocorr1 = r.autocorr(1)
    return {
        "obs": len(r),
        "years": round((s.index[-1] - s.index[0]).days / 365.25, 1),
        "ann_vol_pct": round(100 * ann_vol, 1),
        "daily_med_abs_move_pct": round(100 * r.abs().median(), 3),
        "trendiness_med": round(float(roll.median()), 3),
        "autocorr_lag1": round(float(autocorr1), 4),
        "worst_move_pct": round(100 * r.min(), 1),
    }


def main():
    rows = []
    for name, f, tcol, pcol, ppy in [
        ("BTC/USD", "btc.csv", "time", "PriceUSD", 365),
        ("ETH/USD", "eth.csv", "time", "PriceUSD", 365),
        ("LTC/USD", "ltc.csv", "time", "PriceUSD", 365),
        ("Gold (monthly)", "gold_monthly.csv", "Date", "Price", 12),
        ("S&P500 (monthly)", "sp500_monthly.csv", "Date", "SP500", 12),
    ]:
        s = load(f, tcol, pcol)
        st = stats(s, ppy)
        st["market"] = name
        rows.append(st)
    df = pd.DataFrame(rows).set_index("market")
    print(df.to_string())
    df.to_csv(ROOT / "research" / "market_stats.csv")


if __name__ == "__main__":
    main()

"""Forward-data pipeline: splice Kraken updates onto the historical BTC series,
with integrity checks at the seam (source-switch is a known risk point).

Inputs : data/raw/btc.csv (coinmetrics daily, ends 2026-05-24)
         data/raw/btc_updates.csv (kraken daily closes, ts unix seconds;
         appended from saved fetch-tool responses; last-partial-candle already
         excluded at conversion time)
Output : data/processed/btc_spliced.csv + seam report
Rules  : never silently alter history; overlap region compared, divergence
         >2% aborts the splice (different sources must roughly agree).
"""
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]


def load_hist():
    df = pd.read_csv(ROOT / "data" / "raw" / "btc.csv")
    s = pd.Series(pd.to_numeric(df["PriceUSD"], errors="coerce").values,
                  index=pd.to_datetime(df["time"])).dropna()
    return s[s > 0]


def load_updates():
    df = pd.read_csv(ROOT / "data" / "raw" / "btc_updates.csv")
    s = pd.Series(df["close"].astype(float).values,
                  index=pd.to_datetime(df["ts"].astype(int), unit="s"))
    return s.sort_index()


def splice(max_overlap_div=0.02):
    hist, upd = load_hist(), load_updates()
    overlap = hist.index.intersection(upd.index)
    report = {"hist_end": str(hist.index[-1].date()),
              "upd_start": str(upd.index[0].date()),
              "upd_end": str(upd.index[-1].date()),
              "overlap_days": len(overlap)}
    if len(overlap):
        div = (upd.loc[overlap] / hist.loc[overlap] - 1).abs()
        report["max_overlap_divergence"] = round(float(div.max()), 4)
        if div.max() > max_overlap_div:
            raise SystemExit(f"ABORT SPLICE: sources diverge {div.max():.2%} "
                             f"on overlap (> {max_overlap_div:.0%})")
    gap = (upd.index[0] - hist.index[-1]).days
    if gap > 1 and not len(overlap):
        report["seam_gap_days"] = gap
        if gap > 3:
            raise SystemExit(f"ABORT SPLICE: {gap}-day hole at seam")
    out = pd.concat([hist[~hist.index.isin(overlap)], upd]).sort_index()
    assert out.index.is_unique and out.index.is_monotonic_increasing
    assert (out > 0).all()
    dest = ROOT / "data" / "processed" / "btc_spliced.csv"
    out.rename("close").rename_axis("time").to_csv(dest)
    report["rows"] = len(out)
    return out, report


if __name__ == "__main__":
    s, rep = splice()
    print(rep)
    print(f"spliced series: {s.index[0].date()} .. {s.index[-1].date()}")

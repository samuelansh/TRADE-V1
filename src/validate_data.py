"""Data integrity validation for raw datasets (Master Prompt §6).

Checks: parseable timestamps, monotonic order, duplicates, gaps, non-positive
prices, extreme outlier returns, and writes a dataset manifest.
"""
import json
import hashlib
import sys
from pathlib import Path

import pandas as pd

RAW = Path(__file__).resolve().parents[1] / "data" / "raw"
OUT = Path(__file__).resolve().parents[1] / "data" / "MANIFEST.json"

SPECS = {
    # file: (time col, price col, expected freq, source)
    "btc.csv": ("time", "PriceUSD", "D", "coinmetrics/data@f1a36af"),
    "eth.csv": ("time", "PriceUSD", "D", "coinmetrics/data@f1a36af"),
    "ltc.csv": ("time", "PriceUSD", "D", "coinmetrics/data@f1a36af"),
# sol.csv REJECTED 2026-08-15: only 7 priced rows in coinmetrics ReferenceRateUSD
    "gold_monthly.csv": ("Date", "Price", "MS", "datasets/gold-prices@HEAD"),
    "sp500_monthly.csv": ("Date", "SP500", "MS", "datasets/s-and-p-500@HEAD"),
    "btc_kraken_daily.csv": ("time", "close", "D", "kraken public OHLC API"),
    "eth_kraken_daily.csv": ("time", "close", "D", "kraken public OHLC API"),
}


def validate(fname, tcol, pcol, freq, source):
    path = RAW / fname
    if not path.exists():
        return {"file": fname, "status": "MISSING"}
    df = pd.read_csv(path)
    r = {"file": fname, "source": source, "rows": len(df),
         "sha256": hashlib.sha256(path.read_bytes()).hexdigest()[:16]}
    t = pd.to_datetime(df[tcol], errors="coerce")
    r["bad_timestamps"] = int(t.isna().sum())
    r["start"], r["end"] = str(t.min().date()), str(t.max().date())
    r["duplicates"] = int(t.duplicated().sum())
    r["monotonic"] = bool(t.is_monotonic_increasing)
    p = pd.to_numeric(df[pcol], errors="coerce")
    valid = p.notna() & (p > 0)
    r["price_col"] = pcol
    # Leading null prices are legitimate (asset existed before a market did):
    # trim them, then judge the priced segment.
    if valid.any():
        first = valid.idxmax()
        r["leading_null_prices_trimmed"] = int(first)
        p, valid, t = p.loc[first:], valid.loc[first:], t.loc[first:]
        r["priced_start"] = str(t.iloc[0].date())
    r["interior_null_or_nonpositive"] = int((~valid).sum())
    # gaps
    if freq == "D":
        diffs = t.diff().dt.days.dropna()
        r["gaps_gt_1d"] = int((diffs > 1).sum())
        r["max_gap_days"] = int(diffs.max()) if len(diffs) else None
    # extreme returns on valid segment
    pv = p[valid]
    ret = pv.pct_change().dropna()
    r["abs_return_gt_50pct"] = int((ret.abs() > 0.5).sum())
    r["max_abs_return"] = round(float(ret.abs().max()), 4) if len(ret) else None
    r["null_price_ratio"] = round(float((~valid).sum()) / max(len(p), 1), 4)
    r["priced_rows"] = int(valid.sum())
    problems = (r["bad_timestamps"] or r["duplicates"] or not r["monotonic"]
                or r["null_price_ratio"] > 0.05
                or r["priced_rows"] < 500)
    r["status"] = "FAIL" if problems else "OK"
    return r


def main():
    results = [validate(f, *spec) for f, spec in SPECS.items()]
    OUT.write_text(json.dumps({"generated": pd.Timestamp.now().isoformat(),
                               "datasets": results}, indent=2))
    for r in results:
        print(f"{r['file']:24s} {r['status']:8s} rows={r.get('rows','-'):>6} "
              f"{r.get('start','')}..{r.get('end','')} dup={r.get('duplicates','-')} "
              f"gaps>{'1d'}={r.get('gaps_gt_1d','-')} maxret={r.get('max_abs_return','-')}")
    if any(r["status"] == "FAIL" for r in results):
        sys.exit(1)


if __name__ == "__main__":
    main()

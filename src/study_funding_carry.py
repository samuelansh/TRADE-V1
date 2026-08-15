"""Funding carry descriptive study (prereg: FUNDING_CARRY_STUDY_PREREG.md).

DATA NOTE (disclosed): full-year hourly series is served in 127 fetch chunks;
downloading all was impractical. Instead: 9 systematically-spaced windows
(~3 days each) across Aug-2025..Aug-2026, transcribed at ~4h intervals
(~160 observations). Good for level/sign estimates; 30-day tail question can
only be bounded, stated as such.
"""
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RISK_FREE = 0.05
ROUND_TRIP_COST = 4 * 0.0026  # entry+exit on both legs @26bps


def main():
    df = pd.read_csv(ROOT / "data" / "raw" / "funding_btc_sampled.csv")
    df["t"] = pd.to_datetime(df["timestamp"])
    r = df["rel_funding_hourly"]

    ann = lambda x: x * 8760
    print("=== Q1 gross annualized carry (short-perp side receives when >0) ===")
    print(f"overall mean: {ann(r.mean()):+.2%}/yr  (n={len(r)} obs, 9 windows)")
    per_w = df.groupby("window").agg(
        start=("t", "min"), mean_hourly=("rel_funding_hourly", "mean"))
    per_w["annualized"] = ann(per_w.mean_hourly)
    for w, row in per_w.iterrows():
        print(f"  {w}  {row.start.date()}  {row.annualized:+7.2%}/yr")

    print("\n=== Q2 sign persistence ===")
    pos = (r > 0).mean()
    print(f"positive-funding share of sampled hours: {pos:.1%}")
    neg_windows = (per_w.annualized < 0).sum()
    print(f"windows with negative mean: {neg_windows}/9 (w5 = Apr-2026)")

    print("\n=== Q3 tail bound (sampled, not exhaustive) ===")
    worst_w = per_w.annualized.min()
    print(f"worst sampled window mean: {worst_w:+.2%}/yr "
          f"=> approx 30-day cumulative at that rate: {worst_w/12:+.2%}")

    print("\n=== Q4 net yield ===")
    gross = ann(r.mean())
    for hold_months in [3, 6, 12]:
        cost_ann = ROUND_TRIP_COST * (12 / hold_months)
        print(f"  hold {hold_months:2d}m: net ≈ {gross - cost_ann:+.2%}/yr "
              f"(cost drag {cost_ann:.2%})")

    print("\n=== Q5 go/no-go vs pre-registered bar ===")
    net12 = gross - ROUND_TRIP_COST
    bar = RISK_FREE + 0.03
    checks = {
        f"net carry {net12:+.2%} > {bar:.0%} (rf+3pp)": net12 > bar,
        f"positive hours {pos:.0%} > 65%": pos > 0.65,
        f"worst 30d bound {worst_w/12:+.2%} > -1%": (worst_w / 12) > -0.01,
    }
    for k, v in checks.items():
        print(f"  {'PASS' if v else 'FAIL'}  {k}")
    print("\nVERDICT:", "GO" if all(checks.values()) else "NO-GO",
          "(per pre-registered criteria)")


if __name__ == "__main__":
    main()

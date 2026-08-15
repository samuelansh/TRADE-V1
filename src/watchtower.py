"""WATCHTOWER — checks if the market is offering a fat pitch yet.

Not a trading bot. A lookout. Run it anytime (or ask the agent to).
Checks the tripwires that would reopen research with a REAL margin:

1. FUNDING SPIKE: carry trade reopens if funding > 15%/yr sustained
   (2021-mania levels; at that level net carry beats the bar with room)
2. PANIC REGIME: 30d realized vol > 100%/yr (dislocations = fat pitches;
   also when our validated risk tools matter most)
3. FORWARD PAPER: how the v1 experiment is tracking (neutral report)

Data needed (paste from fetch tool / API when running with agent):
- latest funding rates -> data/raw/funding_latest.csv (ts, rel_hourly)
- latest daily closes  -> spliced file via update_pipeline.py
"""
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]

FUNDING_TRIPWIRE = 0.15   # 15%/yr sustained
VOL_TRIPWIRE = 1.00       # 100%/yr realized vol


def check_funding():
    f = ROOT / "data" / "raw" / "funding_latest.csv"
    src = f if f.exists() else ROOT / "data" / "raw" / "funding_btc_sampled.csv"
    df = pd.read_csv(src)
    col = "rel_hourly" if "rel_hourly" in df.columns else "rel_funding_hourly"
    recent = df[col].tail(72)  # ~3 days
    ann = recent.mean() * 8760
    status = "TRIPPED — carry trade worth a fresh look" if ann > FUNDING_TRIPWIRE \
        else "quiet"
    return f"FUNDING: {ann:+.1%}/yr (3d avg) vs {FUNDING_TRIPWIRE:.0%} tripwire → {status}"


def check_vol():
    f = ROOT / "data" / "processed" / "btc_spliced.csv"
    if not f.exists():
        return "VOL: no spliced file — run update_pipeline.py first"
    s = pd.read_csv(f)
    close = pd.Series(s["close"].values, index=pd.to_datetime(s["time"]))
    rv = close.pct_change().tail(30).std() * np.sqrt(365)
    status = "TRIPPED — panic regime, dislocations possible" if rv > VOL_TRIPWIRE \
        else "calm"
    return f"VOL: 30d realized {rv:.0%}/yr vs {VOL_TRIPWIRE:.0%} tripwire → {status}"


def check_paper():
    j = ROOT / "research" / "paper_forward_journal.csv"
    if not j.exists():
        return "PAPER: no journal yet — run paper_forward.py"
    df = pd.read_csv(j)
    eq = df.equity.iloc[-1]
    return (f"PAPER: {len(df)} bars, equity {eq:,.0f}/10,000 "
            f"({eq/10000-1:+.1%}), weight {df.approved_w.iloc[-1]:.2f}, "
            f"halted={df.halted.iloc[-1]}")


def main():
    print(f"WATCHTOWER REPORT — {datetime.now():%Y-%m-%d}")
    print("-" * 60)
    for fn in (check_funding, check_vol, check_paper):
        try:
            print(fn())
        except Exception as e:
            print(f"{fn.__name__}: error {e!r}")
    print("-" * 60)
    print("All quiet = correct outcome. NO TRADE is a position.")


if __name__ == "__main__":
    main()

"""Forward paper trading of rejected-for-demo candidate v1.

Purpose (ledger 0005 option b): gather true out-of-sample evidence at zero
cost/risk. The window starts 2026-05-25 — after the consumed TEST window —
so every bar here is evidence no optimization ever saw.

Re-runnable: replays the full forward window from the spliced file each time
new updates are appended (journal is rewritten, deterministic).
"""
import json
from pathlib import Path

import pandas as pd

import strategy
from paper_trader import replay
from risk_engine import RiskLimits

ROOT = Path(__file__).resolve().parents[1]
FORWARD_START = "2026-05-25"
JOURNAL = ROOT / "research" / "paper_forward_journal.csv"


def main():
    df = pd.read_csv(ROOT / "data" / "processed" / "btc_spliced.csv")
    s = pd.Series(df["close"].astype(float).values,
                  index=pd.to_datetime(df["time"]))
    seg = pd.concat([s.loc[:FORWARD_START].tail(strategy.MIN_HISTORY + 40),
                     s.loc[FORWARD_START:]])
    seg = seg[~seg.index.duplicated()]
    if JOURNAL.exists():
        JOURNAL.unlink()
    pt = replay(seg, 10_000, JOURNAL, RiskLimits(),
                warmup=strategy.MIN_HISTORY + 39)
    j = pd.read_csv(JOURNAL)
    summary = pt.summary()
    summary.update(bars=len(j), first=str(j.time.iloc[0]),
                   last=str(j.time.iloc[-1]),
                   avg_weight=round(float(j.approved_w.mean()), 3))
    print(json.dumps(summary, indent=2))
    # benchmark over identical window
    bh = float(seg.loc[j.time.iloc[-1]] / seg.loc[j.time.iloc[0]] - 1)
    print(f"buy&hold same window: {bh:+.2%} | strategy: "
          f"{summary['equity'] / 10000 - 1:+.2%}")


if __name__ == "__main__":
    main()

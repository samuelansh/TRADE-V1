"""Paper-trading engine: replays or receives daily closes bar-by-bar,
routes strategy signal through the risk engine, keeps a trade journal.

This is the same decision path a live MT5 layer would use:
  new bar -> strategy.target_weight(history) -> risk.check() -> rebalance.
No vectorization, no future access: the strategy sees only bars <= t.
"""
import csv
import json
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

import strategy
from risk_engine import RiskEngine, RiskLimits

COST_BPS_PER_SIDE = 50.0  # cfd_stress; keep pessimistic in paper mode


class PaperTrader:
    def __init__(self, start_equity: float, journal_path: Path,
                 limits: RiskLimits = None):
        self.equity = float(start_equity)
        self.weight = 0.0
        self.risk = RiskEngine(start_equity, limits)
        self.journal_path = Path(journal_path)
        self.journal_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.journal_path.exists():
            with open(self.journal_path, "w", newline="") as f:
                csv.writer(f).writerow(
                    ["time", "close", "ret", "desired_w", "approved_w",
                     "reason", "cost", "equity", "halted"])

    def on_bar(self, history: pd.Series, now: datetime = None):
        """history: closes up to and including the new bar."""
        now = now or datetime.now(timezone.utc)
        close = float(history.iloc[-1])
        ret = float(history.pct_change().iloc[-1]) if len(history) > 1 else 0.0

        # mark-to-market with the weight held INTO this bar
        pnl = self.weight * ret * self.equity
        self.equity += pnl

        desired = strategy.target_weight(history)
        t_last = history.index[-1]
        t_last = t_last.tz_localize(timezone.utc) if t_last.tzinfo is None else t_last
        approved, reason = self.risk.check(desired, self.equity, t_last, now, ret)

        cost = abs(approved - self.weight) * (COST_BPS_PER_SIDE / 1e4) * self.equity
        self.equity -= cost
        self.weight = approved

        with open(self.journal_path, "a", newline="") as f:
            csv.writer(f).writerow(
                [history.index[-1].date(), round(close, 2), round(ret, 6),
                 round(desired, 4), round(approved, 4), reason,
                 round(cost, 4), round(self.equity, 4),
                 self.risk.state.halted])
        return {"desired": desired, "approved": approved, "reason": reason,
                "equity": self.equity}

    def summary(self):
        return {"equity": round(self.equity, 2), "weight": round(self.weight, 4),
                "halted": self.risk.state.halted,
                "halt_reason": self.risk.state.halt_reason}


def replay(close: pd.Series, start_equity=10_000.0, journal="journal.csv",
           limits=None, warmup=strategy.MIN_HISTORY):
    """Bar-by-bar replay over a historical series."""
    pt = PaperTrader(start_equity, Path(journal), limits)
    for i in range(warmup, len(close)):
        hist = close.iloc[: i + 1]
        now = hist.index[-1].tz_localize(timezone.utc)
        pt.on_bar(hist, now=now)
    return pt


if __name__ == "__main__":
    import sys
    root = Path(__file__).resolve().parents[1]
    df = pd.read_csv(root / "data" / "raw" / "btc.csv")
    s = pd.Series(pd.to_numeric(df["PriceUSD"], errors="coerce").values,
                  index=pd.to_datetime(df["time"])).dropna()
    s = s[s > 0]
    start, end = sys.argv[1], sys.argv[2]
    seg = s.loc[:end]
    seg = pd.concat([seg.loc[:start].tail(strategy.MIN_HISTORY + 40),
                     seg.loc[start:]])
    seg = seg[~seg.index.duplicated()]
    pt = replay(seg, journal=root / "research" / "paper_journal.csv")
    print(json.dumps(pt.summary(), indent=2))

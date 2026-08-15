"""Red-team tests: risk engine kill-switches, abnormal conditions, and
paper-trader vs vectorized backtester consistency.
"""
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
import tempfile

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
import backtest
import strategy
from risk_engine import RiskEngine, RiskLimits
from paper_trader import PaperTrader, replay

NOW = datetime(2026, 1, 10, tzinfo=timezone.utc)
FRESH = NOW - timedelta(hours=12)


def test_stale_data_blocks_trading():
    re = RiskEngine(10000)
    w, reason = re.check(0.8, 10000, NOW - timedelta(days=5), NOW, 0.01)
    assert w == 0.0 and "stale" in reason


def test_abnormal_move_blocks_trading():
    re = RiskEngine(10000)
    w, reason = re.check(0.8, 10000, FRESH, NOW, -0.45)
    assert w == 0.0 and "abnormal" in reason


def test_daily_loss_halts_and_stays_halted():
    re = RiskEngine(10000)
    re.check(0.5, 10000, FRESH, NOW, 0.0)          # sets day-start equity
    w, reason = re.check(0.5, 9400, FRESH, NOW, -0.06)
    assert w == 0.0 and "HALT" in reason
    w2, r2 = re.check(0.5, 12000, FRESH, NOW + timedelta(days=1), 0.02)
    assert w2 == 0.0 and "HALTED" in r2            # no silent resume


def test_drawdown_halts():
    re = RiskEngine(10000, RiskLimits(max_daily_loss=1.0))  # isolate DD rule
    re.check(0.5, 14000, FRESH, NOW, 0.0)          # peak = 14000
    w, reason = re.check(0.5, 10400, FRESH, NOW + timedelta(days=2), -0.03)
    assert w == 0.0 and "max_drawdown" in reason


def test_weight_clipped():
    re = RiskEngine(10000)
    w, reason = re.check(1.7, 10000, FRESH, NOW, 0.0)
    assert w == 1.0 and "CLIPPED" in reason


def test_risk_engine_error_means_no_trade():
    re = RiskEngine(10000)
    w, reason = re.check(0.5, 10000, None, NOW, 0.0)  # None -> TypeError inside
    assert w == 0.0 and "NO TRADE" in reason


def test_insufficient_history_no_trade():
    close = pd.Series(np.linspace(100, 120, 50),
                      index=pd.date_range("2025-01-01", periods=50))
    assert strategy.target_weight(close) == 0.0


def test_paper_matches_vectorized_backtest():
    """Same series, no risk-limit hits -> paper equity ~= backtester equity."""
    rng = np.random.default_rng(7)
    n = strategy.MIN_HISTORY + 200
    ret = rng.normal(0.0005, 0.01, n)               # mild vol: no halts
    close = pd.Series(100 * np.exp(np.cumsum(ret)),
                      index=pd.date_range("2024-01-01", periods=n))
    with tempfile.TemporaryDirectory() as d:
        limits = RiskLimits(max_daily_loss=1.0, max_drawdown=1.0,
                            min_equity_frac=0.0)
        pt = replay(close, 10_000, Path(d) / "j.csv", limits)
    w = strategy.target_weight_series(close)
    res = backtest.run(close, w, 50.0)
    vec_final = 10_000 * float(res.equity.iloc[-1])
    diff = abs(pt.equity - vec_final) / vec_final
    assert diff < 0.005, f"paper vs vectorized differ by {diff:.4%}"


if __name__ == "__main__":
    fns = [v for k, v in list(globals().items()) if k.startswith("test_")]
    for fn in fns:
        fn()
        print(f"PASS {fn.__name__}")
    print(f"{len(fns)} risk/paper tests passed")

"""Backtester validation with known expected outcomes (Backtest Auditor rule).
Run: python3 -m pytest tests/ -q  (or python3 tests/test_backtest.py)
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
import backtest


def idx(n):
    return pd.date_range("2020-01-01", periods=n, freq="D")


def test_zero_weight_zero_return():
    close = pd.Series(np.linspace(100, 200, 50), index=idx(50))
    res = backtest.run(close, pd.Series(0.0, index=close.index), 25)
    assert abs(res.equity.iloc[-1] - 1.0) < 1e-12
    assert res.trades == 0


def test_full_weight_tracks_asset_minus_entry_cost():
    close = pd.Series([100, 110, 121, 133.1], index=idx(4), dtype=float)
    res = backtest.run(close, pd.Series(1.0, index=close.index), 100)  # 1% side
    # weight held from day1 (next-bar). Entry cost 1% on day1.
    expected = (1 + 0.10 - 0.01) * 1.10 * 1.10
    assert abs(res.equity.iloc[-1] - expected) < 1e-9
    assert res.trades == 1


def test_no_lookahead():
    """Signal fires on the LAST bar -> can never be held -> zero P&L."""
    close = pd.Series([100.0] * 9 + [200.0], index=idx(10))
    w = pd.Series(0.0, index=close.index)
    w.iloc[-1] = 1.0  # decided at the final close; no next bar to hold
    res = backtest.run(close, w, 0)
    assert abs(res.equity.iloc[-1] - 1.0) < 1e-12


def test_costs_scale_with_turnover():
    close = pd.Series(100.0, index=idx(100))  # flat price: only costs matter
    w = pd.Series([1.0, 0.0] * 50, index=close.index)  # flip daily
    res = backtest.run(close, w, 50)  # 0.5% per side
    # 99 changes of |dw|=1 (+ initial 0->1 shift edge): equity ~ (1-0.005)^n
    n_changes = (res.weights.diff().abs() > 0).sum() + (res.weights.iloc[0] > 0)
    expected = (1 - 0.005) ** n_changes
    assert abs(res.equity.iloc[-1] - expected) < 1e-9


def test_long_only_clip():
    close = pd.Series(np.linspace(100, 50, 30), index=idx(30))
    w = pd.Series(-1.0, index=close.index)  # tries to short
    res = backtest.run(close, w, 25)
    assert abs(res.equity.iloc[-1] - 1.0) < 1e-12  # clipped to 0


if __name__ == "__main__":
    fns = [v for k, v in list(globals().items()) if k.startswith("test_")]
    for fn in fns:
        fn()
        print(f"PASS {fn.__name__}")
    print(f"{len(fns)} backtester validation tests passed")

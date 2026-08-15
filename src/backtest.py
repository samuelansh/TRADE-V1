"""Daily-bar backtester with realistic cost model.

Deliberately simple and auditable (vectorized, close-to-close) but honest:
- signals computed on close of day t are executed at close of day t+1
  (next-bar execution: no look-ahead)
- every position CHANGE pays: spread/2 + slippage + commission (round-trip
  costs split per side), scaled by the size of the change
- supports fractional target weights in [0, 1] (long-only for now)

Cost presets (per side, in bps of notional):
  spot_tight : 10 bps  (good crypto spot exchange)
  cfd_base   : 25 bps  (typical MT5 CFD all-in)
  cfd_stress : 50 bps  (pessimistic stress, Master Prompt §14)
"""
from dataclasses import dataclass

import numpy as np
import pandas as pd

COST_PRESETS_BPS = {"spot_tight": 10.0, "cfd_base": 25.0, "cfd_stress": 50.0}


@dataclass
class Result:
    equity: pd.Series
    weights: pd.Series
    trades: int
    turnover: float
    stats: dict


def run(close: pd.Series, target_weight: pd.Series, cost_bps_per_side: float,
        periods_per_year: int = 365,
        financing_annual: float = 0.0) -> Result:
    """close: price series. target_weight: desired exposure decided at each
    close (will be applied at the NEXT close). Both indexed identically.
    financing_annual: overnight financing on held notional (e.g. 0.10 = 10%/yr
    long-CFD financing), charged daily on the held weight."""
    close = close.astype(float)
    ret = close.pct_change().fillna(0.0)

    # next-bar execution: weight held during day t is the target decided at t-1
    w_held = target_weight.shift(1).fillna(0.0).clip(0.0, 1.0)

    # position changes happen at the close where the new target takes effect
    dw = w_held.diff().abs().fillna(w_held.iloc[0] if len(w_held) else 0.0)
    cost = dw * (cost_bps_per_side / 1e4)
    cost = cost + w_held * (financing_annual / periods_per_year)

    strat_ret = w_held * ret - cost
    equity = (1.0 + strat_ret).cumprod()

    stats = compute_stats(strat_ret, equity, periods_per_year)
    trades = int((dw > 1e-9).sum())
    turnover = float(dw.sum())
    return Result(equity, w_held, trades, turnover, stats)


def compute_stats(r: pd.Series, equity: pd.Series, ppy: int) -> dict:
    r = r.dropna()
    n = len(r)
    if n == 0:
        return {}
    ann_ret = float((1 + r).prod() ** (ppy / n) - 1)
    ann_vol = float(r.std() * np.sqrt(ppy))
    sharpe = ann_ret / ann_vol if ann_vol > 0 else np.nan
    downside = r[r < 0].std() * np.sqrt(ppy)
    sortino = ann_ret / downside if downside and downside > 0 else np.nan
    dd = (equity / equity.cummax() - 1.0)
    max_dd = float(dd.min())
    exposure = float((r != 0).mean())
    return {
        "ann_return": round(ann_ret, 4), "ann_vol": round(ann_vol, 4),
        "sharpe": round(sharpe, 3), "sortino": round(float(sortino), 3),
        "max_drawdown": round(max_dd, 4), "n_days": n,
        "exposure_frac": round(exposure, 3),
        "total_return": round(float(equity.iloc[-1] / equity.iloc[0] - 1), 4),
    }

"""Frozen candidate v1 (params locked in research/VALIDATION_PREREG.md).

TSMOM ensemble lookbacks {60,90,120,180,250} x vol-target(win=30, tgt=0.6),
long-only, weight capped at 1. Pure function: prices in -> target weight out.
No I/O, no state, no access to anything but the given price history.
"""
import numpy as np
import pandas as pd

LOOKBACKS = (60, 90, 120, 180, 250)
VOL_WIN = 30
TGT_VOL = 0.6
MIN_HISTORY = max(LOOKBACKS) + 1


def target_weight(close: pd.Series) -> float:
    """Desired exposure in [0,1] decided at the latest close.
    Returns 0.0 if history is insufficient (NO TRADE is a valid output)."""
    close = close.dropna()
    if len(close) < MIN_HISTORY:
        return 0.0
    sig = float(np.mean([close.iloc[-1] > close.iloc[-1 - lb]
                         for lb in LOOKBACKS]))
    rv = close.pct_change().iloc[-VOL_WIN:].std() * np.sqrt(365)
    if not np.isfinite(rv) or rv <= 0:
        return 0.0
    scale = min(1.0, TGT_VOL / rv)
    return float(np.clip(sig * scale, 0.0, 1.0))


def target_weight_series(close: pd.Series) -> pd.Series:
    """Vectorized version for backtests. Identical math to target_weight."""
    sig = sum((close > close.shift(lb)).astype(float)
              for lb in LOOKBACKS) / len(LOOKBACKS)
    rv = close.pct_change().rolling(VOL_WIN).std() * np.sqrt(365)
    scale = (TGT_VOL / rv).clip(upper=1.0)
    w = (sig * scale).clip(0.0, 1.0).fillna(0.0)
    w.iloc[:MIN_HISTORY] = 0.0
    return w

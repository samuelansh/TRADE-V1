"""Independent risk engine (Master Prompt §18).

SIGNAL -> RISK VALIDATION -> ORDER. The strategy cannot bypass it: the paper
trader and any future MT5 layer only accept weights that passed check().

All limits are hard construction-time constants; the strategy module has no
import path to modify them. Default response to any uncertainty: NO TRADE
(target weight forced to 0 / HALT).
"""
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone


@dataclass
class RiskLimits:
    max_weight: float = 1.0            # no leverage, long-only
    max_daily_loss: float = 0.05       # 5% of equity in one day -> flatten+halt
    max_drawdown: float = 0.25         # 25% from equity peak -> flatten+halt
    max_data_age_days: float = 2.0     # stale data -> no new exposure
    max_daily_move: float = 0.30       # |ret|>30% = abnormal market or bad data
    min_equity_frac: float = 0.5       # equity below 50% of start -> halt


@dataclass
class RiskState:
    start_equity: float
    peak_equity: float
    day_start_equity: float
    day: str = ""
    halted: bool = False
    halt_reason: str = ""
    log: list = field(default_factory=list)


class RiskEngine:
    def __init__(self, start_equity: float, limits: RiskLimits = None):
        self.limits = limits or RiskLimits()
        self.state = RiskState(start_equity, start_equity, start_equity)

    def check(self, desired_weight: float, equity: float,
              last_price_time: datetime, now: datetime,
              last_return: float) -> tuple:
        """Returns (approved_weight, reason). Never raises to caller."""
        lim, st = self.limits, self.state
        try:
            day = now.strftime("%Y-%m-%d")
            if day != st.day:
                st.day, st.day_start_equity = day, equity
            st.peak_equity = max(st.peak_equity, equity)

            if st.halted:
                return 0.0, f"HALTED: {st.halt_reason}"
            # kill-switches (flatten and halt)
            if equity <= st.start_equity * lim.min_equity_frac:
                return self._halt("equity below min_equity_frac")
            if equity <= st.peak_equity * (1 - lim.max_drawdown):
                return self._halt("max_drawdown breached")
            if equity <= st.day_start_equity * (1 - lim.max_daily_loss):
                return self._halt("max_daily_loss breached")
            # no-new-risk conditions (hold 0, don't halt)
            age = now - last_price_time
            if age > timedelta(days=lim.max_data_age_days):
                return 0.0, f"NO TRADE: stale data ({age})"
            if last_return is not None and abs(last_return) > lim.max_daily_move:
                return 0.0, "NO TRADE: abnormal daily move (data/market anomaly)"
            if not (0.0 <= desired_weight <= lim.max_weight):
                w = min(max(desired_weight, 0.0), lim.max_weight)
                return w, f"CLIPPED from {desired_weight:.3f}"
            return float(desired_weight), "OK"
        except Exception as e:  # uncertainty -> NO TRADE
            return 0.0, f"NO TRADE: risk engine error {e!r}"

    def _halt(self, reason):
        self.state.halted = True
        self.state.halt_reason = reason
        self.state.log.append((self.state.day, reason))
        return 0.0, f"HALT: {reason}"

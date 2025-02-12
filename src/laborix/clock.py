"""Injectable clocks for deterministic timeout and budget tests."""

import time
from typing import Protocol


class Clock(Protocol):
    """Minimal monotonic clock interface."""

    def now(self) -> float: ...


class SystemClock:
    """Production monotonic clock."""

    def now(self) -> float:
        return time.monotonic()


class ManualClock:
    """Explicitly advanced clock for offline simulations."""

    def __init__(self, start: float = 0.0) -> None:
        self._value = start

    def now(self) -> float:
        return self._value

    def advance(self, seconds: float) -> None:
        if seconds < 0:
            raise ValueError("clock cannot move backwards")
        self._value += seconds


def elapsed_seconds(clock: Clock, started_at: float) -> float:
    """Return a nonnegative elapsed duration despite a faulty clock."""
    return max(0.0, clock.now() - started_at)

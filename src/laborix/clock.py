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

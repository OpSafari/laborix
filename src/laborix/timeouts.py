from dataclasses import dataclass


@dataclass(frozen=True)
class Deadline:
    started: float
    timeout: float

    def remaining(self, now: float) -> float:
        return max(0.0, self.timeout - (now - self.started))

    def expired(self, now: float) -> bool:
        return self.remaining(now) <= 0

"""Bandit scheduling over deterministic synthetic reward surfaces."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

import numpy as np


class Surface(Protocol):
    def reward(self, arm: int, run: int, seed: int) -> float: ...


@dataclass(frozen=True)
class StationarySurface:
    means: tuple[float, ...]
    noise: float = 0.0

    def reward(self, arm: int, run: int, seed: int) -> float:
        return float(
            self.means[arm] + np.random.default_rng(seed + run * 997 + arm).normal(0, self.noise)
        )

    def oracle(self) -> tuple[int, float]:
        arm = max(range(len(self.means)), key=self.means.__getitem__)
        return arm, self.means[arm]

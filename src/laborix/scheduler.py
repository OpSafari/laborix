"""Bandit scheduling over deterministic synthetic reward surfaces."""

from __future__ import annotations

import math
from dataclasses import dataclass, field
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


@dataclass(frozen=True)
class Budget:
    max_runs: int
    max_seconds: float | None = None

    def allows(self, runs: int, elapsed: float) -> bool:
        return runs < self.max_runs and (self.max_seconds is None or elapsed < self.max_seconds)


@dataclass
class UCB1:
    arms: int
    counts: list[int] = field(init=False)
    totals: list[float] = field(init=False)

    def __post_init__(self) -> None:
        self.counts = [0] * self.arms
        self.totals = [0.0] * self.arms

    def select(self) -> int:
        for arm, count in enumerate(self.counts):
            if count == 0:
                return arm
        total = sum(self.counts)
        return max(
            range(self.arms),
            key=lambda a: (
                self.totals[a] / self.counts[a] + math.sqrt(2 * math.log(total) / self.counts[a])
            ),
        )

    def update(self, arm: int, reward: float) -> None:
        self.counts[arm] += 1
        self.totals[arm] += reward


@dataclass
class Thompson:
    arms: int
    seed: int = 0

    def __post_init__(self) -> None:
        self.alpha = [1.0] * self.arms
        self.beta = [1.0] * self.arms
        self.rng = np.random.default_rng(self.seed)

    def select(self) -> int:
        return int(np.argmax(self.rng.beta(self.alpha, self.beta)))

    def update(self, arm: int, reward: float) -> None:
        clipped = min(1.0, max(0.0, reward))
        self.alpha[arm] += clipped
        self.beta[arm] += 1 - clipped


@dataclass
class SlidingWindowUCB:
    arms: int
    window: int
    history: list[tuple[int, float]] = field(default_factory=list)

    def select(self) -> int:
        recent = self.history[-self.window :]
        counts = [sum(a == i for a, _ in recent) for i in range(self.arms)]
        if 0 in counts:
            return counts.index(0)
        totals = [sum(r for a, r in recent if a == i) for i in range(self.arms)]
        n = len(recent)
        return max(
            range(self.arms),
            key=lambda a: totals[a] / counts[a] + math.sqrt(2 * math.log(n) / counts[a]),
        )

    def update(self, arm: int, reward: float) -> None:
        self.history.append((arm, reward))


@dataclass(frozen=True)
class Observation:
    run: int
    arm: int
    reward: float
    regret: float


def schedule(
    surface: StationarySurface, policy: object, budget: Budget, seed: int = 0
) -> tuple[Observation, ...]:
    result = []
    _, best = surface.oracle()
    while budget.allows(len(result), float(len(result))):
        arm = policy.select()
        reward = surface.reward(arm, len(result), seed)
        policy.update(arm, reward)
        result.append(Observation(len(result), arm, reward, best - reward))
    return tuple(result)


def cumulative_regret(trace: tuple[Observation, ...]) -> tuple[float, ...]:
    total = 0.0
    values = []
    for item in trace:
        total += item.regret
        values.append(total)
    return tuple(values)

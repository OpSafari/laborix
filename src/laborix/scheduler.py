"""Bandit scheduling over deterministic synthetic reward surfaces."""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Protocol

import numpy as np


class Surface(Protocol):
    def reward(self, arm: int, run: int, seed: int) -> float: ...


class Policy(Protocol):
    def select(self) -> int: ...

    def update(self, arm: int, reward: float) -> None: ...


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
    exploration: float = 2.0
    counts: list[int] = field(init=False)
    totals: list[float] = field(init=False)

    def __post_init__(self) -> None:
        if self.arms < 1:
            raise ValueError("arms must be positive")
        if not math.isfinite(self.exploration) or self.exploration < 0:
            raise ValueError("exploration must be finite and non-negative")
        self.counts = [0] * self.arms
        self.totals = [0.0] * self.arms

    def means(self) -> tuple[float | None, ...]:
        return tuple(
            None if count == 0 else self.totals[a] / count for a, count in enumerate(self.counts)
        )

    def confidence_radii(self) -> tuple[float, ...]:
        total = sum(self.counts)
        if total == 0:
            return (math.inf,) * self.arms
        return tuple(
            math.inf if count == 0 else math.sqrt(self.exploration * math.log(total) / count)
            for count in self.counts
        )

    def scores(self) -> tuple[float, ...]:
        return tuple(
            math.inf if mean is None else mean + radius
            for mean, radius in zip(self.means(), self.confidence_radii(), strict=True)
        )

    def select(self) -> int:
        for arm, count in enumerate(self.counts):
            if count == 0:
                return arm
        scores = self.scores()
        return max(range(self.arms), key=lambda arm: (scores[arm], -arm))

    def update(self, arm: int, reward: float) -> None:
        if not 0 <= arm < self.arms:
            raise IndexError(f"arm out of range: {arm}")
        if not math.isfinite(reward):
            raise ValueError("reward must be finite")
        self.counts[arm] += 1
        self.totals[arm] += reward

    def snapshot(self) -> dict[str, object]:
        return {
            "policy": "ucb1",
            "arms": self.arms,
            "exploration": self.exploration,
            "counts": list(self.counts),
            "totals": list(self.totals),
        }


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
    surface: StationarySurface, policy: Policy, budget: Budget, seed: int = 0
) -> tuple[Observation, ...]:
    result: list[Observation] = []
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

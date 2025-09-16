"""Versioned research-program plan values and validation."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

from laborix.errors import ValidationError


class Stage(StrEnum):
    LITERATURE = "literature"
    IDEATION = "ideation"
    DATA_PREP = "data-prep"
    EXPERIMENT = "experiment"
    ANALYSIS = "analysis"
    REPORT = "report"


@dataclass(frozen=True)
class Port:
    name: str
    kind: str = "json"


@dataclass(frozen=True)
class Resources:
    cpu: int = 1
    memory_mb: int = 256
    wall_seconds: float = 60.0

    def validate(self) -> None:
        if self.cpu < 1 or self.memory_mb < 1 or self.wall_seconds <= 0:
            raise ValidationError("resources must be positive")


@dataclass(frozen=True)
class RetryPolicy:
    attempts: int = 1
    delay_seconds: float = 0.0
    jitter: float = 0.0

    def validate(self) -> None:
        if self.attempts < 1:
            raise ValidationError("retry attempts must be at least one")
        if self.delay_seconds < 0 or not 0 <= self.jitter <= 1:
            raise ValidationError("invalid retry timing")


@dataclass(frozen=True)
class Step:
    id: str
    stage: Stage
    operation: str
    dependencies: tuple[str, ...] = ()
    inputs: dict[str, str] = field(default_factory=dict)
    outputs: tuple[Port, ...] = ()
    config: dict[str, Any] = field(default_factory=dict)
    resources: Resources = field(default_factory=Resources)
    retry: RetryPolicy = field(default_factory=RetryPolicy)


@dataclass(frozen=True)
class Plan:
    name: str
    steps: tuple[Step, ...]
    schema_version: str = "2.0"
    seed: int = 0


def _ids(plan: Plan) -> dict[str, Step]:
    result: dict[str, Step] = {}
    for step in plan.steps:
        if not re.fullmatch(r"[a-z][a-z0-9_-]*", step.id):
            raise ValidationError(f"invalid step id: {step.id}")
        if step.id in result:
            raise ValidationError(f"duplicate step id: {step.id}")
        result[step.id] = step
    return result

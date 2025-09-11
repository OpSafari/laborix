"""Versioned research-program plan values and validation."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

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

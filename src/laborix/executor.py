"""Deterministic in-process plan executor with ledger-backed resume."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from laborix.artifacts import ArtifactStore
from laborix.ledger import Ledger
from laborix.registry import StepRegistry


@dataclass(frozen=True)
class RunResult:
    outputs: dict[str, dict[str, Any]]
    completed: tuple[str, ...]
    failed: str | None = None


class Executor:
    def __init__(self, registry: StepRegistry, run_dir: Path):
        self.registry = registry
        self.store = ArtifactStore(Path(run_dir) / "artifacts")
        self.ledger = Ledger(Path(run_dir) / "ledger.jsonl")

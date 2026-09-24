"""Deterministic in-process plan executor with ledger-backed resume."""

from __future__ import annotations

import threading
import time
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np

from laborix.artifacts import ArtifactRef, ArtifactStore
from laborix.ledger import Ledger, LedgerRecord
from laborix.plan import Plan, topological_order
from laborix.records import derive_seed, value_digest

Operation = Callable[[dict[str, Any], dict[str, Any], int], dict[str, Any]]


class StepRegistry:
    def __init__(self) -> None:
        self._items: dict[str, Operation] = {}

    def register(self, name: str, operation: Operation) -> None:
        if not name or name in self._items:
            raise ValueError(f"operation already registered or empty: {name}")
        self._items[name] = operation

    def resolve(self, name: str) -> Operation:
        try:
            return self._items[name]
        except KeyError as error:
            raise KeyError(f"unknown operation: {name}") from error

    @property
    def names(self) -> tuple[str, ...]:
        return tuple(sorted(self._items))


class CancellationToken:
    def __init__(self) -> None:
        self._event = threading.Event()

    def cancel(self) -> None:
        self._event.set()

    @property
    def cancelled(self) -> bool:
        return self._event.is_set()


@dataclass(frozen=True)
class Deadline:
    started: float
    timeout: float

    def remaining(self, now: float) -> float:
        return max(0.0, self.timeout - (now - self.started))

    def expired(self, now: float) -> bool:
        return self.remaining(now) <= 0


def bounded_batches(values: Sequence[str], limit: int) -> tuple[tuple[str, ...], ...]:
    if limit < 1:
        raise ValueError("parallelism must be positive")
    ordered = sorted(values)
    return tuple(tuple(ordered[i : i + limit]) for i in range(0, len(ordered), limit))


def generate(inputs: dict[str, Any], config: dict[str, Any], seed: int) -> dict[str, Any]:
    rng = np.random.default_rng(seed)
    return {"values": rng.normal(size=int(config.get("count", 32))).tolist()}


def summarize(inputs: dict[str, Any], config: dict[str, Any], seed: int) -> dict[str, Any]:
    values = np.asarray(inputs["values"], dtype=float)
    return {"mean": float(values.mean()), "std": float(values.std())}


def compare(inputs: dict[str, Any], config: dict[str, Any], seed: int) -> dict[str, Any]:
    return {"difference": float(inputs["candidate"] - inputs["baseline"])}


def builtins() -> StepRegistry:
    registry = StepRegistry()
    registry.register("synthetic.generate", generate)
    registry.register("synthetic.summarize", summarize)
    registry.register("synthetic.compare", compare)
    return registry


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

    def run(self, plan: Plan, resume: bool = False) -> RunResult:
        by_id = {s.id: s for s in plan.steps}
        outputs: dict[str, dict[str, Any]] = {}
        completed = []
        prior = self.ledger.successful_steps() if resume else {}
        for step_id in topological_order(plan):
            step = by_id[step_id]
            if step_id in prior and prior[step_id].get("outputs_hash"):
                raw = prior[step_id]
                ref = ArtifactRef(
                    str(raw["outputs_hash"]), int((self.store.root / f"{step.id}.size").read_text())
                )
                outputs[step_id] = self.store.get_json(ref)
                completed.append(step_id)
                continue
            inputs = {
                name: outputs[source][port]
                for name, reference in step.inputs.items()
                for source, port in [reference.split(".", 1)]
            }
            for attempt in range(1, step.retry.attempts + 1):
                started = time.monotonic()
                try:
                    result = self.registry.resolve(step.operation)(
                        inputs, step.config, derive_seed(plan.seed, step.id)
                    )
                    ref = self.store.put_json(result)
                    record = LedgerRecord(
                        step.id,
                        attempt,
                        value_digest(inputs),
                        "0.1.0",
                        value_digest(step.config),
                        derive_seed(plan.seed, step.id),
                        ref.digest,
                        time.monotonic() - started,
                        "success",
                    )
                    self.ledger.append(record)
                    (self.store.root / f"{step.id}.size").write_text(str(ref.size))
                    outputs[step.id] = result
                    completed.append(step.id)
                    break
                except Exception:
                    self.ledger.append(
                        LedgerRecord(
                            step.id,
                            attempt,
                            value_digest(inputs),
                            "0.1.0",
                            value_digest(step.config),
                            derive_seed(plan.seed, step.id),
                            None,
                            time.monotonic() - started,
                            "failed",
                        )
                    )
                    if attempt == step.retry.attempts:
                        return RunResult(outputs, tuple(completed), step.id)
        return RunResult(outputs, tuple(completed))

    def _rewrite(self, records: list[dict[str, Any]]) -> None:
        self.ledger.path.write_text(
            "".join(
                __import__("json").dumps(x, sort_keys=True, separators=(",", ":")) + "\n"
                for x in records
            )
        )

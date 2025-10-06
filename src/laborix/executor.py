"""Deterministic in-process plan executor with ledger-backed resume."""

from __future__ import annotations

import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from laborix.artifacts import ArtifactRef, ArtifactStore
from laborix.hashing import value_digest
from laborix.ledger import Ledger, LedgerRecord
from laborix.plan import Plan, topological_order
from laborix.registry import StepRegistry
from laborix.seeds import derive_seed


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
                ref = ArtifactRef(str(raw["outputs_hash"]), int(raw["output_size"]))
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
                    raw = self.ledger.append(record)
                    raw["output_size"] = ref.size
                    lines = list(self.ledger.records())
                    lines[-1]["output_size"] = ref.size
                    self._rewrite(lines)
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

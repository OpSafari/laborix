"""Append-only, hash-chained provenance ledger."""

from __future__ import annotations

import json
from collections.abc import Iterator
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from laborix.hashing import value_digest
from laborix.redaction import assert_no_secrets


@dataclass(frozen=True)
class LedgerRecord:
    step_id: str
    attempt: int
    inputs_hash: str
    code_version: str
    config_hash: str
    seed: int
    outputs_hash: str | None
    wall_seconds: float
    status: str
    previous_hash: str = "0" * 64
    record_hash: str = ""


class Ledger:
    def __init__(self, path: Path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def records(self) -> Iterator[dict[str, Any]]:
        if not self.path.exists():
            return
        for line in self.path.read_text().splitlines():
            if line:
                yield json.loads(line)

    def append(self, record: LedgerRecord) -> dict[str, Any]:
        raw = asdict(record)
        assert_no_secrets(raw)
        prior = list(self.records())
        raw["previous_hash"] = prior[-1]["record_hash"] if prior else "0" * 64
        raw["record_hash"] = ""
        raw["record_hash"] = value_digest(raw)
        with self.path.open("a", encoding="utf-8") as out:
            out.write(json.dumps(raw, sort_keys=True, separators=(",", ":")) + "\n")
        return raw

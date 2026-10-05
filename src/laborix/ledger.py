"""Append-only, hash-chained provenance ledger."""

from __future__ import annotations

import json
import os
from collections.abc import Iterator
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from laborix.records import assert_no_secrets, value_digest


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
            out.flush()
            os.fsync(out.fileno())
        self.head_path.write_text(str(raw["record_hash"]) + "\n")
        return raw

    @property
    def head_path(self) -> Path:
        return self.path.with_suffix(self.path.suffix + ".head")

    def verify(self) -> tuple[bool, str]:
        previous = "0" * 64
        required = set(LedgerRecord.__dataclass_fields__)
        try:
            records = list(self.records())
        except (json.JSONDecodeError, UnicodeDecodeError) as error:
            return False, f"malformed JSONL: {error.msg}"
        for index, raw in enumerate(records, 1):
            missing = required - raw.keys()
            extra = raw.keys() - required
            if missing:
                return False, f"record {index} missing field: {min(missing)}"
            if extra:
                return False, f"record {index} unknown field: {min(extra)}"
            if raw["status"] not in {"success", "failed", "cancelled", "timeout"}:
                return False, f"record {index} invalid status: {raw['status']}"
            if not isinstance(raw["attempt"], int) or raw["attempt"] < 1:
                return False, f"record {index} invalid attempt"
            if raw.get("previous_hash") != previous:
                return False, f"record {index} previous hash mismatch"
            claimed = raw.get("record_hash")
            candidate = dict(raw)
            candidate["record_hash"] = ""
            if claimed != value_digest(candidate):
                return False, f"record {index} content hash mismatch"
            previous = str(claimed)
        if self.head_path.exists() and self.head_path.read_text().strip() != previous:
            return False, "ledger head mismatch (possible truncation)"
        return True, "ok"

    def successful_steps(self) -> dict[str, dict[str, Any]]:
        return {str(r["step_id"]): r for r in self.records() if r["status"] == "success"}

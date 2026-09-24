"""Canonical values, reproducibility metadata, and provenance record queries."""

from __future__ import annotations

import hashlib
import json
import platform
from collections.abc import Iterable
from dataclasses import asdict, dataclass
from typing import Any

import numpy as np

from laborix import __version__

SECRET_FRAGMENTS = ("api_key", "apikey", "authorization", "password", "secret", "token")


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def strict_canonical_json(value: Any) -> str:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False
    )


def value_digest(value: Any) -> str:
    return hashlib.sha256(strict_canonical_json(value).encode("utf-8")).hexdigest()


def bytes_digest(chunks: Iterable[bytes]) -> str:
    digest = hashlib.sha256()
    for chunk in chunks:
        digest.update(chunk)
    return digest.hexdigest()


def derive_seed(root: int, namespace: str) -> int:
    payload = f"{root}:{namespace}".encode()
    return int.from_bytes(hashlib.sha256(payload).digest()[:4], "big")


def validate_seed(seed: int) -> int:
    if isinstance(seed, bool) or not isinstance(seed, int) or not 0 <= seed < 2**32:
        raise ValueError("seed must be an integer in [0, 2**32)")
    return seed


def is_secret_key(key: str) -> bool:
    normalized = key.lower().replace("-", "_")
    return any(fragment in normalized for fragment in SECRET_FRAGMENTS)


def redact(value: object) -> object:
    if isinstance(value, dict):
        return {
            str(key): "[REDACTED]" if is_secret_key(str(key)) else redact(item)
            for key, item in value.items()
        }
    if isinstance(value, (list, tuple)):
        return [redact(item) for item in value]
    return value


def redact_sequence(values: list[object] | tuple[object, ...]) -> list[object]:
    return [redact(item) for item in values]


def assert_no_secrets(value: object, path: str = "$") -> None:
    if isinstance(value, dict):
        for key, item in value.items():
            if is_secret_key(str(key)):
                raise ValueError(f"secret-like key at {path}.{key}")
            assert_no_secrets(item, f"{path}.{key}")
    elif isinstance(value, (list, tuple)):
        for index, item in enumerate(value):
            assert_no_secrets(item, f"{path}[{index}]")


@dataclass(frozen=True)
class RunMetadata:
    schema_version: str
    laborix_version: str
    python_version: str
    numpy_version: str
    seed: int
    config_hash: str


def metadata(config: object, seed: int) -> RunMetadata:
    return RunMetadata(
        "1.0", __version__, platform.python_version(), np.__version__, seed, value_digest(config)
    )


def metadata_dict(value: RunMetadata) -> dict[str, object]:
    return asdict(value)


def statuses(records: Iterable[dict[str, Any]]):
    """Compute statuses from ledger-shaped records."""
    records = tuple(records)
    return tuple(str(r.get("status", "")) for r in records)


def successful(records: Iterable[dict[str, Any]]):
    """Compute successful from ledger-shaped records."""
    records = tuple(records)
    return tuple(r for r in records if r.get("status") == "success")


def failed(records: Iterable[dict[str, Any]]):
    """Compute failed from ledger-shaped records."""
    records = tuple(records)
    return tuple(r for r in records if r.get("status") == "failed")


def step_names(records: Iterable[dict[str, Any]]):
    """Compute step names from ledger-shaped records."""
    records = tuple(records)
    return tuple(dict.fromkeys(str(r.get("step_id", "")) for r in records))


def attempt_total(records: Iterable[dict[str, Any]]):
    """Compute attempt total from ledger-shaped records."""
    records = tuple(records)
    return sum(int(r.get("attempt", 0)) for r in records)


def wall_total(records: Iterable[dict[str, Any]]):
    """Compute wall total from ledger-shaped records."""
    records = tuple(records)
    return sum(float(r.get("wall_seconds", 0)) for r in records)


def last_record(records: Iterable[dict[str, Any]]):
    """Compute last record from ledger-shaped records."""
    records = tuple(records)
    return tuple(records)[-1] if tuple(records) else None


def record_count(records: Iterable[dict[str, Any]]):
    """Compute record count from ledger-shaped records."""
    records = tuple(records)
    return sum(1 for _ in records)


def status_counts(records: Iterable[dict[str, Any]]):
    """Compute status counts from ledger-shaped records."""
    records = tuple(records)
    return {  # noqa: E501
        status: sum(record.get("status") == status for record in records)
        for status in sorted({str(record.get("status")) for record in records})
    }


def seeds(records: Iterable[dict[str, Any]]):
    """Compute seeds from ledger-shaped records."""
    records = tuple(records)
    return tuple(int(r["seed"]) for r in records if "seed" in r)  # noqa: E501


def code_versions(records: Iterable[dict[str, Any]]):
    """Compute code versions from ledger-shaped records."""
    records = tuple(records)
    return tuple(sorted({str(r.get("code_version")) for r in records}))  # noqa: E501


def output_hashes(records: Iterable[dict[str, Any]]):
    """Compute output hashes from ledger-shaped records."""
    records = tuple(records)
    return tuple(str(r["outputs_hash"]) for r in records if r.get("outputs_hash"))  # noqa: E501


def latest_by_step(records: Iterable[dict[str, Any]]):
    """Compute latest by step from ledger-shaped records."""
    records = tuple(records)
    return {str(r["step_id"]): r for r in records}  # noqa: E501


def attempts_by_step(records: Iterable[dict[str, Any]]):
    """Compute attempts by step from ledger-shaped records."""
    records = tuple(records)
    return {
        s: sum(r.get("step_id") == s for r in records)
        for s in sorted({str(r.get("step_id")) for r in records})
    }  # noqa: E501


def has_failures(records: Iterable[dict[str, Any]]):
    """Compute has failures from ledger-shaped records."""
    records = tuple(records)
    return any(r.get("status") == "failed" for r in records)  # noqa: E501

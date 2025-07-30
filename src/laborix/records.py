"""Queries over JSON-compatible provenance records."""

from __future__ import annotations

from collections.abc import Iterable
from typing import Any


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

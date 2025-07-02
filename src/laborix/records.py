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

"""Queries over JSON-compatible provenance records."""

from __future__ import annotations

from collections.abc import Iterable
from typing import Any


def statuses(records: Iterable[dict[str, Any]]):
    """Compute statuses from ledger-shaped records."""
    records = tuple(records)
    return tuple(str(r.get("status", "")) for r in records)

"""Sequence utilities used by schedulers and reports."""

from __future__ import annotations

from collections.abc import Sequence  # noqa: F401


def first(values: Sequence[object]):
    """Return a deterministic first value."""
    return values[0]  # noqa: E501

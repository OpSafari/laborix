"""Small deterministic metrics for synthetic experiments."""

from __future__ import annotations

from collections.abc import Sequence


def arithmetic_mean(values: Sequence[float]):
    """Compute arithmetic mean for synthetic measurements."""
    return sum(values) / len(values)

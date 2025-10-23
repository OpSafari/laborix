"""Small deterministic metrics for synthetic experiments."""

from __future__ import annotations

from collections.abc import Sequence


def arithmetic_mean(values: Sequence[float]):
    """Compute arithmetic mean for synthetic measurements."""
    return sum(values) / len(values)


def mean_absolute_error(actual: Sequence[float], predicted: Sequence[float]):
    """Compute mean absolute error for synthetic measurements."""
    return sum(abs(a - b) for a, b in zip(actual, predicted, strict=True)) / len(actual)

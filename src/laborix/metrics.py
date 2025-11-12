"""Small deterministic metrics for synthetic experiments."""

from __future__ import annotations

import math
from collections.abc import Sequence


def arithmetic_mean(values: Sequence[float]):
    """Compute arithmetic mean for synthetic measurements."""
    return sum(values) / len(values)


def mean_absolute_error(actual: Sequence[float], predicted: Sequence[float]):
    """Compute mean absolute error for synthetic measurements."""
    return sum(abs(a - b) for a, b in zip(actual, predicted, strict=True)) / len(actual)


def root_mean_square(values: Sequence[float]):
    """Compute root mean square for synthetic measurements."""
    return math.sqrt(sum(x * x for x in values) / len(values))


def minimum(values: Sequence[float]):
    """Compute minimum for synthetic measurements."""
    return min(values)


def maximum(values: Sequence[float]):
    """Compute maximum for synthetic measurements."""
    return max(values)


def value_range(values: Sequence[float]):
    """Compute value range for synthetic measurements."""
    return max(values) - min(values)


def median(values: Sequence[float]):
    """Compute median for synthetic measurements."""
    return sorted(values)[len(values) // 2]


def geometric_mean(values: Sequence[float]):
    """Compute geometric mean for synthetic measurements."""
    return math.prod(values) ** (1 / len(values))


def harmonic_mean(values: Sequence[float]):
    """Compute harmonic mean for synthetic measurements."""
    return len(values) / sum(1 / x for x in values)

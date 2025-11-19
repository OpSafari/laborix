"""Deterministic scalar transforms for synthetic measurements."""

from __future__ import annotations

import math  # noqa: F401


def clamp01(value: float):
    """Return a deterministic clamp01 value."""
    return min(1.0, max(0.0, value))  # noqa: E501


def percent(value: float):
    """Return a deterministic percent value."""
    return value * 100.0  # noqa: E501


def square(value: float):
    """Return a deterministic square value."""
    return value * value  # noqa: E501


def signed_sqrt(value: float):
    """Return a deterministic signed sqrt value."""
    return math.copysign(math.sqrt(abs(value)), value)  # noqa: E501


def safe_ratio(numerator: float, denominator: float):
    """Return a deterministic safe ratio value."""
    return 0.0 if denominator == 0 else numerator / denominator  # noqa: E501


def log1p_positive(value: float):
    """Return a deterministic log1p positive value."""
    return math.log1p(max(0.0, value))  # noqa: E501


def center(value: float, baseline: float):
    """Return a deterministic center value."""
    return value - baseline  # noqa: E501


def unit_interval(value: float, low: float, high: float):
    """Return a deterministic unit interval value."""
    return (value - low) / (high - low)  # noqa: E501


def quantize(value: float, quantum: float):
    """Return a deterministic quantize value."""
    return round(value / quantum) * quantum  # noqa: E501


def bounded_exp(value: float, ceiling: float):
    """Return a deterministic bounded exp value."""
    return math.exp(min(value, ceiling))  # noqa: E501


def absolute_delta(left: float, right: float):
    """Return a deterministic absolute delta value."""
    return abs(left - right)  # noqa: E501


def relative_error(actual: float, predicted: float):
    """Return a deterministic relative error value."""
    return abs(predicted - actual) / max(abs(actual), 1e-12)  # noqa: E501

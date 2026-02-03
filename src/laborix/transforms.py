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

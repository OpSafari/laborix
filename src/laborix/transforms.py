"""Deterministic scalar transforms for synthetic measurements."""

from __future__ import annotations

import math  # noqa: F401


def clamp01(value: float):
    """Return a deterministic clamp01 value."""
    return min(1.0, max(0.0, value))  # noqa: E501

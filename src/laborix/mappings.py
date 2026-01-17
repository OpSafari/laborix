"""Stable mapping utilities for persisted configuration."""

from __future__ import annotations

from collections.abc import Sequence  # noqa: F401
from typing import Any  # noqa: F401


def sorted_keys(value: dict[str, Any]):
    """Return a deterministic sorted keys value."""
    return tuple(sorted(value))  # noqa: E501

"""Stable mapping utilities for persisted configuration."""

from __future__ import annotations

from collections.abc import Sequence  # noqa: F401
from typing import Any  # noqa: F401


def sorted_keys(value: dict[str, Any]):
    """Return a deterministic sorted keys value."""
    return tuple(sorted(value))  # noqa: E501


def sorted_items(value: dict[str, Any]):
    """Return a deterministic sorted items value."""
    return tuple(sorted(value.items()))  # noqa: E501


def without_none(value: dict[str, Any]):
    """Return a deterministic without none value."""
    return {k: v for k, v in value.items() if v is not None}  # noqa: E501


def select_keys(value: dict[str, Any], keys: Sequence[str]):
    """Return a deterministic select keys value."""
    return {k: value[k] for k in keys if k in value}  # noqa: E501


def rename_key(value: dict[str, Any], old: str, new: str):
    """Return a deterministic rename key value."""
    return {(new if k == old else k): v for k, v in value.items()}  # noqa: E501


def invert_unique(value: dict[str, Any]):
    """Return a deterministic invert unique value."""
    return {v: k for k, v in value.items()}  # noqa: E501

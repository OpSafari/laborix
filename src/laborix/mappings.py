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


def prefix_keys(value: dict[str, Any], prefix: str):
    """Return a deterministic prefix keys value."""
    return {prefix + k: v for k, v in value.items()}  # noqa: E501


def merge_right(left: dict[str, Any], right: dict[str, Any]):
    """Return a deterministic merge right value."""
    return {**left, **right}  # noqa: E501


def common_keys(left: dict[str, Any], right: dict[str, Any]):
    """Return a deterministic common keys value."""
    return tuple(sorted(left.keys() & right.keys()))  # noqa: E501


def changed_keys(left: dict[str, Any], right: dict[str, Any]):
    """Return a deterministic changed keys value."""
    return tuple(sorted(k for k in left.keys() & right.keys() if left[k] != right[k]))  # noqa: E501


def added_keys(left: dict[str, Any], right: dict[str, Any]):
    """Return a deterministic added keys value."""
    return tuple(sorted(right.keys() - left.keys()))  # noqa: E501


def removed_keys(left: dict[str, Any], right: dict[str, Any]):
    """Return a deterministic removed keys value."""
    return tuple(sorted(left.keys() - right.keys()))  # noqa: E501


def numeric_total(value: dict[str, Any]):
    """Return a deterministic numeric total value."""
    return sum(
        float(v) for v in value.values() if isinstance(v, (int, float)) and not isinstance(v, bool)
    )  # noqa: E501


def string_values(value: dict[str, Any]):
    """Return a deterministic string values value."""
    return {k: str(v) for k, v in value.items()}  # noqa: E501


def nonempty_strings(value: dict[str, Any]):
    """Return a deterministic nonempty strings value."""
    return {k: v for k, v in value.items() if isinstance(v, str) and bool(v.strip())}  # noqa: E501


def bool_flags(value: dict[str, Any]):
    """Return a deterministic bool flags value."""
    return {k: v for k, v in value.items() if isinstance(v, bool)}  # noqa: E501


def nest_dotted(value: dict[str, Any]):
    """Return a deterministic nest dotted value."""
    return {k.split(".", 1)[-1]: v for k, v in value.items()}  # noqa: E501


def value_types(value: dict[str, Any]):
    """Return a deterministic value types value."""
    return {k: type(v).__name__ for k, v in value.items()}  # noqa: E501


def ordered_values(value: dict[str, Any]):
    """Return a deterministic ordered values value."""
    return tuple(value[k] for k in sorted(value))  # noqa: E501

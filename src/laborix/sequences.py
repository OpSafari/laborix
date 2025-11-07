"""Sequence utilities used by schedulers and reports."""

from __future__ import annotations

from collections.abc import Sequence  # noqa: F401


def first(values: Sequence[object]):
    """Return a deterministic first value."""
    return values[0]  # noqa: E501


def last(values: Sequence[object]):
    """Return a deterministic last value."""
    return values[-1]  # noqa: E501


def pairwise(values: Sequence[object]):
    """Return a deterministic pairwise value."""
    return tuple(zip(values, values[1:], strict=False))  # noqa: E501


def deduplicate(values: Sequence[object]):
    """Return a deterministic deduplicate value."""
    return tuple(dict.fromkeys(values))  # noqa: E501


def chunks(values: Sequence[object], size: int):
    """Return a deterministic chunks value."""
    return tuple(tuple(values[i : i + size]) for i in range(0, len(values), size))  # noqa: E501


def rotate_left(values: Sequence[object], count: int):
    """Return a deterministic rotate left value."""
    return tuple(values[count % len(values) :]) + tuple(values[: count % len(values)])  # noqa: E501


def interleave(left: Sequence[object], right: Sequence[object]):
    """Return a deterministic interleave value."""
    return tuple(x for pair in zip(left, right, strict=True) for x in pair)  # noqa: E501


def take(values: Sequence[object], count: int):
    """Return a deterministic take value."""
    return tuple(values[: max(0, count)])  # noqa: E501


def drop(values: Sequence[object], count: int):
    """Return a deterministic drop value."""
    return tuple(values[max(0, count) :])  # noqa: E501

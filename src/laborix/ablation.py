"""Ablation grids, coverage, comparisons, and uncertainty."""

from __future__ import annotations

from itertools import product
from typing import Any


def factor_grid(factors: dict[str, list[Any]]) -> tuple[dict[str, Any], ...]:
    names = tuple(sorted(factors))
    return tuple(
        dict(zip(names, values, strict=True)) for values in product(*(factors[n] for n in names))
    )

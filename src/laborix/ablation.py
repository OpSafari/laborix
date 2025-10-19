"""Ablation grids, coverage, comparisons, and uncertainty."""

from __future__ import annotations

from itertools import product
from typing import Any


def factor_grid(factors: dict[str, list[Any]]) -> tuple[dict[str, Any], ...]:
    names = tuple(sorted(factors))
    return tuple(
        dict(zip(names, values, strict=True)) for values in product(*(factors[n] for n in names))
    )


def missing_cells(
    factors: dict[str, list[Any]], rows: list[dict[str, Any]]
) -> tuple[dict[str, Any], ...]:
    expected = factor_grid(factors)
    keys = tuple(sorted(factors))
    seen = {tuple(row.get(k) for k in keys) for row in rows}
    return tuple(cell for cell in expected if tuple(cell[k] for k in keys) not in seen)

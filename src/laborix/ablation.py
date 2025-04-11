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


def coverage(factors: dict[str, list[Any]], rows: list[dict[str, Any]]) -> dict[str, bool]:
    result = {}
    for name in sorted(factors):
        others = tuple(k for k in sorted(factors) if k != name)
        groups = {}
        for row in rows:
            groups.setdefault(tuple(row.get(k) for k in others), set()).add(row.get(name))
        result[name] = any(
            set(values) <= seen for seen in groups.values() for values in [factors[name]]
        )
    return result


def paired_effect(
    rows: list[dict[str, Any]], factor: str, low: Any, high: Any, metric: str = "score"
) -> tuple[float, ...]:
    others = sorted(set(rows[0]) - {factor, metric}) if rows else []
    groups = {}
    for row in rows:
        groups.setdefault(tuple(row[k] for k in others), {})[row[factor]] = float(row[metric])
    return tuple(
        groups[key][high] - groups[key][low]
        for key in sorted(groups)
        if low in groups[key] and high in groups[key]
    )

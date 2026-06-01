"""Ablation grids, coverage, comparisons, and uncertainty."""

from __future__ import annotations

from dataclasses import dataclass
from itertools import product
from typing import Any

import numpy as np


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
        groups: dict[tuple[Any, ...], set[Any]] = {}
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
    groups: dict[tuple[Any, ...], dict[Any, float]] = {}
    for row in rows:
        groups.setdefault(tuple(row[k] for k in others), {})[row[factor]] = float(row[metric])
    return tuple(
        groups[key][high] - groups[key][low]
        for key in sorted(groups)
        if low in groups[key] and high in groups[key]
    )


def bootstrap_ci(
    values: tuple[float, ...], seed: int = 0, samples: int = 1000, level: float = 0.95
) -> tuple[float, float]:
    if not values:
        raise ValueError("cannot bootstrap empty values")
    rng = np.random.default_rng(seed)
    data = np.asarray(values)
    means = np.mean(rng.choice(data, (samples, len(data)), replace=True), axis=1)
    tail = (1 - level) / 2
    return float(np.quantile(means, tail)), float(np.quantile(means, 1 - tail))


@dataclass(frozen=True)
class ResultTable:
    columns: tuple[str, ...]
    rows: tuple[tuple[Any, ...], ...]


def result_table(records: list[dict[str, Any]]) -> ResultTable:
    columns = tuple(sorted({key for row in records for key in row}))
    return ResultTable(columns, tuple(tuple(row.get(key) for key in columns) for row in records))

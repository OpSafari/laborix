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


@dataclass(frozen=True)
class CoverageDiagnostic:
    factor: str
    covered: bool
    observed_levels: tuple[Any, ...]
    required_levels: tuple[Any, ...]
    witness_context: tuple[tuple[str, Any], ...] | None


@dataclass(frozen=True)
class AblationSummary:
    expected_cells: int
    observed_cells: int
    completeness: float
    missing: tuple[dict[str, Any], ...]
    coverage: tuple[CoverageDiagnostic, ...]


def coverage_diagnostics(
    factors: dict[str, list[Any]], rows: list[dict[str, Any]]
) -> tuple[CoverageDiagnostic, ...]:
    """Explain coverage using a fixed-other-factors witness when available."""
    diagnostics = []
    for name in sorted(factors):
        others = tuple(key for key in sorted(factors) if key != name)
        groups: dict[tuple[Any, ...], set[Any]] = {}
        for row in rows:
            if all(key in row for key in factors):
                groups.setdefault(tuple(row[key] for key in others), set()).add(row[name])
        required = tuple(factors[name])
        witnesses = sorted(
            (context for context, levels in groups.items() if set(required) <= levels), key=repr
        )
        observed = tuple(dict.fromkeys(row[name] for row in rows if name in row))
        witness = tuple(zip(others, witnesses[0], strict=True)) if witnesses else None
        diagnostics.append(
            CoverageDiagnostic(name, witness is not None, observed, required, witness)
        )
    return tuple(diagnostics)


def summarize_ablation(
    factors: dict[str, list[Any]], rows: list[dict[str, Any]]
) -> AblationSummary:
    """Summarize grid completeness without counting duplicate observations twice."""
    expected = factor_grid(factors)
    keys = tuple(sorted(factors))
    expected_keys = {tuple(cell[key] for key in keys) for cell in expected}
    observed_keys = {
        tuple(row[key] for key in keys)
        for row in rows
        if all(key in row for key in keys) and tuple(row[key] for key in keys) in expected_keys
    }
    count, total = len(observed_keys), len(expected_keys)
    return AblationSummary(
        total,
        count,
        count / total if total else 1.0,
        missing_cells(factors, rows),
        coverage_diagnostics(factors, rows),
    )

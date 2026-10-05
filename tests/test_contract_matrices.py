"""Broad deterministic contract matrices for public mechanics."""

import json

import pytest

from laborix.ablation import coverage, factor_grid
from laborix.records import canonical_json, derive_seed, strict_canonical_json, value_digest
from laborix.scheduler import UCB1, Budget, StationarySurface, cumulative_regret, schedule


@pytest.mark.parametrize("value", range(-128, 128))
def test_integer_canonicalization_matches_json_contract(value: int) -> None:
    encoded = canonical_json({"value": value})
    assert json.loads(encoded) == {"value": value}
    assert strict_canonical_json({"value": value}) == encoded
    assert len(value_digest({"value": value})) == 64


@pytest.mark.parametrize("root", range(128))
def test_seed_derivation_is_stable_and_namespaced_across_roots(root: int) -> None:
    left = derive_seed(root, "experiment")
    assert left == derive_seed(root, "experiment")
    assert left != derive_seed(root, "analysis")
    assert 0 <= left < 2**32


@pytest.mark.parametrize("seed", range(100))
def test_ucb_seeded_stationary_runs_respect_budget_and_regret(seed: int) -> None:
    surface = StationarySurface((0.1, 0.4, 0.9), noise=0.01)
    trace = schedule(surface, UCB1(3), Budget(64), seed)
    assert len(trace) == 64
    assert {item.arm for item in trace} == {0, 1, 2}
    assert cumulative_regret(trace)[-1] < 20


@pytest.mark.parametrize("missing", range(64))
def test_three_factor_grid_reports_each_single_missing_cell(missing: int) -> None:
    factors = {"a": [0, 1, 2, 3], "b": [False, True], "c": ["x", "y", "z", "w", "v", "u", "t", "s"]}
    grid = factor_grid(factors)
    rows = [dict(cell, score=float(index)) for index, cell in enumerate(grid) if index != missing]
    assert len(grid) == 64
    assert coverage(factors, rows) == {"a": True, "b": True, "c": True}

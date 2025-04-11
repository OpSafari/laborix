import pytest

from laborix.ablation import factor_grid


def test_factor_grid_is_complete_and_stable() -> None:
    assert factor_grid({"b": [0, 1], "a": ["x", "y"]}) == (
        {"a": "x", "b": 0},
        {"a": "x", "b": 1},
        {"a": "y", "b": 0},
        {"a": "y", "b": 1},
    )


def test_missing_cells_reports_exact_configurations() -> None:
    from laborix.ablation import missing_cells

    assert missing_cells({"x": [0, 1]}, [{"x": 0, "score": 2}]) == ({"x": 1},)


def test_coverage_requires_controlled_variation() -> None:
    from laborix.ablation import coverage

    factors = {"a": [0, 1], "b": [0, 1]}
    assert coverage(factors, list(factor_grid(factors))) == {"a": True, "b": True}
    assert coverage(factors, [{"a": 0, "b": 0}, {"a": 1, "b": 1}]) == {"a": False, "b": False}


def test_paired_effect_uses_matched_contexts() -> None:
    from laborix.ablation import paired_effect

    rows = [
        {"method": "a", "seed": 1, "score": 2},
        {"method": "b", "seed": 1, "score": 5},
        {"method": "a", "seed": 2, "score": 4},
        {"method": "b", "seed": 2, "score": 3},
    ]
    assert paired_effect(rows, "method", "a", "b") == pytest.approx((3, -1))


def test_bootstrap_ci_is_seeded_and_contains_constant() -> None:
    from laborix.ablation import bootstrap_ci

    assert bootstrap_ci((2.0, 2.0), 4, 100) == (2.0, 2.0)
    with pytest.raises(ValueError, match="empty"):
        bootstrap_ci(())

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


def test_result_table_aligns_sparse_rows() -> None:
    from laborix.ablation import result_table

    table = result_table([{"b": 2}, {"a": 1, "b": 3}])
    assert table.columns == ("a", "b")
    assert table.rows == ((None, 2), (1, 3))


def test_ablation_summary_counts_unique_valid_cells() -> None:
    from laborix.ablation import summarize_ablation

    factors = {"a": [0, 1], "b": ["x", "y"]}
    rows = [{"a": 0, "b": "x"}, {"a": 0, "b": "x"}, {"a": 1, "b": "x"}]
    summary = summarize_ablation(factors, rows)
    assert (summary.expected_cells, summary.observed_cells, summary.completeness) == (4, 2, 0.5)
    assert summary.missing == ({"a": 0, "b": "y"}, {"a": 1, "b": "y"})


def test_coverage_diagnostics_include_fixed_context_witnesses() -> None:
    from laborix.ablation import coverage_diagnostics

    factors = {"a": [0, 1], "b": ["x", "y"]}
    diagnostics = coverage_diagnostics(factors, list(factor_grid(factors)))
    assert [item.factor for item in diagnostics] == ["a", "b"]
    assert all(item.covered for item in diagnostics)
    assert diagnostics[0].witness_context == (("b", "x"),)

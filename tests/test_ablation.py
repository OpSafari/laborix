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

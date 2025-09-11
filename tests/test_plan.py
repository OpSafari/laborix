from laborix.plan import Stage


def test_stage_values_are_stable() -> None:
    assert [x.value for x in Stage] == [
        "literature",
        "ideation",
        "data-prep",
        "experiment",
        "analysis",
        "report",
    ]

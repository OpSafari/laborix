def test_step_ids_query() -> None:
    from laborix.plan import Plan, Stage, Step
    from laborix.plan_queries import step_ids

    assert step_ids(Plan("x", (Step("a", Stage.REPORT, "x"),))) == ("a",)

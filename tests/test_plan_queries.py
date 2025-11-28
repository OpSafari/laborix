def test_step_ids_query() -> None:
    from laborix.plan import Plan, Stage, Step
    from laborix.plan_queries import step_ids

    assert step_ids(Plan("x", (Step("a", Stage.REPORT, "x"),))) == ("a",)


def test_operations_query() -> None:
    from laborix.plan import Plan, Stage, Step
    from laborix.plan_queries import operations

    plan = Plan("x", (Step("a", Stage.REPORT, "z"), Step("b", Stage.REPORT, "a")))
    assert operations(plan) == ("a", "z")


def test_dependency_count_query() -> None:
    from laborix.plan import Plan, Stage, Step
    from laborix.plan_queries import dependency_count

    actual = dependency_count(
        Plan("x", (Step("a", Stage.REPORT, "x"), Step("b", Stage.REPORT, "x", ("a",))))
    )
    assert actual == 1


def test_leaf_steps_query() -> None:
    from laborix.plan import Plan, Stage, Step
    from laborix.plan_queries import leaf_steps

    actual = leaf_steps(
        Plan("x", (Step("a", Stage.REPORT, "x"), Step("b", Stage.REPORT, "x", ("a",))))
    )
    assert actual == ("b",)


def test_root_steps_query() -> None:
    from laborix.plan import Plan, Stage, Step
    from laborix.plan_queries import root_steps

    actual = root_steps(
        Plan("x", (Step("a", Stage.REPORT, "x"), Step("b", Stage.REPORT, "x", ("a",))))
    )
    assert actual == ("a",)

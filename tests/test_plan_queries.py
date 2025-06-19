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


def test_stages_used_query() -> None:
    from laborix.plan import Plan, Stage, Step
    from laborix.plan_queries import stages_used

    actual = stages_used(Plan("x", (Step("a", Stage.REPORT, "x"), Step("b", Stage.ANALYSIS, "x"))))
    assert actual == ("analysis", "report")


def test_stages_used_query_is_stable() -> None:
    from laborix.plan import Plan, Stage, Step
    from laborix.plan_queries import stages_used

    plan = Plan("x", (Step("a", Stage.REPORT, "x"), Step("b", Stage.ANALYSIS, "x")))
    assert stages_used(plan) == stages_used(plan)


def test_output_count_query() -> None:
    from laborix.plan import Plan, Stage, Step
    from laborix.plan_queries import output_count

    actual = output_count(Plan("x", (Step("a", Stage.REPORT, "x"),)))
    assert actual == 0


def test_max_retry_attempts_query() -> None:
    from laborix.plan import Plan, Stage, Step
    from laborix.plan_queries import max_retry_attempts

    actual = max_retry_attempts(Plan("x", (Step("a", Stage.REPORT, "x"),)))
    assert actual == 1


def test_max_retry_attempts_query_is_stable() -> None:
    from laborix.plan import Plan, Stage, Step
    from laborix.plan_queries import max_retry_attempts

    first = max_retry_attempts(Plan("x", (Step("a", Stage.REPORT, "x"),)))
    second = max_retry_attempts(Plan("x", (Step("a", Stage.REPORT, "x"),)))
    assert first == second


def test_total_cpu_query() -> None:
    from laborix.plan import Plan, Stage, Step
    from laborix.plan_queries import total_cpu

    actual = total_cpu(Plan("x", (Step("a", Stage.REPORT, "x"), Step("b", Stage.REPORT, "x"))))
    assert actual == 2


def test_total_memory_mb_query() -> None:
    from laborix.plan import Plan, Stage, Step
    from laborix.plan_queries import total_memory_mb

    actual = total_memory_mb(Plan("x", (Step("a", Stage.REPORT, "x"),)))
    assert actual == 256


def test_total_memory_mb_query_is_stable() -> None:
    from laborix.plan import Plan, Stage, Step
    from laborix.plan_queries import total_memory_mb

    first = total_memory_mb(Plan("x", (Step("a", Stage.REPORT, "x"),)))
    second = total_memory_mb(Plan("x", (Step("a", Stage.REPORT, "x"),)))
    assert first == second


def test_stage_steps_query() -> None:
    from laborix.plan import Plan, Stage, Step
    from laborix.plan_queries import stage_steps

    actual = stage_steps(Plan("x", (Step("a", Stage.REPORT, "x"),)), Stage.REPORT)
    assert actual == ("a",)


def test_operation_steps_query() -> None:
    from laborix.plan import Plan, Stage, Step
    from laborix.plan_queries import operation_steps

    actual = operation_steps(Plan("x", (Step("a", Stage.REPORT, "mean"),)), "mean")
    assert actual == ("a",)

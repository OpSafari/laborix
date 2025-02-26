import pytest

from laborix.errors import ValidationError
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


def test_port_defaults_to_json() -> None:
    from laborix.plan import Port

    assert Port("metrics").kind == "json"


def test_resources_require_positive_limits() -> None:
    from laborix.plan import Resources

    Resources().validate()
    with pytest.raises(ValidationError, match="positive"):
        Resources(cpu=0).validate()


def test_retry_policy_checks_ceiling_and_jitter() -> None:
    from laborix.plan import RetryPolicy

    with pytest.raises(ValidationError, match="attempts"):
        RetryPolicy(0).validate()
    with pytest.raises(ValidationError, match="timing"):
        RetryPolicy(jitter=1.1).validate()


def test_step_defaults_are_isolated() -> None:
    from laborix.plan import Step

    left = Step("a", Stage.EXPERIMENT, "noop")
    right = Step("b", Stage.REPORT, "noop")
    left.config["x"] = 1
    assert right.config == {}


def test_plan_records_schema_and_seed() -> None:
    from laborix.plan import Plan

    assert Plan("demo", (), seed=7).schema_version == "2.0"


def test_identifiers_and_duplicates_are_rejected() -> None:
    from laborix.plan import Plan, Step, _ids

    with pytest.raises(ValidationError, match="invalid step id"):
        _ids(Plan("x", (Step("Bad", Stage.REPORT, "x"),)))
    a = Step("a", Stage.REPORT, "x")
    with pytest.raises(ValidationError, match="duplicate"):
        _ids(Plan("x", (a, a)))


def test_topological_order_is_stable_and_rejects_dangling() -> None:
    from laborix.plan import Plan, Step, topological_order

    steps = (Step("b", Stage.REPORT, "x", ("a",)), Step("a", Stage.EXPERIMENT, "x"))
    assert topological_order(Plan("x", steps)) == ("a", "b")
    with pytest.raises(ValidationError, match="dangling dependency: z"):
        topological_order(Plan("x", (Step("a", Stage.REPORT, "x", ("z",)),)))


def test_topological_order_reports_cycles() -> None:
    from laborix.plan import Plan, Step, topological_order

    steps = (Step("a", Stage.EXPERIMENT, "x", ("b",)), Step("b", Stage.ANALYSIS, "x", ("a",)))
    with pytest.raises(ValidationError, match="cycle among: a, b"):
        topological_order(Plan("x", steps))


def test_input_references_require_existing_ports() -> None:
    from laborix.plan import Plan, Port, Step, validate_plan

    a = Step("a", Stage.EXPERIMENT, "x", outputs=(Port("score"),))
    b = Step("b", Stage.ANALYSIS, "x", ("a",), {"x": "a.missing"})
    with pytest.raises(ValidationError, match=r"missing port a\.missing"):
        validate_plan(Plan("x", (a, b)))


def test_plan_json_is_canonical() -> None:
    from laborix.plan import Plan, plan_to_json

    assert (
        plan_to_json(Plan("合成", (), seed=3))
        == '{"name":"合成","schema_version":"2.0","seed":3,"steps":[]}'
    )


def test_plan_roundtrip_preserves_typed_values() -> None:
    from laborix.plan import Plan, Port, Step, plan_from_json, plan_to_json

    value = Plan("x", (Step("a", Stage.EXPERIMENT, "mean", outputs=(Port("score", "number"),)),))
    assert plan_from_json(plan_to_json(value)) == value


def test_migration_upgrades_v1_without_mutation() -> None:
    from laborix.plan import migrate_plan

    old = {"schema_version": "1.0", "name": "x", "steps": []}
    new = migrate_plan(old)
    assert new == {"schema_version": "2.0", "name": "x", "steps": [], "seed": 0}
    assert old["schema_version"] == "1.0"


def test_plan_diff_classifies_step_changes() -> None:
    from laborix.plan import Plan, Step, diff_plans

    before = Plan("x", (Step("a", Stage.EXPERIMENT, "old"), Step("gone", Stage.REPORT, "x")))
    after = Plan("x", (Step("a", Stage.EXPERIMENT, "new"), Step("new", Stage.REPORT, "x")))
    assert diff_plans(before, after).added == ("new",)
    assert diff_plans(before, after).removed == ("gone",)
    assert diff_plans(before, after).changed == ("a",)

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

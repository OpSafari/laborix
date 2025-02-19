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

from laborix.errors import ValidationError


def test_validation_error_is_value_error() -> None:
    assert isinstance(ValidationError("bad plan"), ValueError)


def test_execution_error_includes_context() -> None:
    from laborix.errors import ExecutionError

    error = ExecutionError("fit", 2, "timed out")
    assert str(error) == "step 'fit' attempt 2: timed out"

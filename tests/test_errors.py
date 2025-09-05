from laborix.errors import ValidationError


def test_validation_error_is_value_error() -> None:
    assert isinstance(ValidationError("bad plan"), ValueError)

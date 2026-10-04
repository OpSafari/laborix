from laborix.records import canonical_json


def test_canonical_json_sorts_keys_and_preserves_unicode() -> None:
    assert canonical_json({"β": 2, "a": 1}) == '{"a":1,"β":2}'


def test_strict_canonical_json_rejects_nan() -> None:
    import pytest

    from laborix.records import strict_canonical_json

    with pytest.raises(ValueError, match="JSON compliant"):
        strict_canonical_json({"loss": float("nan")})

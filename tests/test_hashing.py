from laborix.hashing import value_digest


def test_value_digest_ignores_mapping_order() -> None:
    assert value_digest({"a": 1, "b": 2}) == value_digest({"b": 2, "a": 1})

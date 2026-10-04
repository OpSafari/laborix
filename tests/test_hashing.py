from laborix.records import value_digest


def test_value_digest_ignores_mapping_order() -> None:
    assert value_digest({"a": 1, "b": 2}) == value_digest({"b": 2, "a": 1})


def test_bytes_digest_respects_order() -> None:
    from laborix.records import bytes_digest

    assert bytes_digest([b"ab", b"c"]) == bytes_digest([b"a", b"bc"])
    assert bytes_digest([b"a", b"b"]) != bytes_digest([b"b", b"a"])

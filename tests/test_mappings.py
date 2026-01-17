def test_sorted_keys_contract() -> None:
    from laborix.mappings import sorted_keys

    actual = sorted_keys({"b": 2, "a": 1})
    assert actual == ("a", "b")
    assert actual == sorted_keys({"b": 2, "a": 1})


def test_sorted_keys_result_has_stable_representation() -> None:
    from laborix.mappings import sorted_keys

    result_one = sorted_keys({"b": 2, "a": 1})
    result_two = sorted_keys({"b": 2, "a": 1})
    assert type(result_one) is type(result_two)
    assert repr(result_one) == repr(result_two)

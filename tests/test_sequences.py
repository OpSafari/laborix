def test_first_contract() -> None:
    from laborix.sequences import first

    actual = first(["a", "b"])
    assert actual == "a"
    assert actual == first(["a", "b"])


def test_first_result_has_stable_representation() -> None:
    from laborix.sequences import first

    result_one = first(["a", "b"])
    result_two = first(["a", "b"])
    assert type(result_one) is type(result_two)
    assert repr(result_one) == repr(result_two)

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


def test_last_contract() -> None:
    from laborix.sequences import last

    actual = last(["a", "b"])
    assert actual == "b"
    assert actual == last(["a", "b"])


def test_last_result_has_stable_representation() -> None:
    from laborix.sequences import last

    result_one = last(["a", "b"])
    result_two = last(["a", "b"])
    assert type(result_one) is type(result_two)
    assert repr(result_one) == repr(result_two)

def test_clamp01_contract() -> None:
    from laborix.transforms import clamp01

    actual = clamp01(-2.0)
    assert actual == 0.0
    assert actual == clamp01(-2.0)


def test_clamp01_result_has_stable_representation() -> None:
    from laborix.transforms import clamp01

    first = clamp01(-2.0)
    second = clamp01(-2.0)
    assert type(first) is type(second)
    assert repr(first) == repr(second)


def test_percent_contract() -> None:
    from laborix.transforms import percent

    actual = percent(0.125)
    assert actual == 12.5
    assert actual == percent(0.125)


def test_percent_result_has_stable_representation() -> None:
    from laborix.transforms import percent

    result_one = percent(0.125)
    result_two = percent(0.125)
    assert type(result_one) is type(result_two)
    assert repr(result_one) == repr(result_two)

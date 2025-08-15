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

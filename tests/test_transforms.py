def test_clamp01_contract() -> None:
    from laborix.transforms import clamp01

    actual = clamp01(-2.0)
    assert actual == 0.0
    assert actual == clamp01(-2.0)

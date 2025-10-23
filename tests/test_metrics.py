def test_arithmetic_mean_example() -> None:
    from laborix.metrics import arithmetic_mean

    assert arithmetic_mean([1.0, 2.0, 6.0]) == 3.0

def test_arithmetic_mean_example() -> None:
    from laborix.metrics import arithmetic_mean

    assert arithmetic_mean([1.0, 2.0, 6.0]) == 3.0


def test_mean_absolute_error_example() -> None:
    from laborix.metrics import mean_absolute_error

    assert mean_absolute_error([1.0, 3.0], [2.0, 5.0]) == 1.5

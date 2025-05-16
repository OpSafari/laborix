def test_arithmetic_mean_example() -> None:
    from laborix.metrics import arithmetic_mean

    assert arithmetic_mean([1.0, 2.0, 6.0]) == 3.0


def test_mean_absolute_error_example() -> None:
    from laborix.metrics import mean_absolute_error

    assert mean_absolute_error([1.0, 3.0], [2.0, 5.0]) == 1.5


def test_root_mean_square_example() -> None:
    import math

    import pytest

    from laborix.metrics import root_mean_square

    assert root_mean_square([3.0, 4.0]) == pytest.approx(math.sqrt(12.5))


def test_minimum_example() -> None:
    from laborix.metrics import minimum

    assert minimum([3.0, -1.0, 2.0]) == -1.0


def test_maximum_example() -> None:
    from laborix.metrics import maximum

    assert maximum([3.0, -1.0, 2.0]) == 3.0


def test_maximum_is_repeatable() -> None:
    from laborix.metrics import maximum

    assert maximum([3.0, -1.0, 2.0]) == maximum([3.0, -1.0, 2.0])


def test_value_range_example() -> None:
    from laborix.metrics import value_range

    assert value_range([3.0, -1.0, 2.0]) == 4.0


def test_median_example() -> None:
    from laborix.metrics import median

    assert median([9.0, 1.0, 4.0]) == 4.0

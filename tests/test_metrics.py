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


def test_median_is_repeatable() -> None:
    from laborix.metrics import median

    assert median([9.0, 1.0, 4.0]) == median([9.0, 1.0, 4.0])


def test_geometric_mean_example() -> None:
    from laborix.metrics import geometric_mean

    assert geometric_mean([1.0, 4.0]) == 2.0


def test_harmonic_mean_example() -> None:
    import pytest

    from laborix.metrics import harmonic_mean

    assert harmonic_mean([1.0, 2.0]) == pytest.approx(4 / 3)


def test_harmonic_mean_is_repeatable() -> None:
    from laborix.metrics import harmonic_mean

    assert harmonic_mean([1.0, 2.0]) == harmonic_mean([1.0, 2.0])


def test_sum_squares_example() -> None:
    from laborix.metrics import sum_squares

    assert sum_squares([2.0, 3.0]) == 13.0


def test_l1_norm_example() -> None:
    from laborix.metrics import l1_norm

    assert l1_norm([-2.0, 3.0]) == 5.0


def test_l1_norm_is_repeatable() -> None:
    from laborix.metrics import l1_norm

    assert l1_norm([-2.0, 3.0]) == l1_norm([-2.0, 3.0])


def test_l2_norm_example() -> None:
    from laborix.metrics import l2_norm

    assert l2_norm([3.0, 4.0]) == 5.0


def test_positive_rate_example() -> None:
    from laborix.metrics import positive_rate

    assert positive_rate([-1.0, 0.0, 2.0, 3.0]) == 0.5


def test_positive_rate_is_repeatable() -> None:
    from laborix.metrics import positive_rate

    assert positive_rate([-1.0, 0.0, 2.0, 3.0]) == positive_rate([-1.0, 0.0, 2.0, 3.0])


def test_zero_rate_example() -> None:
    from laborix.metrics import zero_rate

    assert zero_rate([0.0, 1.0, 0.0, 2.0]) == 0.5


def test_clipped_mean_example() -> None:
    from laborix.metrics import clipped_mean

    assert clipped_mean([-2.0, 2.0, 9.0], 0.0, 4.0) == 2.0


def test_clipped_mean_is_repeatable() -> None:
    from laborix.metrics import clipped_mean

    assert clipped_mean([-2.0, 2.0, 9.0], 0.0, 4.0) == clipped_mean([-2.0, 2.0, 9.0], 0.0, 4.0)


def test_weighted_sum_example() -> None:
    from laborix.metrics import weighted_sum

    assert weighted_sum([2.0, 3.0], [0.25, 0.75]) == 2.75


def test_max_index_example() -> None:
    from laborix.metrics import max_index

    assert max_index([1.0, 9.0, 2.0]) == 1


def test_max_index_is_repeatable() -> None:
    from laborix.metrics import max_index

    assert max_index([1.0, 9.0, 2.0]) == max_index([1.0, 9.0, 2.0])

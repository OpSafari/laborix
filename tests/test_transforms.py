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


def test_square_contract() -> None:
    from laborix.transforms import square

    actual = square(-3.0)
    assert actual == 9.0
    assert actual == square(-3.0)


def test_square_result_has_stable_representation() -> None:
    from laborix.transforms import square

    result_one = square(-3.0)
    result_two = square(-3.0)
    assert type(result_one) is type(result_two)
    assert repr(result_one) == repr(result_two)


def test_signed_sqrt_contract() -> None:
    from laborix.transforms import signed_sqrt

    actual = signed_sqrt(-9.0)
    assert actual == -3.0
    assert actual == signed_sqrt(-9.0)


def test_signed_sqrt_result_has_stable_representation() -> None:
    from laborix.transforms import signed_sqrt

    result_one = signed_sqrt(-9.0)
    result_two = signed_sqrt(-9.0)
    assert type(result_one) is type(result_two)
    assert repr(result_one) == repr(result_two)


def test_safe_ratio_contract() -> None:
    from laborix.transforms import safe_ratio

    actual = safe_ratio(3.0, 2.0)
    assert actual == 1.5
    assert actual == safe_ratio(3.0, 2.0)


def test_safe_ratio_result_has_stable_representation() -> None:
    from laborix.transforms import safe_ratio

    result_one = safe_ratio(3.0, 2.0)
    result_two = safe_ratio(3.0, 2.0)
    assert type(result_one) is type(result_two)
    assert repr(result_one) == repr(result_two)


def test_log1p_positive_contract() -> None:
    import math

    from laborix.transforms import log1p_positive

    actual = log1p_positive(math.e - 1)
    assert actual == 1.0
    assert actual == log1p_positive(math.e - 1)


def test_log1p_positive_result_has_stable_representation() -> None:
    import math

    from laborix.transforms import log1p_positive

    result_one = log1p_positive(math.e - 1)
    result_two = log1p_positive(math.e - 1)
    assert type(result_one) is type(result_two)
    assert repr(result_one) == repr(result_two)


def test_center_contract() -> None:
    from laborix.transforms import center

    actual = center(8.0, 3.0)
    assert actual == 5.0
    assert actual == center(8.0, 3.0)


def test_center_result_has_stable_representation() -> None:
    from laborix.transforms import center

    result_one = center(8.0, 3.0)
    result_two = center(8.0, 3.0)
    assert type(result_one) is type(result_two)
    assert repr(result_one) == repr(result_two)


def test_unit_interval_contract() -> None:
    from laborix.transforms import unit_interval

    actual = unit_interval(5.0, 0.0, 10.0)
    assert actual == 0.5
    assert actual == unit_interval(5.0, 0.0, 10.0)


def test_unit_interval_result_has_stable_representation() -> None:
    from laborix.transforms import unit_interval

    result_one = unit_interval(5.0, 0.0, 10.0)
    result_two = unit_interval(5.0, 0.0, 10.0)
    assert type(result_one) is type(result_two)
    assert repr(result_one) == repr(result_two)


def test_quantize_contract() -> None:
    from laborix.transforms import quantize

    actual = quantize(1.24, 0.5)
    assert actual == 1.0
    assert actual == quantize(1.24, 0.5)


def test_quantize_result_has_stable_representation() -> None:
    from laborix.transforms import quantize

    result_one = quantize(1.24, 0.5)
    result_two = quantize(1.24, 0.5)
    assert type(result_one) is type(result_two)
    assert repr(result_one) == repr(result_two)


def test_bounded_exp_contract() -> None:
    from laborix.transforms import bounded_exp

    actual = bounded_exp(10.0, 0.0)
    assert actual == 1.0
    assert actual == bounded_exp(10.0, 0.0)


def test_bounded_exp_result_has_stable_representation() -> None:
    from laborix.transforms import bounded_exp

    result_one = bounded_exp(10.0, 0.0)
    result_two = bounded_exp(10.0, 0.0)
    assert type(result_one) is type(result_two)
    assert repr(result_one) == repr(result_two)


def test_absolute_delta_contract() -> None:
    from laborix.transforms import absolute_delta

    actual = absolute_delta(2.0, 5.5)
    assert actual == 3.5
    assert actual == absolute_delta(2.0, 5.5)


def test_absolute_delta_result_has_stable_representation() -> None:
    from laborix.transforms import absolute_delta

    result_one = absolute_delta(2.0, 5.5)
    result_two = absolute_delta(2.0, 5.5)
    assert type(result_one) is type(result_two)
    assert repr(result_one) == repr(result_two)


def test_relative_error_contract() -> None:
    from laborix.transforms import relative_error

    actual = relative_error(4.0, 5.0)
    assert actual == 0.25
    assert actual == relative_error(4.0, 5.0)


def test_relative_error_result_has_stable_representation() -> None:
    from laborix.transforms import relative_error

    result_one = relative_error(4.0, 5.0)
    result_two = relative_error(4.0, 5.0)
    assert type(result_one) is type(result_two)
    assert repr(result_one) == repr(result_two)


def test_softsign_contract() -> None:
    from laborix.transforms import softsign

    actual = softsign(3.0)
    assert actual == 0.75
    assert actual == softsign(3.0)


def test_softsign_result_has_stable_representation() -> None:
    from laborix.transforms import softsign

    result_one = softsign(3.0)
    result_two = softsign(3.0)
    assert type(result_one) is type(result_two)
    assert repr(result_one) == repr(result_two)


def test_lerp_contract() -> None:
    from laborix.transforms import lerp

    actual = lerp(2.0, 6.0, 0.25)
    assert actual == 3.0
    assert actual == lerp(2.0, 6.0, 0.25)


def test_lerp_result_has_stable_representation() -> None:
    from laborix.transforms import lerp

    result_one = lerp(2.0, 6.0, 0.25)
    result_two = lerp(2.0, 6.0, 0.25)
    assert type(result_one) is type(result_two)
    assert repr(result_one) == repr(result_two)


def test_sign_contract() -> None:
    from laborix.transforms import sign

    actual = sign(-2.0)
    assert actual == -1
    assert actual == sign(-2.0)


def test_sign_result_has_stable_representation() -> None:
    from laborix.transforms import sign

    result_one = sign(-2.0)
    result_two = sign(-2.0)
    assert type(result_one) is type(result_two)
    assert repr(result_one) == repr(result_two)


def test_midpoint_contract() -> None:
    from laborix.transforms import midpoint

    actual = midpoint(2.0, 8.0)
    assert actual == 5.0
    assert actual == midpoint(2.0, 8.0)


def test_midpoint_result_has_stable_representation() -> None:
    from laborix.transforms import midpoint

    result_one = midpoint(2.0, 8.0)
    result_two = midpoint(2.0, 8.0)
    assert type(result_one) is type(result_two)
    assert repr(result_one) == repr(result_two)


def test_reciprocal_contract() -> None:
    from laborix.transforms import reciprocal

    actual = reciprocal(4.0)
    assert actual == 0.25
    assert actual == reciprocal(4.0)


def test_reciprocal_result_has_stable_representation() -> None:
    from laborix.transforms import reciprocal

    result_one = reciprocal(4.0)
    result_two = reciprocal(4.0)
    assert type(result_one) is type(result_two)
    assert repr(result_one) == repr(result_two)


def test_negative_contract() -> None:
    from laborix.transforms import negative

    actual = negative(3.0)
    assert actual == -3.0
    assert actual == negative(3.0)


def test_negative_result_has_stable_representation() -> None:
    from laborix.transforms import negative

    result_one = negative(3.0)
    result_two = negative(3.0)
    assert type(result_one) is type(result_two)
    assert repr(result_one) == repr(result_two)

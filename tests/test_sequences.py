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


def test_pairwise_contract() -> None:
    from laborix.sequences import pairwise

    actual = pairwise([1, 2, 3])
    assert actual == ((1, 2), (2, 3))
    assert actual == pairwise([1, 2, 3])


def test_deduplicate_contract() -> None:
    from laborix.sequences import deduplicate

    actual = deduplicate([1, 2, 1, 3])
    assert actual == (1, 2, 3)
    assert actual == deduplicate([1, 2, 1, 3])


def test_deduplicate_result_has_stable_representation() -> None:
    from laborix.sequences import deduplicate

    result_one = deduplicate([1, 2, 1, 3])
    result_two = deduplicate([1, 2, 1, 3])
    assert type(result_one) is type(result_two)
    assert repr(result_one) == repr(result_two)


def test_chunks_contract() -> None:
    from laborix.sequences import chunks

    actual = chunks([1, 2, 3, 4, 5], 2)
    assert actual == ((1, 2), (3, 4), (5,))
    assert actual == chunks([1, 2, 3, 4, 5], 2)


def test_chunks_result_has_stable_representation() -> None:
    from laborix.sequences import chunks

    result_one = chunks([1, 2, 3, 4, 5], 2)
    result_two = chunks([1, 2, 3, 4, 5], 2)
    assert type(result_one) is type(result_two)
    assert repr(result_one) == repr(result_two)


def test_rotate_left_contract() -> None:
    from laborix.sequences import rotate_left

    actual = rotate_left([1, 2, 3], 1)
    assert actual == (2, 3, 1)
    assert actual == rotate_left([1, 2, 3], 1)


def test_rotate_left_result_has_stable_representation() -> None:
    from laborix.sequences import rotate_left

    result_one = rotate_left([1, 2, 3], 1)
    result_two = rotate_left([1, 2, 3], 1)
    assert type(result_one) is type(result_two)
    assert repr(result_one) == repr(result_two)


def test_interleave_contract() -> None:
    from laborix.sequences import interleave

    actual = interleave([1, 2], ["a", "b"])
    assert actual == (1, "a", 2, "b")
    assert actual == interleave([1, 2], ["a", "b"])


def test_interleave_result_has_stable_representation() -> None:
    from laborix.sequences import interleave

    result_one = interleave([1, 2], ["a", "b"])
    result_two = interleave([1, 2], ["a", "b"])
    assert type(result_one) is type(result_two)
    assert repr(result_one) == repr(result_two)


def test_take_contract() -> None:
    from laborix.sequences import take

    actual = take([1, 2, 3], 2)
    assert actual == (1, 2)
    assert actual == take([1, 2, 3], 2)


def test_take_result_has_stable_representation() -> None:
    from laborix.sequences import take

    result_one = take([1, 2, 3], 2)
    result_two = take([1, 2, 3], 2)
    assert type(result_one) is type(result_two)
    assert repr(result_one) == repr(result_two)


def test_drop_contract() -> None:
    from laborix.sequences import drop

    actual = drop([1, 2, 3], 1)
    assert actual == (2, 3)
    assert actual == drop([1, 2, 3], 1)


def test_drop_result_has_stable_representation() -> None:
    from laborix.sequences import drop

    result_one = drop([1, 2, 3], 1)
    result_two = drop([1, 2, 3], 1)
    assert type(result_one) is type(result_two)
    assert repr(result_one) == repr(result_two)


def test_flatten_once_contract() -> None:
    from laborix.sequences import flatten_once

    actual = flatten_once([[1, 2], [3]])
    assert actual == (1, 2, 3)
    assert actual == flatten_once([[1, 2], [3]])


def test_flatten_once_result_has_stable_representation() -> None:
    from laborix.sequences import flatten_once

    result_one = flatten_once([[1, 2], [3]])
    result_two = flatten_once([[1, 2], [3]])
    assert type(result_one) is type(result_two)
    assert repr(result_one) == repr(result_two)


def test_index_map_contract() -> None:
    from laborix.sequences import index_map

    actual = index_map(["a", "b"])
    assert actual == {"a": 0, "b": 1}
    assert actual == index_map(["a", "b"])


def test_index_map_result_has_stable_representation() -> None:
    from laborix.sequences import index_map

    result_one = index_map(["a", "b"])
    result_two = index_map(["a", "b"])
    assert type(result_one) is type(result_two)
    assert repr(result_one) == repr(result_two)


def test_only_contract() -> None:
    from laborix.sequences import only

    actual = only(["x"])
    assert actual == "x"
    assert actual == only(["x"])


def test_only_result_has_stable_representation() -> None:
    from laborix.sequences import only

    result_one = only(["x"])
    result_two = only(["x"])
    assert type(result_one) is type(result_two)
    assert repr(result_one) == repr(result_two)


def test_windows_contract() -> None:
    from laborix.sequences import windows

    actual = windows([1, 2, 3], 2)
    assert actual == ((1, 2), (2, 3))
    assert actual == windows([1, 2, 3], 2)


def test_windows_result_has_stable_representation() -> None:
    from laborix.sequences import windows

    result_one = windows([1, 2, 3], 2)
    result_two = windows([1, 2, 3], 2)
    assert type(result_one) is type(result_two)
    assert repr(result_one) == repr(result_two)


def test_reversed_tuple_contract() -> None:
    from laborix.sequences import reversed_tuple

    actual = reversed_tuple([1, 2, 3])
    assert actual == (3, 2, 1)
    assert actual == reversed_tuple([1, 2, 3])


def test_reversed_tuple_result_has_stable_representation() -> None:
    from laborix.sequences import reversed_tuple

    result_one = reversed_tuple([1, 2, 3])
    result_two = reversed_tuple([1, 2, 3])
    assert type(result_one) is type(result_two)
    assert repr(result_one) == repr(result_two)


def test_enumerated_contract() -> None:
    from laborix.sequences import enumerated

    actual = enumerated(["a", "b"])
    assert actual == ((0, "a"), (1, "b"))
    assert actual == enumerated(["a", "b"])


def test_enumerated_result_has_stable_representation() -> None:
    from laborix.sequences import enumerated

    result_one = enumerated(["a", "b"])
    result_two = enumerated(["a", "b"])
    assert type(result_one) is type(result_two)
    assert repr(result_one) == repr(result_two)


def test_repeat_contract() -> None:
    from laborix.sequences import repeat

    actual = repeat([1, 2], 2)
    assert actual == (1, 2, 1, 2)
    assert actual == repeat([1, 2], 2)


def test_repeat_result_has_stable_representation() -> None:
    from laborix.sequences import repeat

    result_one = repeat([1, 2], 2)
    result_two = repeat([1, 2], 2)
    assert type(result_one) is type(result_two)
    assert repr(result_one) == repr(result_two)


def test_every_other_contract() -> None:
    from laborix.sequences import every_other

    actual = every_other([1, 2, 3, 4])
    assert actual == (1, 3)
    assert actual == every_other([1, 2, 3, 4])


def test_every_other_result_has_stable_representation() -> None:
    from laborix.sequences import every_other

    result_one = every_other([1, 2, 3, 4])
    result_two = every_other([1, 2, 3, 4])
    assert type(result_one) is type(result_two)
    assert repr(result_one) == repr(result_two)


def test_tail_contract() -> None:
    from laborix.sequences import tail

    actual = tail([1, 2, 3])
    assert actual == (2, 3)
    assert actual == tail([1, 2, 3])


def test_tail_result_has_stable_representation() -> None:
    from laborix.sequences import tail

    result_one = tail([1, 2, 3])
    result_two = tail([1, 2, 3])
    assert type(result_one) is type(result_two)
    assert repr(result_one) == repr(result_two)


def test_head_contract() -> None:
    from laborix.sequences import head

    actual = head([1, 2, 3])
    assert actual == (1, 2)
    assert actual == head([1, 2, 3])

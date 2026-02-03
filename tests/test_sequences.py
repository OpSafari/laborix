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

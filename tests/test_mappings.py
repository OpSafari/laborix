def test_sorted_keys_contract() -> None:
    from laborix.mappings import sorted_keys

    actual = sorted_keys({"b": 2, "a": 1})
    assert actual == ("a", "b")
    assert actual == sorted_keys({"b": 2, "a": 1})


def test_sorted_keys_result_has_stable_representation() -> None:
    from laborix.mappings import sorted_keys

    result_one = sorted_keys({"b": 2, "a": 1})
    result_two = sorted_keys({"b": 2, "a": 1})
    assert type(result_one) is type(result_two)
    assert repr(result_one) == repr(result_two)


def test_sorted_items_contract() -> None:
    from laborix.mappings import sorted_items

    actual = sorted_items({"b": 2, "a": 1})
    assert actual == (("a", 1), ("b", 2))
    assert actual == sorted_items({"b": 2, "a": 1})


def test_sorted_items_result_has_stable_representation() -> None:
    from laborix.mappings import sorted_items

    result_one = sorted_items({"b": 2, "a": 1})
    result_two = sorted_items({"b": 2, "a": 1})
    assert type(result_one) is type(result_two)
    assert repr(result_one) == repr(result_two)


def test_without_none_contract() -> None:
    from laborix.mappings import without_none

    actual = without_none({"a": 1, "b": None})
    assert actual == {"a": 1}
    assert actual == without_none({"a": 1, "b": None})


def test_without_none_result_has_stable_representation() -> None:
    from laborix.mappings import without_none

    result_one = without_none({"a": 1, "b": None})
    result_two = without_none({"a": 1, "b": None})
    assert type(result_one) is type(result_two)
    assert repr(result_one) == repr(result_two)


def test_select_keys_contract() -> None:
    from laborix.mappings import select_keys

    actual = select_keys({"a": 1, "b": 2}, ["b"])
    assert actual == {"b": 2}
    assert actual == select_keys({"a": 1, "b": 2}, ["b"])


def test_select_keys_result_has_stable_representation() -> None:
    from laborix.mappings import select_keys

    result_one = select_keys({"a": 1, "b": 2}, ["b"])
    result_two = select_keys({"a": 1, "b": 2}, ["b"])
    assert type(result_one) is type(result_two)
    assert repr(result_one) == repr(result_two)


def test_rename_key_contract() -> None:
    from laborix.mappings import rename_key

    actual = rename_key({"old": 1}, "old", "new")
    assert actual == {"new": 1}
    assert actual == rename_key({"old": 1}, "old", "new")

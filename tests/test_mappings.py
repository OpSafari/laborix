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


def test_rename_key_result_has_stable_representation() -> None:
    from laborix.mappings import rename_key

    result_one = rename_key({"old": 1}, "old", "new")
    result_two = rename_key({"old": 1}, "old", "new")
    assert type(result_one) is type(result_two)
    assert repr(result_one) == repr(result_two)


def test_invert_unique_contract() -> None:
    from laborix.mappings import invert_unique

    actual = invert_unique({"a": 1, "b": 2})
    assert actual == {1: "a", 2: "b"}
    assert actual == invert_unique({"a": 1, "b": 2})


def test_invert_unique_result_has_stable_representation() -> None:
    from laborix.mappings import invert_unique

    result_one = invert_unique({"a": 1, "b": 2})
    result_two = invert_unique({"a": 1, "b": 2})
    assert type(result_one) is type(result_two)
    assert repr(result_one) == repr(result_two)


def test_prefix_keys_contract() -> None:
    from laborix.mappings import prefix_keys

    actual = prefix_keys({"a": 1}, "run.")
    assert actual == {"run.a": 1}
    assert actual == prefix_keys({"a": 1}, "run.")


def test_prefix_keys_result_has_stable_representation() -> None:
    from laborix.mappings import prefix_keys

    result_one = prefix_keys({"a": 1}, "run.")
    result_two = prefix_keys({"a": 1}, "run.")
    assert type(result_one) is type(result_two)
    assert repr(result_one) == repr(result_two)


def test_merge_right_contract() -> None:
    from laborix.mappings import merge_right

    actual = merge_right({"a": 1}, {"a": 2, "b": 3})
    assert actual == {"a": 2, "b": 3}
    assert actual == merge_right({"a": 1}, {"a": 2, "b": 3})


def test_merge_right_result_has_stable_representation() -> None:
    from laborix.mappings import merge_right

    result_one = merge_right({"a": 1}, {"a": 2, "b": 3})
    result_two = merge_right({"a": 1}, {"a": 2, "b": 3})
    assert type(result_one) is type(result_two)
    assert repr(result_one) == repr(result_two)


def test_common_keys_contract() -> None:
    from laborix.mappings import common_keys

    actual = common_keys({"a": 1, "b": 2}, {"b": 3})
    assert actual == ("b",)
    assert actual == common_keys({"a": 1, "b": 2}, {"b": 3})


def test_common_keys_result_has_stable_representation() -> None:
    from laborix.mappings import common_keys

    result_one = common_keys({"a": 1, "b": 2}, {"b": 3})
    result_two = common_keys({"a": 1, "b": 2}, {"b": 3})
    assert type(result_one) is type(result_two)
    assert repr(result_one) == repr(result_two)


def test_changed_keys_contract() -> None:
    from laborix.mappings import changed_keys

    actual = changed_keys({"a": 1, "b": 2}, {"a": 1, "b": 3})
    assert actual == ("b",)
    assert actual == changed_keys({"a": 1, "b": 2}, {"a": 1, "b": 3})


def test_changed_keys_result_has_stable_representation() -> None:
    from laborix.mappings import changed_keys

    result_one = changed_keys({"a": 1, "b": 2}, {"a": 1, "b": 3})
    result_two = changed_keys({"a": 1, "b": 2}, {"a": 1, "b": 3})
    assert type(result_one) is type(result_two)
    assert repr(result_one) == repr(result_two)


def test_added_keys_contract() -> None:
    from laborix.mappings import added_keys

    actual = added_keys({"a": 1}, {"a": 1, "b": 2})
    assert actual == ("b",)
    assert actual == added_keys({"a": 1}, {"a": 1, "b": 2})


def test_added_keys_result_has_stable_representation() -> None:
    from laborix.mappings import added_keys

    result_one = added_keys({"a": 1}, {"a": 1, "b": 2})
    result_two = added_keys({"a": 1}, {"a": 1, "b": 2})
    assert type(result_one) is type(result_two)
    assert repr(result_one) == repr(result_two)


def test_removed_keys_contract() -> None:
    from laborix.mappings import removed_keys

    actual = removed_keys({"a": 1, "b": 2}, {"a": 1})
    assert actual == ("b",)
    assert actual == removed_keys({"a": 1, "b": 2}, {"a": 1})


def test_removed_keys_result_has_stable_representation() -> None:
    from laborix.mappings import removed_keys

    result_one = removed_keys({"a": 1, "b": 2}, {"a": 1})
    result_two = removed_keys({"a": 1, "b": 2}, {"a": 1})
    assert type(result_one) is type(result_two)
    assert repr(result_one) == repr(result_two)


def test_numeric_total_contract() -> None:
    from laborix.mappings import numeric_total

    actual = numeric_total({"a": 1, "b": 2.5, "c": "x"})
    assert actual == 3.5
    assert actual == numeric_total({"a": 1, "b": 2.5, "c": "x"})


def test_numeric_total_result_has_stable_representation() -> None:
    from laborix.mappings import numeric_total

    result_one = numeric_total({"a": 1, "b": 2.5, "c": "x"})
    result_two = numeric_total({"a": 1, "b": 2.5, "c": "x"})
    assert type(result_one) is type(result_two)
    assert repr(result_one) == repr(result_two)


def test_string_values_contract() -> None:
    from laborix.mappings import string_values

    actual = string_values({"a": 1, "b": True})
    assert actual == {"a": "1", "b": "True"}
    assert actual == string_values({"a": 1, "b": True})


def test_string_values_result_has_stable_representation() -> None:
    from laborix.mappings import string_values

    result_one = string_values({"a": 1, "b": True})
    result_two = string_values({"a": 1, "b": True})
    assert type(result_one) is type(result_two)
    assert repr(result_one) == repr(result_two)


def test_nonempty_strings_contract() -> None:
    from laborix.mappings import nonempty_strings

    actual = nonempty_strings({"a": " x ", "b": "", "c": 2})
    assert actual == {"a": " x "}
    assert actual == nonempty_strings({"a": " x ", "b": "", "c": 2})


def test_nonempty_strings_result_has_stable_representation() -> None:
    from laborix.mappings import nonempty_strings

    result_one = nonempty_strings({"a": " x ", "b": "", "c": 2})
    result_two = nonempty_strings({"a": " x ", "b": "", "c": 2})
    assert type(result_one) is type(result_two)
    assert repr(result_one) == repr(result_two)


def test_bool_flags_contract() -> None:
    from laborix.mappings import bool_flags

    actual = bool_flags({"a": True, "b": 1})
    assert actual == {"a": True}
    assert actual == bool_flags({"a": True, "b": 1})


def test_bool_flags_result_has_stable_representation() -> None:
    from laborix.mappings import bool_flags

    result_one = bool_flags({"a": True, "b": 1})
    result_two = bool_flags({"a": True, "b": 1})
    assert type(result_one) is type(result_two)
    assert repr(result_one) == repr(result_two)


def test_nest_dotted_contract() -> None:
    from laborix.mappings import nest_dotted

    actual = nest_dotted({"run.seed": 7})
    assert actual == {"seed": 7}
    assert actual == nest_dotted({"run.seed": 7})


def test_nest_dotted_result_has_stable_representation() -> None:
    from laborix.mappings import nest_dotted

    result_one = nest_dotted({"run.seed": 7})
    result_two = nest_dotted({"run.seed": 7})
    assert type(result_one) is type(result_two)
    assert repr(result_one) == repr(result_two)


def test_value_types_contract() -> None:
    from laborix.mappings import value_types

    actual = value_types({"a": 1, "b": "x"})
    assert actual == {"a": "int", "b": "str"}
    assert actual == value_types({"a": 1, "b": "x"})


def test_value_types_result_has_stable_representation() -> None:
    from laborix.mappings import value_types

    result_one = value_types({"a": 1, "b": "x"})
    result_two = value_types({"a": 1, "b": "x"})
    assert type(result_one) is type(result_two)
    assert repr(result_one) == repr(result_two)

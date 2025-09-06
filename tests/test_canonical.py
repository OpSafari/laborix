from laborix.canonical import canonical_json


def test_canonical_json_sorts_keys_and_preserves_unicode() -> None:
    assert canonical_json({"β": 2, "a": 1}) == '{"a":1,"β":2}'

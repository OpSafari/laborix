def test_first_contract() -> None:
    from laborix.sequences import first

    actual = first(["a", "b"])
    assert actual == "a"
    assert actual == first(["a", "b"])

from laborix.records import derive_seed


def test_derive_seed_is_stable_and_namespaced() -> None:
    assert derive_seed(7, "fit") == derive_seed(7, "fit")
    assert derive_seed(7, "fit") != derive_seed(7, "score")


def test_validate_seed_boundaries() -> None:
    import pytest

    from laborix.records import validate_seed

    assert validate_seed(0) == 0
    assert validate_seed(2**32 - 1) == 2**32 - 1
    for invalid in (-1, 2**32, True):
        with pytest.raises(ValueError, match="seed"):
            validate_seed(invalid)

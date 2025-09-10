from laborix.seeds import derive_seed


def test_derive_seed_is_stable_and_namespaced() -> None:
    assert derive_seed(7, "fit") == derive_seed(7, "fit")
    assert derive_seed(7, "fit") != derive_seed(7, "score")

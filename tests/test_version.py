from importlib.metadata import version

import laborix


def test_version_matches_installed_metadata() -> None:
    assert laborix.__version__ == version("laborix") == "0.1.0"


def test_public_core_exports() -> None:
    import laborix

    assert {
        "ExecutionError",
        "ValidationError",
        "__version__",
        "derive_seed",
        "value_digest",
    } <= set(laborix.__all__)

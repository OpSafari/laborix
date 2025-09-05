from importlib.metadata import version

import laborix


def test_version_matches_installed_metadata() -> None:
    assert laborix.__version__ == version("laborix") == "0.1.0"

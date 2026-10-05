import re
import tomllib
from importlib.metadata import version
from pathlib import Path

import laborix


def test_version_matches_installed_metadata() -> None:
    assert laborix.__version__ == version("laborix")


def test_version_matches_pyproject_and_changelog() -> None:
    root = Path(__file__).resolve().parents[1]
    pyproject = tomllib.loads((root / "pyproject.toml").read_text())
    assert pyproject["project"]["version"] == laborix.__version__
    heading = re.search(
        r"^##\s+\[?v?(\d+\.\d+\.\d+)\]?", (root / "CHANGELOG.md").read_text(), re.MULTILINE
    )
    assert heading is not None and heading.group(1) == laborix.__version__


def test_public_core_exports() -> None:
    import laborix

    assert {
        "ExecutionError",
        "ValidationError",
        "__version__",
        "derive_seed",
        "value_digest",
    } <= set(laborix.__all__)

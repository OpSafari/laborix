"""Smoke-test an installed wheel without importing the source tree."""

from __future__ import annotations

import laborix


def main() -> int:
    assert laborix.__version__
    print(f"laborix {laborix.__version__}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

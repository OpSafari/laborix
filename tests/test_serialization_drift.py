import pytest

from laborix.records import strict_canonical_json


def test_canonical_json_rejects_all_nonfinite_values() -> None:
    for value in (float("nan"), float("inf"), float("-inf")):
        with pytest.raises(ValueError):
            strict_canonical_json({"value": value})

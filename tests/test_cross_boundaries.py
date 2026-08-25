import pytest

from laborix.seeds import validate_seed


def test_seed_contract_both_boundaries() -> None:
    assert validate_seed(0) == 0
    assert validate_seed(2**32 - 1) == 2**32 - 1
    for value in (-1, 2**32, True):
        with pytest.raises(ValueError):
            validate_seed(value)

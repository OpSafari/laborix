import pytest

from laborix.executor import bounded_batches


def test_bounded_batches() -> None:
    assert bounded_batches(["c", "a", "b"], 2) == (("a", "b"), ("c",))
    with pytest.raises(ValueError):
        bounded_batches([], 0)

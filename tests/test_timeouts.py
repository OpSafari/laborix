from laborix.timeouts import Deadline


def test_deadline() -> None:
    value = Deadline(10, 2)
    assert value.remaining(11) == 1
    assert value.expired(12)

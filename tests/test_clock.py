from laborix.clock import SystemClock


def test_system_clock_is_monotonic() -> None:
    clock = SystemClock()
    assert clock.now() <= clock.now()


def test_manual_clock_advances_and_rejects_negative_time() -> None:
    import pytest

    from laborix.clock import ManualClock

    clock = ManualClock(2.0)
    clock.advance(1.5)
    assert clock.now() == 3.5
    with pytest.raises(ValueError, match="backwards"):
        clock.advance(-0.1)


def test_elapsed_seconds_never_negative() -> None:
    from laborix.clock import ManualClock, elapsed_seconds

    assert elapsed_seconds(ManualClock(1.0), 2.0) == 0.0

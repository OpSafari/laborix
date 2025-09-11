from laborix.clock import SystemClock


def test_system_clock_is_monotonic() -> None:
    clock = SystemClock()
    assert clock.now() <= clock.now()

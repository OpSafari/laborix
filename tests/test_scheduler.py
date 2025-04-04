from laborix.scheduler import StationarySurface


def test_stationary_oracle_finds_best_arm() -> None:
    s = StationarySurface((0.1, 0.8, 0.3))
    assert s.oracle() == (1, 0.8)
    assert s.reward(1, 0, 4) == 0.8


def test_budget_enforces_both_limits() -> None:
    from laborix.scheduler import Budget

    b = Budget(3, 2.0)
    assert b.allows(2, 1.9)
    assert not b.allows(3, 0)
    assert not b.allows(0, 2.0)

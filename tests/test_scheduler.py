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


def test_ucb1_cold_starts_in_arm_order() -> None:
    from laborix.scheduler import UCB1

    p = UCB1(3)
    seen = []
    for reward in (0.1, 0.9, 0.2):
        a = p.select()
        seen.append(a)
        p.update(a, reward)
    assert seen == [0, 1, 2]

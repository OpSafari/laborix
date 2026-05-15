from laborix.scheduler import UCB1, Budget, StationarySurface, cumulative_regret, schedule


def test_stationary_regret_is_sublinear() -> None:
    trace = schedule(StationarySurface((0.1, 0.9, 0.3)), UCB1(3), Budget(400), 3)
    assert cumulative_regret(trace)[-1] < len(trace) ** 0.75

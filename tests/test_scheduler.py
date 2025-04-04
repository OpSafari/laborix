from laborix.scheduler import StationarySurface


def test_stationary_oracle_finds_best_arm() -> None:
    s = StationarySurface((0.1, 0.8, 0.3))
    assert s.oracle() == (1, 0.8)
    assert s.reward(1, 0, 4) == 0.8

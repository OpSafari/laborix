from laborix.scheduler import Budget


def test_budget_never_crosses_either_limit() -> None:
    budget = Budget(3, 2.0)
    assert budget.allows(2, 1.9)
    assert not budget.allows(3, 0)
    assert not budget.allows(0, 2.0)
    assert not budget.allows(4, 3.0)

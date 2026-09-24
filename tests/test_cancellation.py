from laborix.executor import CancellationToken


def test_cancellation() -> None:
    token = CancellationToken()
    assert not token.cancelled
    token.cancel()
    assert token.cancelled

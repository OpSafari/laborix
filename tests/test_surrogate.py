import pytest

torch = pytest.importorskip("torch")
from laborix.surrogate import train_surrogate  # noqa: E402


@pytest.mark.model
@pytest.mark.slow
def test_surrogate_loss_decreases_on_synthetic_data() -> None:
    x = torch.linspace(-1, 1, 24).reshape(-1, 1)
    y = 2 * x[:, 0] + 0.5
    _, losses = train_surrogate(x, y, 7, 60)
    assert losses[-1] < losses[0] * 0.1

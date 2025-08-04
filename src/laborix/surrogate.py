"""Optional compact Torch surrogate for synthetic reward prediction."""

from __future__ import annotations

from typing import Any


def train_surrogate(
    features: Any, targets: Any, seed: int = 0, epochs: int = 80
) -> tuple[Any, tuple[float, ...]]:
    import torch

    torch.manual_seed(seed)
    x = torch.as_tensor(features, dtype=torch.float32)
    y = torch.as_tensor(targets, dtype=torch.float32).reshape(-1, 1)
    model = torch.nn.Sequential(
        torch.nn.Linear(x.shape[1], 8), torch.nn.Tanh(), torch.nn.Linear(8, 1)
    )
    optimizer = torch.optim.Adam(model.parameters(), lr=0.05)
    losses = []
    for _ in range(epochs):
        optimizer.zero_grad()
        loss = torch.nn.functional.mse_loss(model(x), y)
        loss.backward()
        optimizer.step()
        losses.append(float(loss.detach()))
    return model, tuple(losses)

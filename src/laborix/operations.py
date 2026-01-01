"""Built-in NumPy operations for fully offline synthetic programs."""

from __future__ import annotations

from typing import Any

import numpy as np

from laborix.registry import StepRegistry


def generate(inputs: dict[str, Any], config: dict[str, Any], seed: int) -> dict[str, Any]:
    rng = np.random.default_rng(seed)
    count = int(config.get("count", 32))
    x = rng.normal(size=count)
    return {"values": x.tolist()}


def summarize(inputs: dict[str, Any], config: dict[str, Any], seed: int) -> dict[str, Any]:
    values = np.asarray(inputs["values"], dtype=float)
    return {"mean": float(values.mean()), "std": float(values.std())}


def compare(inputs: dict[str, Any], config: dict[str, Any], seed: int) -> dict[str, Any]:
    return {"difference": float(inputs["candidate"] - inputs["baseline"])}


def builtins() -> StepRegistry:
    registry = StepRegistry()
    registry.register("synthetic.generate", generate)
    registry.register("synthetic.summarize", summarize)
    registry.register("synthetic.compare", compare)
    return registry

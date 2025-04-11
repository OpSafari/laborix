"""Dependency-free deterministic SVG charts."""

from __future__ import annotations

from collections.abc import Sequence


def regret_svg(values: Sequence[float], width: int = 480, height: int = 240) -> str:
    if width < 20 or height < 20:
        raise ValueError("chart dimensions must be at least 20")
    if not values:
        return f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}"/>'
    top = max(values) or 1.0
    points = " ".join(
        f"{10 + i * (width - 20) / max(1, len(values) - 1):.2f},"
        f"{height - 10 - v * (height - 20) / top:.2f}"
        for i, v in enumerate(values)
    )
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'role="img"><title>Cumulative regret on synthetic data</title>'
        f'<polyline fill="none" stroke="#245" points="{points}"/></svg>'
    )

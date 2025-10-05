"""Named in-process NumPy operation registry."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

Operation = Callable[[dict[str, Any], dict[str, Any], int], dict[str, Any]]


class StepRegistry:
    def __init__(self) -> None:
        self._items: dict[str, Operation] = {}

    def register(self, name: str, operation: Operation) -> None:
        if not name or name in self._items:
            raise ValueError(f"operation already registered or empty: {name}")
        self._items[name] = operation

    def resolve(self, name: str) -> Operation:
        try:
            return self._items[name]
        except KeyError as error:
            raise KeyError(f"unknown operation: {name}") from error

    @property
    def names(self) -> tuple[str, ...]:
        return tuple(sorted(self._items))

"""Model-agnostic text adapters; deterministic implementations are offline."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


class ModelAdapter(Protocol):
    def propose_ideas(self, prompt: str) -> str: ...
    def summarize_paper(self, text: str) -> str: ...
    def interpret_results(self, text: str) -> str: ...


@dataclass
class ScriptedAdapter:
    responses: dict[str, list[str]]

    def _take(self, kind: str) -> str:
        if not self.responses.get(kind):
            raise LookupError(f"no scripted response for {kind}")
        return self.responses[kind].pop(0)

    def propose_ideas(self, prompt: str) -> str:
        return self._take("propose_ideas")

    def summarize_paper(self, text: str) -> str:
        return self._take("summarize_paper")

    def interpret_results(self, text: str) -> str:
        return self._take("interpret_results")

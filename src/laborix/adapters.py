"""Model-agnostic text adapters; deterministic implementations are offline."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
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


@dataclass
class ReplayAdapter:
    records: list[dict[str, str]]

    @classmethod
    def from_jsonl(cls, path: Path) -> ReplayAdapter:
        return cls([json.loads(x) for x in path.read_text().splitlines() if x])

    def _find(self, kind: str, prompt: str) -> str:
        for item in self.records:
            if item.get("kind") == kind and item.get("prompt") == prompt:
                return item["response"]
        raise LookupError(f"no replay for {kind}")

    def propose_ideas(self, prompt: str) -> str:
        return self._find("propose_ideas", prompt)

    def summarize_paper(self, text: str) -> str:
        return self._find("summarize_paper", text)

    def interpret_results(self, text: str) -> str:
        return self._find("interpret_results", text)

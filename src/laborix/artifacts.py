"""Content-addressed artifacts stored beneath a run directory."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ArtifactRef:
    digest: str
    size: int
    media_type: str = "application/json"

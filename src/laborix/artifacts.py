"""Content-addressed artifacts stored beneath a run directory."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from laborix.hashing import bytes_digest


@dataclass(frozen=True)
class ArtifactRef:
    digest: str
    size: int
    media_type: str = "application/json"


class ArtifactStore:
    def __init__(self, root: Path):
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)

    def put_bytes(self, data: bytes, media_type: str = "application/octet-stream") -> ArtifactRef:
        digest = bytes_digest([data])
        path = self.root / digest[:2] / digest[2:]
        path.parent.mkdir(parents=True, exist_ok=True)
        if not path.exists():
            path.write_bytes(data)
        return ArtifactRef(digest, len(data), media_type)

"""Content-addressed artifacts stored beneath a run directory."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from laborix.records import bytes_digest, strict_canonical_json


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

    def get_bytes(self, ref: ArtifactRef) -> bytes:
        data = (self.root / ref.digest[:2] / ref.digest[2:]).read_bytes()
        if len(data) != ref.size or bytes_digest([data]) != ref.digest:
            raise ValueError(f"artifact integrity failure: {ref.digest}")
        return data

    def put_json(self, value: Any) -> ArtifactRef:
        return self.put_bytes(strict_canonical_json(value).encode(), "application/json")

    def get_json(self, ref: ArtifactRef) -> Any:
        return json.loads(self.get_bytes(ref))

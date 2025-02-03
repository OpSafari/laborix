"""Canonical serialization used by hashes and persisted artifacts."""

import json
from typing import Any


def canonical_json(value: Any) -> str:
    """Encode JSON with sorted keys and no insignificant whitespace."""
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)

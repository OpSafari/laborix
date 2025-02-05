"""Stable content hashes."""

import hashlib
from typing import Any

from laborix.canonical import strict_canonical_json


def value_digest(value: Any) -> str:
    """Return a SHA-256 digest of a JSON-compatible value."""
    payload = strict_canonical_json(value).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()

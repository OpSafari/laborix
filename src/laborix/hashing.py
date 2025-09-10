"""Stable content hashes."""

import hashlib
from typing import Any

from laborix.canonical import strict_canonical_json


def value_digest(value: Any) -> str:
    """Return a SHA-256 digest of a JSON-compatible value."""
    payload = strict_canonical_json(value).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def bytes_digest(chunks: list[bytes]) -> str:
    """Digest ordered byte chunks without concatenating them in memory."""
    digest = hashlib.sha256()
    for chunk in chunks:
        digest.update(chunk)
    return digest.hexdigest()

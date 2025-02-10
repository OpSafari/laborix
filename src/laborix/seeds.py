"""Seed derivation independent of process hash randomization."""

import hashlib


def derive_seed(root: int, namespace: str) -> int:
    """Derive a stable unsigned 32-bit seed."""
    payload = f"{root}:{namespace}".encode()
    return int.from_bytes(hashlib.sha256(payload).digest()[:4], "big")

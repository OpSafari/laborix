"""Seed derivation independent of process hash randomization."""

import hashlib


def derive_seed(root: int, namespace: str) -> int:
    """Derive a stable unsigned 32-bit seed."""
    payload = f"{root}:{namespace}".encode()
    return int.from_bytes(hashlib.sha256(payload).digest()[:4], "big")


def validate_seed(seed: int) -> int:
    """Validate a NumPy-compatible unsigned 32-bit seed."""
    if isinstance(seed, bool) or not isinstance(seed, int) or not 0 <= seed < 2**32:
        raise ValueError("seed must be an integer in [0, 2**32)")
    return seed

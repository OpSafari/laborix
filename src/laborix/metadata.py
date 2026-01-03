"""Reproducibility metadata for persisted runs."""

from __future__ import annotations

import platform
from dataclasses import asdict, dataclass

import numpy as np

from laborix import __version__
from laborix.hashing import value_digest


@dataclass(frozen=True)
class RunMetadata:
    schema_version: str
    laborix_version: str
    python_version: str
    numpy_version: str
    seed: int
    config_hash: str


def metadata(config: object, seed: int) -> RunMetadata:
    return RunMetadata(
        "1.0", __version__, platform.python_version(), np.__version__, seed, value_digest(config)
    )


def metadata_dict(value: RunMetadata) -> dict[str, object]:
    return asdict(value)

from pathlib import Path

import pytest

from laborix.artifacts import ArtifactRef


def test_artifact_reference_records_identity() -> None:
    assert ArtifactRef("a" * 64, 3).size == 3


def test_store_deduplicates_equal_bytes(tmp_path: Path) -> None:
    from laborix.artifacts import ArtifactStore

    store = ArtifactStore(tmp_path)
    a = store.put_bytes(b"data")
    b = store.put_bytes(b"data")
    assert a == b
    assert len(list(tmp_path.glob("*/*"))) == 1


def test_store_detects_tampered_content(tmp_path: Path) -> None:
    from laborix.artifacts import ArtifactStore

    store = ArtifactStore(tmp_path)
    ref = store.put_bytes(b"good")
    (tmp_path / ref.digest[:2] / ref.digest[2:]).write_bytes(b"evil")
    with pytest.raises(ValueError, match="integrity"):
        store.get_bytes(ref)

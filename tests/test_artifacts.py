from pathlib import Path

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

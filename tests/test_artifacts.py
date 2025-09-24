from laborix.artifacts import ArtifactRef


def test_artifact_reference_records_identity() -> None:
    assert ArtifactRef("a" * 64, 3).size == 3

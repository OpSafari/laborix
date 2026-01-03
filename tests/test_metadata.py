from laborix.metadata import metadata, metadata_dict


def test_metadata_embeds_versions_seed_and_config_hash() -> None:
    value = metadata({"x": 1}, 7)
    raw = metadata_dict(value)
    assert raw["schema_version"] == "1.0"
    assert raw["seed"] == 7
    assert len(raw["config_hash"]) == 64

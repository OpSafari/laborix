def test_public_api_manifest() -> None:
    import laborix

    assert len(laborix.__all__) == 12
    assert len(set(laborix.__all__)) == 12

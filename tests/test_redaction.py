from laborix.records import is_secret_key


def test_secret_key_detection_is_case_and_separator_insensitive() -> None:
    assert is_secret_key("API-Key")
    assert is_secret_key("refreshToken")
    assert is_secret_key("token_count") is not False  # conservative by design


def test_redact_handles_nested_mappings_without_mutation() -> None:
    from laborix.records import redact

    source = {"nested": {"password": "p", "label": "safe"}}
    assert redact(source) == {"nested": {"password": "[REDACTED]", "label": "safe"}}
    assert source["nested"]["password"] == "p"


def test_redact_sequence_descends_into_items() -> None:
    from laborix.records import redact_sequence

    assert redact_sequence([{"secret": "x"}, {"ok": 1}]) == [{"secret": "[REDACTED]"}, {"ok": 1}]


def test_assert_no_secrets_reports_nested_path() -> None:
    import pytest

    from laborix.records import assert_no_secrets

    with pytest.raises(ValueError, match=r"\$\.request\.api_key"):
        assert_no_secrets({"request": {"api_key": "x"}})

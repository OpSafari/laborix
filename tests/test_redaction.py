from laborix.redaction import is_secret_key


def test_secret_key_detection_is_case_and_separator_insensitive() -> None:
    assert is_secret_key("API-Key")
    assert is_secret_key("refreshToken")
    assert is_secret_key("token_count") is not False  # conservative by design


def test_redact_handles_nested_mappings_without_mutation() -> None:
    from laborix.redaction import redact

    source = {"nested": {"password": "p", "label": "safe"}}
    assert redact(source) == {"nested": {"password": "[REDACTED]", "label": "safe"}}
    assert source["nested"]["password"] == "p"

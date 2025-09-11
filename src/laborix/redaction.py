"""Conservative removal of credentials from persisted metadata."""

SECRET_FRAGMENTS = ("api_key", "apikey", "authorization", "password", "secret", "token")


def is_secret_key(key: str) -> bool:
    """Return whether a metadata key appears credential-bearing."""
    normalized = key.lower().replace("-", "_")
    return any(fragment in normalized for fragment in SECRET_FRAGMENTS)


def redact(value: object) -> object:
    """Return a JSON-like value with mapping credentials replaced."""
    if isinstance(value, dict):
        return {
            str(key): "[REDACTED]" if is_secret_key(str(key)) else redact(item)
            for key, item in value.items()
        }
    return value


def redact_sequence(values: list[object] | tuple[object, ...]) -> list[object]:
    """Redact every value in a JSON-like sequence."""
    return [redact(item) for item in values]


def assert_no_secrets(value: object, path: str = "$") -> None:
    """Reject a nested payload whose keys could expose credentials."""
    if isinstance(value, dict):
        for key, item in value.items():
            if is_secret_key(str(key)):
                raise ValueError(f"secret-like key at {path}.{key}")
            assert_no_secrets(item, f"{path}.{key}")
    elif isinstance(value, (list, tuple)):
        for index, item in enumerate(value):
            assert_no_secrets(item, f"{path}[{index}]")

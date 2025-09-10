"""Conservative removal of credentials from persisted metadata."""

SECRET_FRAGMENTS = ("api_key", "apikey", "authorization", "password", "secret", "token")


def is_secret_key(key: str) -> bool:
    """Return whether a metadata key appears credential-bearing."""
    normalized = key.lower().replace("-", "_")
    return any(fragment in normalized for fragment in SECRET_FRAGMENTS)

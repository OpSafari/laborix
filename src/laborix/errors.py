"""Domain-specific failures with stable user-facing messages."""


class ValidationError(ValueError):
    """Raised when a research-program value violates an invariant."""

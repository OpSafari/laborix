"""Domain-specific failures with stable user-facing messages."""


class ValidationError(ValueError):
    """Raised when a research-program value violates an invariant."""


class ExecutionError(RuntimeError):
    """Failure tied to one step and attempt."""

    def __init__(self, step_id: str, attempt: int, message: str) -> None:
        self.step_id = step_id
        self.attempt = attempt
        super().__init__(f"step {step_id!r} attempt {attempt}: {message}")

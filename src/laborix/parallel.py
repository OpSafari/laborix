from collections.abc import Sequence


def bounded_batches(values: Sequence[str], limit: int) -> tuple[tuple[str, ...], ...]:
    if limit < 1:
        raise ValueError("parallelism must be positive")
    ordered = sorted(values)
    return tuple(tuple(ordered[i : i + limit]) for i in range(0, len(ordered), limit))

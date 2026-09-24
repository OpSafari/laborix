import pytest

from laborix.executor import StepRegistry


def noop(inputs, config, seed):
    return {"seed": seed}


def test_registry_resolves_named_operation() -> None:
    registry = StepRegistry()
    registry.register("seed", noop)
    assert registry.resolve("seed")({}, {}, 4) == {"seed": 4}
    assert registry.names == ("seed",)


def test_registry_rejects_duplicates_and_unknown_names() -> None:
    registry = StepRegistry()
    registry.register("x", noop)
    with pytest.raises(ValueError, match="registered"):
        registry.register("x", noop)
    with pytest.raises(KeyError, match="unknown operation"):
        registry.resolve("missing")

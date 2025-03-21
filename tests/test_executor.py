from pathlib import Path

from laborix.executor import Executor
from laborix.registry import StepRegistry


def registry() -> StepRegistry:
    result = StepRegistry()
    result.register("constant", lambda inputs, config, seed: {"value": config["value"]})
    result.register(
        "plus", lambda inputs, config, seed: {"value": inputs["x"] + config.get("amount", 1)}
    )
    return result


def test_executor_initializes_run_storage(tmp_path: Path) -> None:
    runner = Executor(registry(), tmp_path)
    assert runner.store.root.exists()

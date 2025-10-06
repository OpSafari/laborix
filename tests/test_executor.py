from pathlib import Path

from laborix.executor import Executor
from laborix.plan import Plan, Port, Stage, Step
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


def test_executor_runs_dependencies_and_artifacts(tmp_path: Path) -> None:
    plan = Plan(
        "x",
        (
            Step("a", Stage.EXPERIMENT, "constant", outputs=(Port("value"),), config={"value": 2}),
            Step("b", Stage.ANALYSIS, "plus", ("a",), {"x": "a.value"}, (Port("value"),)),
        ),
    )
    result = Executor(registry(), tmp_path).run(plan)
    assert result.outputs["b"] == {"value": 3}
    assert result.completed == ("a", "b")


def test_executor_returns_clean_partial_state(tmp_path: Path) -> None:
    reg = registry()
    reg.register("fail", lambda a, b, c: (_ for _ in ()).throw(RuntimeError("boom")))
    plan = Plan(
        "x",
        (
            Step("a", Stage.EXPERIMENT, "constant", config={"value": 2}),
            Step("b", Stage.ANALYSIS, "fail", ("a",)),
        ),
    )
    result = Executor(reg, tmp_path).run(plan)
    assert result.completed == ("a",)
    assert result.failed == "b"

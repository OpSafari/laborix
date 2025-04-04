from pathlib import Path

from laborix.executor import Executor
from laborix.plan import Plan, Port, RetryPolicy, Stage, Step
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


def test_executor_honors_retry_ceiling(tmp_path: Path) -> None:
    calls = []
    reg = registry()
    reg.register("flaky", lambda a, b, c: calls.append(1) or (_ for _ in ()).throw(RuntimeError()))
    result = Executor(reg, tmp_path).run(
        Plan("x", (Step("a", Stage.EXPERIMENT, "flaky", retry=RetryPolicy(3)),))
    )
    assert result.failed == "a"
    assert len(calls) == 3


def test_resume_replays_completed_artifacts(tmp_path: Path) -> None:
    calls = []
    reg = StepRegistry()
    reg.register("once", lambda a, b, c: calls.append(1) or {"value": 9})
    plan = Plan("x", (Step("a", Stage.EXPERIMENT, "once"),))
    first = Executor(reg, tmp_path).run(plan)
    second = Executor(reg, tmp_path).run(plan, resume=True)
    assert first.outputs == second.outputs
    assert len(calls) == 1

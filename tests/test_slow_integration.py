"""Longer offline integration checks over complete synthetic mechanics."""

import subprocess
import sys
import time
from pathlib import Path

import pytest

from laborix.ablation import coverage, factor_grid, missing_cells
from laborix.executor import Executor, StepRegistry
from laborix.plan import Plan, Stage, Step
from laborix.scheduler import UCB1, Budget, StationarySurface, cumulative_regret, schedule

pytestmark = pytest.mark.slow


def _constant_registry() -> StepRegistry:
    registry = StepRegistry()
    registry.register("constant", lambda inputs, config, seed: {"value": config["value"]})
    return registry


def _artifact_bytes(root: Path) -> dict[str, bytes]:
    return {
        str(path.relative_to(root)): path.read_bytes()
        for path in sorted(root.rglob("*"))
        if path.is_file() and not path.name.endswith(".size")
    }


def test_real_subprocess_kill_resumes_to_straight_run_artifacts(tmp_path: Path) -> None:
    interrupted = tmp_path / "interrupted"
    ready = tmp_path / "ready"
    code = "\n".join(
        (
            "import sys,time",
            "from pathlib import Path",
            "from laborix.executor import Executor,StepRegistry",
            "from laborix.plan import Plan,Stage,Step",
            "run,ready=map(Path,sys.argv[1:])",
            "r=StepRegistry()",
            "def slow(i,c,s): ready.write_text('ready'); time.sleep(30); return {'value':7}",
            "r.register('slow',slow)",
            "Executor(r,run).run(Plan('kill',(Step('a',Stage.EXPERIMENT,'slow'),)))",
        )
    )
    process = subprocess.Popen([sys.executable, "-c", code, str(interrupted), str(ready)])
    for _ in range(200):
        if ready.exists():
            break
        time.sleep(0.01)
    assert ready.exists()
    process.kill()
    process.wait(timeout=5)

    plan = Plan("kill", (Step("a", Stage.EXPERIMENT, "constant", config={"value": 7}),))
    resumed = Executor(_constant_registry(), interrupted).run(plan, resume=True)
    straight_dir = tmp_path / "straight"
    straight = Executor(_constant_registry(), straight_dir).run(plan)
    assert resumed.outputs == straight.outputs == {"a": {"value": 7}}
    assert _artifact_bytes(interrupted / "artifacts") == _artifact_bytes(straight_dir / "artifacts")


def test_executor_is_byte_deterministic_across_run_directories(tmp_path: Path) -> None:
    plan = Plan("same", (Step("a", Stage.EXPERIMENT, "constant", config={"value": [1, 2]}),))
    left, right = tmp_path / "left", tmp_path / "right"
    Executor(_constant_registry(), left).run(plan)
    Executor(_constant_registry(), right).run(plan)
    assert _artifact_bytes(left / "artifacts") == _artifact_bytes(right / "artifacts")


def test_ucb_regret_is_sublinear_over_500_pulls() -> None:
    trace = schedule(StationarySurface((0.1, 0.5, 0.9), 0.02), UCB1(3), Budget(500), 91)
    regret = cumulative_regret(trace)
    assert len(trace) == 500
    assert regret[-1] < 0.1 * len(trace)


def test_three_factor_ablation_grid_has_complete_witness_coverage() -> None:
    factors = {"optimizer": ["a", "b", "c"], "batch": [8, 16, 32], "augment": [False, True]}
    grid = factor_grid(factors)
    rows = [dict(cell, score=float(index)) for index, cell in enumerate(grid)]
    assert len(grid) == 18
    assert coverage(factors, rows) == {name: True for name in sorted(factors)}
    assert missing_cells(factors, rows) == ()

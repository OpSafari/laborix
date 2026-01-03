"""Complete deterministic synthetic research-program demonstration."""

from __future__ import annotations

from pathlib import Path

from laborix.ablation import coverage, factor_grid, result_table
from laborix.report import Report, html_report
from laborix.scheduler import UCB1, Budget, StationarySurface, cumulative_regret, schedule


def run_demo(output: Path) -> dict[str, object]:
    output.mkdir(parents=True, exist_ok=True)
    surface = StationarySurface((0.2, 0.8, 0.5))
    trace = schedule(surface, UCB1(3), Budget(24), seed=7)
    rows = [
        dict(x, score=float(x["method"] == "b") + 0.1 * x["seed"])
        for x in factor_grid({"method": ["a", "b"], "seed": [1, 2]})
    ]
    facts = {
        "synthetic": True,
        "runs": len(trace),
        "regret": cumulative_regret(trace)[-1],
        "coverage": coverage({"method": ["a", "b"], "seed": [1, 2]}, rows),
    }
    report = Report(
        "laborix synthetic demo",
        {"seed": 7, "runs": len(trace)},
        result_table(rows),
        ("Uses a known synthetic reward surface.", "No model or wet-lab result is evaluated."),
    )
    (output / "report.html").write_text(html_report(report))
    return facts

"""Deterministic Markdown and self-contained HTML report synthesis."""

from __future__ import annotations

import html
from dataclasses import dataclass
from typing import Any

from laborix.ablation import ResultTable


@dataclass(frozen=True)
class Report:
    title: str
    metadata: dict[str, Any]
    table: ResultTable
    limitations: tuple[str, ...]


def markdown(report: Report) -> str:
    lines = [f"# {report.title}", "", "## Run metadata", ""] + [
        f"- {k}: {report.metadata[k]}" for k in sorted(report.metadata)
    ]
    lines += [
        "",
        "## Synthetic results",
        "",
        "| " + " | ".join(report.table.columns) + " |",
        "| " + " | ".join("---" for _ in report.table.columns) + " |",
    ]
    lines += ["| " + " | ".join(map(str, row)) + " |" for row in report.table.rows]
    lines += ["", "## Limitations", ""] + [f"- {x}" for x in report.limitations]
    return chr(10).join(lines) + chr(10)


def html_report(report: Report) -> str:
    body = html.escape(markdown(report))
    return f'<!doctype html><meta charset="utf-8"><title>{html.escape(report.title)}</title><pre>{body}</pre>'

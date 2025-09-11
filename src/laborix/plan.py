"""Versioned research-program plan values and validation."""

from __future__ import annotations

from enum import StrEnum


class Stage(StrEnum):
    LITERATURE = "literature"
    IDEATION = "ideation"
    DATA_PREP = "data-prep"
    EXPERIMENT = "experiment"
    ANALYSIS = "analysis"
    REPORT = "report"

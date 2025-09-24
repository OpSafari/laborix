"""Machine-readable plan schema."""

from __future__ import annotations

from typing import Any

PLAN_SCHEMA: dict[str, Any] = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "$id": "https://laborix.dev/schema/plan-2.0.json",
    "type": "object",
    "required": ["schema_version", "name", "steps"],
    "properties": {
        "schema_version": {"const": "2.0"},
        "name": {"type": "string", "minLength": 1},
        "seed": {"type": "integer", "minimum": 0},
        "steps": {"type": "array"},
    },
    "additionalProperties": False,
}


def plan_schema() -> dict[str, Any]:
    """Return an isolated copy of the public schema."""
    import copy

    return copy.deepcopy(PLAN_SCHEMA)

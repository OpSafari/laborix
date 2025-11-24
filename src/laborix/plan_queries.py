"""Read-only queries over research plans."""

from __future__ import annotations

from laborix.plan import Plan


def step_ids(plan: Plan):
    """Return the plan step ids."""
    return tuple(step.id for step in plan.steps)

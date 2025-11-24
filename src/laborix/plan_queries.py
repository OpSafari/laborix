"""Read-only queries over research plans."""

from __future__ import annotations

from laborix.plan import Plan


def step_ids(plan: Plan):
    """Return the plan step ids."""
    return tuple(step.id for step in plan.steps)


def operations(plan: Plan):
    """Return the plan operations."""
    return tuple(sorted({step.operation for step in plan.steps}))


def dependency_count(plan: Plan):
    """Return the plan dependency count."""
    return sum(len(step.dependencies) for step in plan.steps)


def leaf_steps(plan: Plan):
    """Return the plan leaf steps."""
    return tuple(  # noqa: E501
        step.id
        for step in plan.steps
        if not any(step.id in other.dependencies for other in plan.steps)
    )

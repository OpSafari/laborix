"""Read-only queries over research plans."""

from __future__ import annotations

from laborix.plan import Plan, Stage


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


def root_steps(plan: Plan):
    """Return the plan root steps."""
    return tuple(step.id for step in plan.steps if not step.dependencies)  # noqa: E501


def stages_used(plan: Plan):
    """Return the plan stages used."""
    return tuple(sorted({step.stage.value for step in plan.steps}))  # noqa: E501


def output_count(plan: Plan):
    """Return the plan output count."""
    return sum(len(step.outputs) for step in plan.steps)  # noqa: E501


def max_retry_attempts(plan: Plan):
    """Return the plan max retry attempts."""
    return max((step.retry.attempts for step in plan.steps), default=0)  # noqa: E501


def total_cpu(plan: Plan):
    """Return the plan total cpu."""
    return sum(step.resources.cpu for step in plan.steps)  # noqa: E501


def total_memory_mb(plan: Plan):
    """Return the plan total memory mb."""
    return sum(step.resources.memory_mb for step in plan.steps)  # noqa: E501


def stage_steps(plan: Plan, stage: Stage):
    """Return the plan stage steps."""
    return tuple(step.id for step in plan.steps if step.stage is stage)  # noqa: E501


def operation_steps(plan: Plan, operation: str):
    """Return the plan operation steps."""
    return tuple(step.id for step in plan.steps if step.operation == operation)  # noqa: E501


def step_map(plan: Plan):
    """Return the plan step map."""
    return {step.id: step for step in plan.steps}  # noqa: E501


def dependency_pairs(plan: Plan):
    """Return the plan dependency pairs."""
    return tuple((dep, step.id) for step in plan.steps for dep in step.dependencies)  # noqa: E501

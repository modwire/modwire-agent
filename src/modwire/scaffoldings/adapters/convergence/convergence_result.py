from typing import TypedDict

from .convergence_plan import ConvergencePlan


class ConvergenceResult(TypedDict):
    id: str | None
    name: str
    dry_run: bool
    changed: bool
    plan: ConvergencePlan

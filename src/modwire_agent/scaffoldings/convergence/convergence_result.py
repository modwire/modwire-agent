from typing import TypedDict

from pydantic import JsonValue

from .convergence_plan import ConvergencePlan


class ConvergenceResult(TypedDict):
    id: JsonValue
    name: str
    dry_run: bool
    changed: bool
    plan: ConvergencePlan

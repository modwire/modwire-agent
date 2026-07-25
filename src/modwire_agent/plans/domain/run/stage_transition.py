from dataclasses import dataclass

from .plan_run import PlanRun
from .stage_submission import StageSubmission


@dataclass(frozen=True, slots=True)
class StageTransition:
    submission: StageSubmission
    updated_run: PlanRun
    expected_revision: int

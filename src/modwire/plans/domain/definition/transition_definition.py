from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class TransitionDefinition:
    source_stage_id: str
    target_stage_id: str

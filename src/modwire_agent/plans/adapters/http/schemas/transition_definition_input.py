from ninja import Schema


class TransitionDefinitionInput(Schema):
    source_stage_id: str
    target_stage_id: str

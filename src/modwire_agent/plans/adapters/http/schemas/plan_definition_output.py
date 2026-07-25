from ninja import Schema


class PlanDefinitionOutput(Schema):
    id: str
    version: int
    start_stage_id: str

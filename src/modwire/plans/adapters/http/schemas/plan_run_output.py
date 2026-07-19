from ninja import Schema


class PlanRunOutput(Schema):
    id: str
    current_stage_id: str
    status: str

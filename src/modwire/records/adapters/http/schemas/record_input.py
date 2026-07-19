from .strict import StrictSchema


class RecordInput(StrictSchema):
    title: str
    kind: str

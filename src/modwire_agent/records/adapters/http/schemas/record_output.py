from ninja import Schema


class RecordOutput(Schema):
    id: str
    title: str
    kind: str
    status: str

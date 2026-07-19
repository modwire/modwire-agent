from ninja import Schema


class RecordDetailsOutput(Schema):
    id: str
    title: str
    kind: str
    status: str
    tags: list[str]

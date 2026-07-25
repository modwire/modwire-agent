from ninja import Schema


class SectionRecordOutput(Schema):
    id: str
    title: str
    kind: str
    status: str

from ninja import Schema


class ContentOutput(Schema):
    id: str
    schema_version: int

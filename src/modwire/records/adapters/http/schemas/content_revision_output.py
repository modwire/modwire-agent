from ninja import Schema


class ContentRevisionOutput(Schema):
    id: str
    actor_id: str
    actor_type: str
    markdown: str
    schema_version: int

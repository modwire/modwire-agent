from ninja import Schema


class SectionOutput(Schema):
    id: str
    title: str
    allowed_kinds: list[str]

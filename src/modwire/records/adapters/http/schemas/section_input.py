from ninja import Schema


class SectionInput(Schema):
    title: str
    allowed_kinds: list[str]

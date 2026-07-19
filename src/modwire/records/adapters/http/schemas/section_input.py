from .strict import StrictSchema


class SectionInput(StrictSchema):
    title: str
    allowed_kinds: list[str]

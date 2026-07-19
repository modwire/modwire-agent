from ninja import Schema

from .section_record_output import SectionRecordOutput


class SectionDetailsOutput(Schema):
    id: str
    title: str
    allowed_kinds: list[str]
    records: list[SectionRecordOutput]

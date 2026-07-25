from ninja import Schema


class SectionPlacementsOutput(Schema):
    record_ids: list[str]

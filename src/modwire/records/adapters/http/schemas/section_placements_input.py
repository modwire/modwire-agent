from uuid import UUID

from ninja import Schema


class SectionPlacementsInput(Schema):
    record_ids: list[UUID]

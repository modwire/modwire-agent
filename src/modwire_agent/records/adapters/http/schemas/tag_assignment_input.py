from uuid import UUID

from ninja import Schema


class TagAssignmentInput(Schema):
    tag_ids: list[UUID]

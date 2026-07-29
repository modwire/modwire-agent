from typing import Any
from uuid import UUID

from ninja import Schema
from pydantic import ConfigDict

from ...domain.collaboration.actor import Actor
from ...domain.collaboration.invalid import InvalidActor
from ..actor_policy import ActorPolicy


class ActorHeaders:
    @staticmethod
    def extract(request: Any, policy: ActorPolicy) -> Actor:
        actor_id = request.headers.get("X-Actor-Id")
        actor_type = request.headers.get("X-Actor-Type")
        missing = [
            name
            for name, value in (("X-Actor-Id", actor_id), ("X-Actor-Type", actor_type))
            if not value or not value.strip()
        ]
        if missing:
            raise InvalidActor(f"Missing required actor headers: {', '.join(missing)}.")
        return policy.identify(actor_id, actor_type)


class StrictSchema(Schema):
    model_config = ConfigDict(extra="forbid")


class ContentInput(Schema):
    markdown: str


class ContentOutput(Schema):
    id: str
    schema_version: int


class ContentProposalDetailsOutput(Schema):
    id: str
    markdown: str
    proposed_by_id: str
    proposed_by_type: str
    status: str


class ContentProposalOutput(Schema):
    id: str
    status: str


class ContentRevisionOutput(Schema):
    id: str
    actor_id: str
    actor_type: str
    markdown: str
    schema_version: int


class ProposalStatusInput(Schema):
    status: str


class RecordDetailsOutput(Schema):
    id: str
    title: str
    kind: str
    status: str
    tags: list[str]


class RecordInput(StrictSchema):
    title: str
    kind: str


class RecordOutput(Schema):
    id: str
    title: str
    kind: str
    status: str


class RecordTitleInput(Schema):
    title: str


class RoutedRecordOutput(Schema):
    id: str
    title: str
    reason: str | None = None


class SearchResultOutput(Schema):
    id: str
    title: str
    reason: str


class SectionRecordOutput(Schema):
    id: str
    title: str
    kind: str
    status: str


class SectionDetailsOutput(Schema):
    id: str
    title: str
    allowed_kinds: list[str]
    records: list[SectionRecordOutput]


class SectionInput(StrictSchema):
    title: str
    allowed_kinds: list[str]


class SectionOutput(Schema):
    id: str
    title: str
    allowed_kinds: list[str]


class SectionPlacementsInput(Schema):
    record_ids: list[UUID]


class SectionPlacementsOutput(Schema):
    record_ids: list[str]


class TagAssignmentInput(Schema):
    tag_ids: list[UUID]


class TagInput(StrictSchema):
    name: str


class TagOutput(Schema):
    id: str
    name: str

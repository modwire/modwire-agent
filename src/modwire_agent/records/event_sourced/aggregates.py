from uuid import UUID

from eventsourcing.domain import Aggregate, event


class Section(Aggregate):
    @event("SectionCreated")
    def __init__(self, title: str, allowed_kinds: list[str]) -> None:
        self.title = title
        self.allowed_kinds = allowed_kinds
        self.record_ids: list[UUID] = []

    @event("RecordPlaced")
    def place(self, record_id: UUID) -> None:
        self.record_ids.append(record_id)

    @event("RecordsReordered")
    def reorder(self, record_ids: list[UUID]) -> None:
        if set(record_ids) != set(self.record_ids) or len(record_ids) != len(self.record_ids):
            raise ValueError("Placements must contain each section record exactly once.")
        self.record_ids = record_ids


class Tag(Aggregate):
    @event("TagCreated")
    def __init__(self, name: str) -> None:
        self.name = name


class Record(Aggregate):
    @event("RecordCreated")
    def __init__(self, title: str, kind: str, section_id: UUID) -> None:
        self.title = title
        self.kind = kind
        self.section_id = section_id
        self.status = "draft"
        self.tag_names: list[str] = []
        self.markdown = ""
        self.schema_version = 0

    @event("RecordRenamed")
    def rename(self, title: str) -> None:
        self.title = title

    @event("TagsAssigned")
    def assign_tags(self, tag_names: list[str]) -> None:
        self.tag_names = tag_names

    @event("ContentReplaced")
    def replace_content(
        self, revision_id: UUID, markdown: str, schema_version: int, actor_id: str, actor_kind: str
    ) -> None:
        self.markdown = markdown
        self.schema_version = schema_version

    @event("RecordPublished")
    def publish(self) -> None:
        if not self.markdown:
            raise ValueError("A record needs content before it can be published.")
        self.status = "published"

    @event("RecordArchived")
    def archive(self) -> None:
        if self.status == "archived":
            raise ValueError("Record is already archived.")
        self.status = "archived"


class ContentProposal(Aggregate):
    @event("ProposalCreated")
    def __init__(self, record_id: UUID, markdown: str, actor_id: str, actor_kind: str) -> None:
        self.record_id = record_id
        self.markdown = markdown
        self.actor_id = actor_id
        self.actor_kind = actor_kind
        self.status = "proposed"

    @event("ProposalResolved")
    def resolve(self, status: str) -> None:
        if self.status != "proposed":
            raise ValueError("Only proposed content can be resolved.")
        if status not in {"accepted", "rejected"}:
            raise ValueError("Proposal status must be accepted or rejected.")
        self.status = status

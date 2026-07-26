from uuid import UUID

from eventsourcing.application import Application

from .aggregates import ContentProposal, Record, Section, Tag


class RecordsApplication(Application):
    name = "Records"
    snapshotting_intervals = {Record: 20, Section: 20, ContentProposal: 20}

    def create_section(self, title: str, allowed_kinds: list[str]) -> Section:
        section = Section(title, allowed_kinds)
        self.save(section)
        return section

    def create_tag(self, name: str) -> Tag:
        tag = Tag(name.strip().lower())
        self.save(tag)
        return tag

    def create_record(self, section_id: UUID, title: str, kind: str) -> Record:
        section = self.repository.get(section_id)
        if kind not in section.allowed_kinds:
            raise ValueError(f"Record kind '{kind}' is not allowed in this section.")
        record = Record(title.strip(), kind, section_id)
        section.place(record.id)
        self.save(record, section)
        return record

    def reorder_section(self, section_id: UUID, record_ids: list[UUID]) -> Section:
        section = self.repository.get(section_id)
        section.reorder(record_ids)
        self.save(section)
        return section

    def rename_record(self, record_id: UUID, title: str) -> Record:
        record = self.repository.get(record_id)
        record.rename(title)
        self.save(record)
        return record

    def assign_tags(self, record_id: UUID, tag_ids: list[UUID]) -> Record:
        record = self.repository.get(record_id)
        tag_names = [self.repository.get(tag_id).name for tag_id in tag_ids]
        if len(set(tag_names)) != len(tag_names):
            raise ValueError("A record cannot receive the same tag twice.")
        record.assign_tags(tag_names)
        self.save(record)
        return record

    def replace_content(self, record_id: UUID, markdown: str, actor_id: str, actor_kind: str) -> UUID:
        record = self.repository.get(record_id)
        revision_id = Record.create_id()
        record.replace_content(revision_id, markdown, record.schema_version + 1, actor_id, actor_kind)
        self.save(record)
        return revision_id

    def publish_record(self, record_id: UUID) -> Record:
        record = self.repository.get(record_id)
        record.publish()
        self.save(record)
        return record

    def archive_record(self, record_id: UUID) -> None:
        record = self.repository.get(record_id)
        record.archive()
        self.save(record)

    def propose_content(self, record_id: UUID, markdown: str, actor_id: str, actor_kind: str) -> ContentProposal:
        self.repository.get(record_id)
        proposal = ContentProposal(record_id, markdown, actor_id, actor_kind)
        self.save(proposal)
        return proposal

    def resolve_proposal(self, proposal_id: UUID, status: str) -> ContentProposal:
        proposal = self.repository.get(proposal_id)
        proposal.resolve(status)
        aggregates = [proposal]
        if status == "accepted":
            record = self.repository.get(proposal.record_id)
            record.replace_content(
                Record.create_id(), proposal.markdown, record.schema_version + 1, proposal.actor_id, proposal.actor_kind
            )
            aggregates.append(record)
        self.save(*aggregates)
        return proposal

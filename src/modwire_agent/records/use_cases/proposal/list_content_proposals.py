from dataclasses import dataclass
from uuid import UUID

from ...domain.proposal.content_proposal import ContentProposal
from ...ports.outbound import ContentProposalStore, RecordStore


@dataclass(frozen=True, slots=True)
class ListContentProposals:
    records: RecordStore
    proposals: ContentProposalStore

    def execute(self, record_id: UUID) -> list[ContentProposal]:
        self.records.get(record_id)
        return self.proposals.for_record(record_id)

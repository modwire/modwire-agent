from dataclasses import dataclass
from uuid import UUID

from ...domain.proposal.content_proposal import ContentProposal
from ...ports.proposal.content_proposal_store import ContentProposalStore
from ...ports.record.record_store import RecordStore


@dataclass(frozen=True, slots=True)
class ListContentProposals:
    records: RecordStore
    proposals: ContentProposalStore

    def execute(self, record_id: UUID) -> list[ContentProposal]:
        self.records.get(record_id)
        return self.proposals.for_record(record_id)

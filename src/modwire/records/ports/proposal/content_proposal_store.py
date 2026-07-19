from abc import ABC, abstractmethod
from uuid import UUID

from ...domain.proposal.content_proposal import ContentProposal


class ContentProposalStore(ABC):
    @abstractmethod
    def for_record(self, record_id: UUID) -> list[ContentProposal]:
        raise NotImplementedError

    @abstractmethod
    def get(self, proposal_id: UUID) -> ContentProposal:
        raise NotImplementedError

    @abstractmethod
    def save(self, proposal: ContentProposal) -> None:
        raise NotImplementedError

from dataclasses import dataclass
from uuid import UUID, uuid4

from ..collaboration.actor import Actor
from .content_proposal import ContentProposal
from .invalid import InvalidProposal
from .status import ProposalStatus


@dataclass(frozen=True, slots=True)
class ContentProposalPolicy:
    def propose(self, record_id: UUID, markdown: str, actor: Actor) -> ContentProposal:
        return ContentProposal(
            identifier=uuid4(),
            record_id=record_id,
            proposed_by=actor,
            markdown=markdown,
            status=ProposalStatus.PROPOSED,
        )

    def resolve(self, proposal: ContentProposal, status: str, actor: Actor) -> ContentProposal:
        if proposal.status is not ProposalStatus.PROPOSED:
            raise InvalidProposal("Only a proposed change can be resolved.")
        try:
            resolution = ProposalStatus(status)
        except ValueError as error:
            raise InvalidProposal("Proposal status must be accepted or rejected.") from error
        if resolution is ProposalStatus.PROPOSED:
            raise InvalidProposal("Proposal status must be accepted or rejected.")
        return ContentProposal(
            identifier=proposal.identifier,
            record_id=proposal.record_id,
            proposed_by=proposal.proposed_by,
            markdown=proposal.markdown,
            status=resolution,
        )

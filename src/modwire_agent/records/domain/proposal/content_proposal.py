from dataclasses import dataclass
from uuid import UUID

from ..collaboration.actor import Actor
from .status import ProposalStatus


@dataclass(frozen=True, slots=True)
class ContentProposal:
    identifier: UUID
    record_id: UUID
    proposed_by: Actor
    markdown: str
    status: ProposalStatus

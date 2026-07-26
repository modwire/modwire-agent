from dataclasses import dataclass
from uuid import UUID

from ...domain.collaboration.actor import Actor
from ...domain.collaboration.policy import ActorPolicy
from ...domain.proposal.content_proposal import ContentProposal
from ...domain.proposal.policy import ContentProposalPolicy
from ...domain.record.content_schema_policy import ContentSchemaPolicy
from ...ports.outbound import ContentProposalStore, RecordStore


@dataclass(frozen=True, slots=True)
class ProposeContent:
    records: RecordStore
    proposals: ContentProposalStore
    actors: ActorPolicy
    content_schema: ContentSchemaPolicy
    policy: ContentProposalPolicy

    def execute(self, record_id: UUID, markdown: str, actor: Actor) -> ContentProposal:
        self.actors.allow_proposing(actor)
        self.content_schema.validate(self.records.get(record_id), markdown)
        proposal = self.policy.propose(record_id, markdown, actor)
        self.proposals.save(proposal)
        return proposal

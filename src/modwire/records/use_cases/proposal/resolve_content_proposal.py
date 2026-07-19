from dataclasses import dataclass
from uuid import UUID

from ...domain.collaboration.actor import Actor
from ...domain.collaboration.policy import ActorPolicy
from ...domain.proposal.content_proposal import ContentProposal
from ...domain.proposal.policy import ContentProposalPolicy
from ...domain.record.content_revision import ContentRevision
from ...domain.record.content_schema_policy import ContentSchemaPolicy
from ...ports.proposal.content_proposal_store import ContentProposalStore
from ...ports.record.content_store import ContentStore
from ...ports.record.record_store import RecordStore


@dataclass(frozen=True, slots=True)
class ResolveContentProposal:
    records: RecordStore
    proposals: ContentProposalStore
    content: ContentStore
    actors: ActorPolicy
    content_schema: ContentSchemaPolicy
    policy: ContentProposalPolicy

    def execute(self, proposal_id: UUID, status: str, actor: Actor) -> ContentProposal:
        self.actors.allow_resolving_proposals(actor)
        proposal = self.policy.resolve(self.proposals.get(proposal_id), status, actor)
        if proposal.status.value == "accepted":
            revision = self.content_schema.create_revision(self.records.get(proposal.record_id), proposal.markdown, self.content.next_version(proposal.record_id), proposal.proposed_by)
            self.content.save(revision)
        self.proposals.save(proposal)
        return proposal

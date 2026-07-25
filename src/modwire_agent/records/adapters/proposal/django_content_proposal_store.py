from uuid import UUID

from modwire_hex.django import DjangoRepository

from ...domain.collaboration.actor import Actor
from ...domain.collaboration.actor_kind import ActorKind
from ...domain.proposal.content_proposal import ContentProposal
from ...domain.proposal.status import ProposalStatus
from ...ports.proposal.content_proposal_store import ContentProposalStore
from ..django.models import ContentProposalModel


class DjangoContentProposalStore(DjangoRepository[ContentProposal, ContentProposalModel, UUID], ContentProposalStore):
    def for_record(self, record_id: UUID) -> list[ContentProposal]:
        return [
            self.to_domain(model)
            for model in ContentProposalModel.objects.filter(record_id=record_id).order_by("identifier")
        ]

    def key_of(self, domain: ContentProposal) -> UUID:
        return domain.identifier

    def find_record(self, key: UUID) -> ContentProposalModel | None:
        try:
            return ContentProposalModel.objects.get(identifier=key)
        except ContentProposalModel.DoesNotExist:
            return None

    def create_record(self, domain: ContentProposal) -> ContentProposalModel:
        return ContentProposalModel(
            identifier=domain.identifier,
            record_id=domain.record_id,
            proposed_by_id=domain.proposed_by.identifier,
            proposed_by_kind=domain.proposed_by.kind,
            markdown=domain.markdown,
            status=domain.status,
        )

    def update_record(self, model: ContentProposalModel, domain: ContentProposal) -> None:
        model.status = domain.status

    def get(self, proposal_id: UUID) -> ContentProposal:
        proposal = self.load(proposal_id)
        if proposal is None:
            raise LookupError(f"Content proposal {proposal_id!r} was not found.")
        return proposal

    def to_domain(self, model: ContentProposalModel) -> ContentProposal:
        return ContentProposal(
            identifier=model.identifier,
            record_id=model.record_id,
            proposed_by=Actor(identifier=model.proposed_by_id, kind=ActorKind(model.proposed_by_kind)),
            markdown=model.markdown,
            status=ProposalStatus(model.status),
        )

from typing import Any
from uuid import UUID

from modwire_hex.django import DjangoRequest
from ninja_extra import ControllerBase, api_controller, route

from ...domain.collaboration.policy import ActorPolicy
from ...use_cases.proposal.resolve_content_proposal import ResolveContentProposal
from .actor_headers import ActorHeaders
from .schemas.content_proposal_output import ContentProposalOutput
from .schemas.proposal_status_input import ProposalStatusInput


@api_controller("/content-proposals", tags=["records"])
class ContentProposalsController(ControllerBase):
    @route.patch("/{proposal_id}", response={200: ContentProposalOutput}, operation_id="resolve_content_proposal")
    def resolve(
        self, request: Any, proposal_id: UUID, payload: ProposalStatusInput
    ) -> tuple[int, ContentProposalOutput]:
        actor = ActorHeaders.extract(request, DjangoRequest.resolve(request, ActorPolicy))
        proposal = DjangoRequest.resolve(request, ResolveContentProposal).execute(proposal_id, payload.status, actor)
        return 200, ContentProposalOutput(id=str(proposal.identifier), status=proposal.status)

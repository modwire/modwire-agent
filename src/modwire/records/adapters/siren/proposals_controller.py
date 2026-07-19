from typing import Any
from uuid import UUID

from modwire_hex.django import DjangoRequest
from modwire_siren import SirenEntityRequest
from ninja.errors import HttpError
from ninja_extra import ControllerBase, api_controller, route

from modwire.core.siren import project_siren, siren_response

from ...domain.collaboration.invalid import InvalidActor
from ...domain.collaboration.policy import ActorPolicy
from ...domain.proposal.invalid import InvalidProposal
from ...use_cases.proposal.resolve_content_proposal import ResolveContentProposal
from ..http.actor_headers import ActorHeaders
from ..http.schemas.proposal_status_input import ProposalStatusInput
from .contract import COLLECTION_ROUTE, IDENTIFIER_PARAMETER, PROPOSAL_IDENTIFIER_PARAMETER, PROPOSAL_RESOURCE_NAME, RESOLVE_PROPOSAL_OPERATION


@api_controller(COLLECTION_ROUTE + "/{record_id}/content-proposals", tags=["records"])
class ContentProposalsSirenController(ControllerBase):
    @route.patch("/{proposal_id}", response=dict, operation_id=RESOLVE_PROPOSAL_OPERATION)
    def resolve(self, request: Any, record_id: UUID, proposal_id: UUID, payload: ProposalStatusInput):
        try:
            actor = ActorHeaders.extract(request, DjangoRequest.resolve(request, ActorPolicy))
            proposal = DjangoRequest.resolve(request, ResolveContentProposal).execute(proposal_id, payload.status, actor)
        except (InvalidActor, InvalidProposal) as error:
            raise HttpError(422, str(error)) from error
        return siren_response(project_siren(request).document(SirenEntityRequest(resource_name=PROPOSAL_RESOURCE_NAME, properties={"id": str(proposal.identifier), "status": proposal.status}, operation_ids=(RESOLVE_PROPOSAL_OPERATION,), path_values={IDENTIFIER_PARAMETER: record_id, PROPOSAL_IDENTIFIER_PARAMETER: proposal.identifier}, entities=())))

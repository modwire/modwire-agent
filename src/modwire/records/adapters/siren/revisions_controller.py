from typing import Any
from uuid import UUID

from modwire_hex.django import DjangoRequest
from modwire_siren import SirenEntityRequest
from ninja.errors import HttpError
from ninja_extra import ControllerBase, api_controller, route

from modwire.core.siren import project_siren, siren_response

from ...use_cases.record.list_content_revisions import ListContentRevisions
from .contract import COLLECTION_ROUTE, GET_REVISION_OPERATION, IDENTIFIER_PARAMETER, REVISION_IDENTIFIER_PARAMETER, REVISION_RESOURCE_NAME


@api_controller(COLLECTION_ROUTE + "/{record_id}/content-revisions", tags=["records"])
class ContentRevisionsSirenController(ControllerBase):
    @route.get("/{revision_id}", response=dict, operation_id=GET_REVISION_OPERATION)
    def get_revision(self, request: Any, record_id: UUID, revision_id: UUID):
        revision = next((item for item in DjangoRequest.resolve(request, ListContentRevisions).execute(record_id) if item.identifier == revision_id), None)
        if revision is None: raise HttpError(404, "Content revision not found.")
        return siren_response(project_siren(request).document(SirenEntityRequest(resource_name=REVISION_RESOURCE_NAME, properties={"id": str(revision.identifier), "actor_id": revision.actor.identifier, "actor_type": revision.actor.kind, "markdown": revision.markdown, "schema_version": revision.schema_version}, operation_ids=(GET_REVISION_OPERATION,), path_values={IDENTIFIER_PARAMETER: record_id, REVISION_IDENTIFIER_PARAMETER: revision.identifier}, entities=())))

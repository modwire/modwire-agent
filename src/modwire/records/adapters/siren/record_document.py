from typing import Any
from uuid import UUID

from modwire_hex.django import DjangoRequest
from modwire_siren import SirenEntityRequest

from modwire.core.siren import project_siren, siren_response

from ...use_cases.record.get_record_details import GetRecordDetails
from .contract import ARCHIVE_OPERATION, ASSIGN_TAGS_OPERATION, GET_OPERATION, IDENTIFIER_PARAMETER, LIST_PROPOSALS_OPERATION, LIST_REVISIONS_OPERATION, PROPOSE_CONTENT_OPERATION, PUBLISH_OPERATION, RENAME_OPERATION, REPLACE_CONTENT_OPERATION, RESOURCE_NAME


class RecordDocument:
    def __call__(self, request: Any, record_id: UUID):
        record = DjangoRequest.resolve(request, GetRecordDetails).execute(record_id)
        return siren_response(project_siren(request).document(SirenEntityRequest(resource_name=RESOURCE_NAME, properties={"id": str(record.identifier), "title": record.title, "kind": record.kind, "status": record.status, "tags": list(record.tag_names)}, operation_ids=(GET_OPERATION, ASSIGN_TAGS_OPERATION, REPLACE_CONTENT_OPERATION, PROPOSE_CONTENT_OPERATION, PUBLISH_OPERATION, RENAME_OPERATION, ARCHIVE_OPERATION, LIST_REVISIONS_OPERATION, LIST_PROPOSALS_OPERATION), path_values={IDENTIFIER_PARAMETER: record.identifier}, entities=())))


record_document = RecordDocument()

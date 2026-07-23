from typing import Any

from modwire_hex.django import DjangoRequest
from modwire_siren import SirenCollectionRequest, SirenEntityRequest
from ninja.errors import HttpError
from ninja_extra import ControllerBase, api_controller, route

from modwire.core.siren import project_siren, siren_response

from ...use_cases.language.get_language import GetLanguage
from ...use_cases.language.list_languages import ListLanguages
from .contract import (
    COLLECTION_ROUTE,
    ENTITY_ROUTE,
    GET_OPERATION,
    IDENTIFIER_PARAMETER,
    LIST_OPERATION,
    RESOURCE_NAME,
)


@api_controller(COLLECTION_ROUTE, tags=["languages"], auto_import=False)
class LanguagesSirenController(ControllerBase):
    @route.get("", response=dict, operation_id=LIST_OPERATION)
    def list_languages(self, request: Any):
        languages = DjangoRequest.resolve(request, ListLanguages).execute()
        document = project_siren(request).collection(
            SirenCollectionRequest(
                resource_name=RESOURCE_NAME,
                items=tuple(language.model_dump() for language in languages),
                collection_operation_ids=(LIST_OPERATION,),
                item_operation_ids=(GET_OPERATION,),
                path_values={},
            )
        )
        return siren_response(document)

    @route.get(ENTITY_ROUTE, response=dict, operation_id=GET_OPERATION)
    def get_language(self, request: Any, language_id: str):
        try:
            language = DjangoRequest.resolve(request, GetLanguage).execute(language_id)
        except LookupError as error:
            raise HttpError(404, str(error)) from error
        document = project_siren(request).document(
            SirenEntityRequest(
                resource_name=RESOURCE_NAME,
                properties=language.model_dump(),
                operation_ids=(GET_OPERATION,),
                path_values={IDENTIFIER_PARAMETER: language.id},
                entities=(),
            )
        )
        return siren_response(document)

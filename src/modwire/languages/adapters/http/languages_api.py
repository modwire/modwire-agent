from typing import Any

from modwire_hex.django import DjangoRequest
from ninja.errors import HttpError
from ninja_extra import ControllerBase, api_controller, route

from ...use_cases.language.get_language import GetLanguage
from ...use_cases.language.list_languages import ListLanguages
from .schemas.language_output import LanguageOut


@api_controller("/languages", tags=["languages"])
class LanguagesController(ControllerBase):
    @route.get("", response={200: list[LanguageOut]}, operation_id="list_languages")
    def list_languages(self, request: Any) -> tuple[int, list[LanguageOut]]:
        languages = DjangoRequest.resolve(request, ListLanguages).execute()
        return 200, [LanguageOut(**language.model_dump()) for language in languages]

    @route.get("/{language_id}", response={200: LanguageOut}, operation_id="get_language")
    def get_language(self, request: Any, language_id: str) -> tuple[int, LanguageOut]:
        try:
            language = DjangoRequest.resolve(request, GetLanguage).execute(language_id)
        except LookupError as error:
            raise HttpError(404, str(error)) from error
        return 200, LanguageOut(**language.model_dump())

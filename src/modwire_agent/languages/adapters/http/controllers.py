from typing import Any

from modwire_hex.django import DjangoRequest
from ninja_extra import ControllerBase, api_controller, route

from ...use_cases.get_language import GetLanguage
from ...use_cases.list_languages import ListLanguages
from .schemas import LanguageOut


@api_controller("/languages", tags=["languages"])
class LanguagesController(ControllerBase):
    @route.get("", response={200: list[LanguageOut]}, operation_id="list_languages")
    def list_languages(self, request: Any) -> tuple[int, list[LanguageOut]]:
        """List every supported language and its toolchain metadata."""
        languages = DjangoRequest.resolve(request, ListLanguages).execute()
        return 200, [LanguageOut(**language.model_dump()) for language in languages]

    @route.get("/{language_id}", response={200: LanguageOut}, operation_id="get_language")
    def get_language(self, request: Any, language_id: str) -> tuple[int, LanguageOut]:
        """Return the metadata for one supported language."""
        language = DjangoRequest.resolve(request, GetLanguage).execute(language_id)
        return 200, LanguageOut(**language.model_dump())

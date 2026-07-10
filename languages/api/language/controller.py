from typing import Annotated

from ninja import Status
from ninja_extra import ControllerBase, api_controller, route
from wireup import Inject
from wireup.integration.django import inject

from ...services.language import LanguageService
from .schemas import LanguageIn, LanguageOut, LanguagePatchIn


@api_controller("/languages", tags=["Languages"])
class LanguageController(ControllerBase):
    @route.get(
        "",
        response=list[LanguageOut],
        operation_id="list_languages",
        summary="List languages.",
    )
    @inject
    def list(self, service: Annotated[LanguageService, Inject()]):
        return service.list()

    @route.get(
        "/{language_id}",
        response=LanguageOut,
        operation_id="get_language",
        summary="Get language.",
    )
    @inject
    def get(self, language_id: int, service: Annotated[LanguageService, Inject()]):
        return service.get(language_id)

    @route.post(
        "",
        response=LanguageOut,
        operation_id="create_language",
        summary="Create language.",
    )
    @inject
    def create(self, data: LanguageIn, service: Annotated[LanguageService, Inject()]):
        return service.create(**data.model_dump())

    @route.put(
        "/{language_id}",
        response=LanguageOut,
        operation_id="update_language",
        summary="Update language.",
    )
    @inject
    def update(
        self,
        language_id: int,
        data: LanguageIn,
        service: Annotated[LanguageService, Inject()],
    ):
        return service.update(language_id, **data.model_dump())

    @route.patch(
        "/{language_id}",
        response=LanguageOut,
        operation_id="partial_update_language",
        summary="Partially update language.",
    )
    @inject
    def partial_update(
        self,
        language_id: int,
        data: LanguagePatchIn,
        service: Annotated[LanguageService, Inject()],
    ):
        return service.update(language_id, **data.model_dump(exclude_unset=True))

    @route.delete(
        "/{language_id}",
        response={204: None},
        operation_id="delete_language",
        summary="Delete language.",
    )
    @inject
    def delete(self, language_id: int, service: Annotated[LanguageService, Inject()]):
        service.delete(language_id)
        return Status(204, None)

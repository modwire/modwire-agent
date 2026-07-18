from typing import Annotated

from ninja_extra import ControllerBase, api_controller, route
from wireup import Inject
from wireup.integration.django import inject

from modwire.shared.api.hypermedia import siren_resource
from modwire.shared.languages import LanguageCatalogService

from .schemas import LanguageOut


@siren_resource(
    name="language",
    path="/api/languages",
    class_="language",
    identifier="id",
    path_parameters={},
    relations={},
    collection_only=True,
)
@api_controller("/languages", tags=["Languages"])
class LanguageController(ControllerBase):
    @route.get(
        "",
        response=list[LanguageOut],
        operation_id="list_languages",
        summary="List languages.",
    )
    @inject
    def find_all(self, service: Annotated[LanguageCatalogService, Inject()]):
        return service.find_all()

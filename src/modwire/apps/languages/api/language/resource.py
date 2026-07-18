from modwire.shared.api.hypermedia import CollectionResource, ResourceSpec
from modwire.shared.languages import LanguageCatalogService

from .schemas import LanguageOut

language = CollectionResource(
    name="language",
    collection_path="/api/languages",
    out_schema=LanguageOut,
    service=LanguageCatalogService,
    tags=("Languages",),
    summary="List languages.",
    service_method="find_all",
)

SIREN_RESOURCES = (
    ResourceSpec(
        name="language",
        path="/api/languages",
        resource_class="language",
        identifier="id",
        path_parameters={},
        relations={},
        collection_only=True,
    ),
)

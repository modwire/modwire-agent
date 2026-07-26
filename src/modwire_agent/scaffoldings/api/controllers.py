from django.conf import settings
from modwire_hex.django import DjangoRequest
from ninja_extra import ControllerBase, api_controller, route

from ..services import ScaffoldingService
from . import schemas


@api_controller("", tags=["Root"])
class RootController(ControllerBase):
    @route.get("/", response=dict, operation_id="get_api_root", summary="Discover the API.")
    def get(self):
        """Return links to the API's public entry points."""
        return {
            "title": "Modwire API",
            "version": settings.RELEASE_VERSION,
        }


@api_controller("/scaffoldings", tags=["Scaffoldings"])
class ScaffoldingController(ControllerBase):
    service: ScaffoldingService

    @route.post("", response=schemas.Scaffolding, operation_id="create_scaffolding", summary="Add new source code scaffolding.")
    def create( self, request, body: schemas.NewScaffolding):
        return self.service

    @route.get(
        "/{scaffolding_id}/schema",
        response=ScaffoldingFormSchemaOut,
        by_alias=True,
        operation_id="get_scaffolding_schema",
        summary="Get the scaffolding variable form schema.",
    )
    def schema(
        self,
        request,
        scaffolding_id: str,
    ):
        """Return the variable form schema for one scaffolding."""
        activity = DjangoRequest.resolve(request, GetScaffoldingSchema)
        return activity.execute(scaffolding_id)

    @route.get(
        "/{scaffolding_id}/bundle",
        response=ScaffoldingBundleOut,
        operation_id="get_scaffolding_bundle",
        summary="Get a generic scaffolding bundle for a local generator.",
    )
    def bundle(self, request, scaffolding_id: str):
        """Return the generator bundle for one scaffolding."""
        activity = DjangoRequest.resolve(request, GetScaffoldingBundle)
        return activity.execute(scaffolding_id)

    @route.post(
        "/{scaffolding_id}/preview",
        response={200: ScaffoldingPreviewOut, 422: ScaffoldingPreviewErrorOut},
        operation_id="preview_scaffolding",
        summary="Preview a rendered scaffolding.",
    )
    def preview(
        self,
        request,
        scaffolding_id: str,
        data: ScaffoldingPreviewIn,
    ):
        """Render a validated preview for one scaffolding."""
        activity = DjangoRequest.resolve(request, PreviewScaffolding)
        return activity.execute(
            scaffolding_id,
            data.values,
            [override.model_dump(exclude_none=True) for override in data.template_overrides],
        )

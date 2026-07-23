from modwire_hex.django import DjangoRequest
from ninja_extra import route
from ninja_extra.controllers import ControllerBase, api_controller

from ....use_cases.converge_scaffolding import ConvergeScaffolding
from ....use_cases.get_scaffolding_bundle import GetScaffoldingBundle
from ....use_cases.get_scaffolding_schema import GetScaffoldingSchema
from ....use_cases.preview_scaffolding import PreviewScaffolding
from .schemas import (
    ScaffoldingBundleOut,
    ScaffoldingConvergenceIn,
    ScaffoldingConvergenceOut,
    ScaffoldingFormSchemaOut,
    ScaffoldingPreviewErrorOut,
    ScaffoldingPreviewIn,
    ScaffoldingPreviewOut,
)


@api_controller("/scaffoldings", tags=["Scaffoldings"])
class ScaffoldingController(ControllerBase):
    @route.post(
        "/converge",
        response=ScaffoldingConvergenceOut,
        operation_id="converge_scaffolding",
        summary="Validate or transactionally reconcile a complete scaffolding aggregate.",
    )
    def converge(
        self,
        request,
        data: ScaffoldingConvergenceIn,
    ):
        service = DjangoRequest.resolve(request, ConvergeScaffolding)
        return service.execute(data.model_dump())

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
        activity = DjangoRequest.resolve(request, GetScaffoldingSchema)
        return activity.execute(scaffolding_id)

    @route.get(
        "/{scaffolding_id}/bundle",
        response=ScaffoldingBundleOut,
        operation_id="get_scaffolding_bundle",
        summary="Get a generic scaffolding bundle for a local generator.",
    )
    def bundle(self, request, scaffolding_id: str):
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
        activity = DjangoRequest.resolve(request, PreviewScaffolding)
        return activity.execute(
            scaffolding_id,
            data.values,
            [override.model_dump(exclude_none=True) for override in data.template_overrides],
        )

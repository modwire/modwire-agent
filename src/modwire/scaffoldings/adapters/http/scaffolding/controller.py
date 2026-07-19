from modwire_hex.django import DjangoRequest
from ninja import Status
from ninja_extra import route
from ninja_extra.controllers import ControllerBase, api_controller

from modwire.scaffoldings.adapters.http.errors import validated

from ....use_cases.bundle import ScaffoldingBundleService
from ....use_cases.converge_scaffolding import ConvergeScaffolding
from ....use_cases.preview import ScaffoldingPreviewService
from ....use_cases.preview_errors import PreviewFailed
from ....use_cases.scaffolding import ScaffoldingService
from ....use_cases.schema import ScaffoldingSchemaService
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
        return validated(service.execute, data.model_dump())

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
        scaffoldings = DjangoRequest.resolve(request, ScaffoldingService)
        schemas = DjangoRequest.resolve(request, ScaffoldingSchemaService)
        return schemas.build(scaffoldings.get(scaffolding_id))

    @route.get(
        "/{scaffolding_id}/bundle",
        response=ScaffoldingBundleOut,
        operation_id="get_scaffolding_bundle",
        summary="Get a generic scaffolding bundle for a local generator.",
    )
    def bundle(self, request, scaffolding_id: str):
        service = DjangoRequest.resolve(request, ScaffoldingBundleService)
        return service.get(scaffolding_id)

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
        service = DjangoRequest.resolve(request, ScaffoldingPreviewService)
        try:
            return service.preview(
                scaffolding_id,
                data.values,
                [override.model_dump(exclude_none=True) for override in data.template_overrides],
            )
        except PreviewFailed as error:
            return Status(422, {"errors": [item.as_dict() for item in error.errors]})

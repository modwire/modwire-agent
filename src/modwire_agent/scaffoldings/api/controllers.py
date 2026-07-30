from modwire_hex.django import DjangoRequest
from ninja import Status
from ninja_extra import ControllerBase, api_controller, route

from ..services import ScaffoldingService
from . import schemas


@api_controller("/scaffoldings", tags=["Scaffoldings"])
class ScaffoldingController(ControllerBase):
    @route.post("", response={201: schemas.Scaffolding}, operation_id="create_scaffolding")
    def create(self, request, body: schemas.ScaffoldingInput):
        scaffolding = DjangoRequest.resolve(request, ScaffoldingService).create(body.model_dump(mode="json"))
        return Status(201, scaffolding)

    @route.get("", response=list[schemas.ScaffoldingSummary], operation_id="find_scaffoldings")
    def find_all(self, request):
        return DjangoRequest.resolve(request, ScaffoldingService).find_all()

    @route.get("/{scaffolding_id}", response=schemas.Scaffolding, operation_id="get_scaffolding")
    def get(self, request, scaffolding_id: str):
        return DjangoRequest.resolve(request, ScaffoldingService).get(scaffolding_id)

    @route.put("/{scaffolding_id}", response=schemas.Scaffolding, operation_id="update_scaffolding")
    def update(self, request, scaffolding_id: str, body: schemas.ScaffoldingInput):
        return DjangoRequest.resolve(request, ScaffoldingService).update(scaffolding_id, body.model_dump(mode="json"))

    @route.post("/{scaffolding_id}/render", response=schemas.Rendering, operation_id="render_scaffolding")
    def create_rendering(self, request, scaffolding_id: str, body: schemas.GenerateSourceCode):
        return {
            "files": DjangoRequest.resolve(
                request,
                ScaffoldingService,
            ).render(scaffolding_id, body.parameters).package.files,
        }

    @route.delete("/{scaffolding_id}", response={204: None}, operation_id="delete_scaffolding")
    def delete(self, request, scaffolding_id: str):
        DjangoRequest.resolve(request, ScaffoldingService).delete(scaffolding_id)
        return Status(204, None)

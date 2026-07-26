from django.conf import settings
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

    @route.post("", operation_id="create_scaffolding", summary="Add new source code scaffolding.")
    def create(self, body: schemas.NewScaffolding):
        self.service.create(**body.model_dump())

    @route.put("/{scaffolding_id}", operation_id="update_scaffolding", summary="Add new source code scaffolding.")
    def update(self, scaffolding_id: str, body: schemas.NewScaffolding):
        self.service.update_scaffolding(scaffolding_id, **body.model_dump())

    @route.get("", response=list[schemas.Scaffolding], operation_id="find_scaffoldings", summary="Find all Scaffoldings.", )
    def find_all(self):
        return self.service.find_all()

    @route.get("/{scaffolding_id}", response=schemas.Scaffolding, operation_id="get_scaffolding", summary="Get the scaffolding.")
    def get(self, scaffolding_id: str):
        return self.service.get(scaffolding_id)

    @route.post("/{scaffolding_id}/renderings", response={201: schemas.SourceCode}, operation_id="render_scaffolding", summary="Render scaffolding.")
    def render( self, scaffolding_id: str, body: schemas.GenerateSourceCode):
        pass

    @route.delete("/{scaffolding_id}/variables", response=list[schemas.Scaffolding], operation_id="find_scaffoldings", summary="Find all Scaffoldings.", )
    def delete(self, scaffolding_id: str):
        return self.service.delete_variables(scaffolding_id, )

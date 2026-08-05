from modwire_hex.django import DjangoRequest
from ninja import Status
from ninja_extra import ControllerBase, api_controller, route

from ..services import ProjectsService
from . import schemas


@api_controller("/projects", tags=["Projects"])
class ProjectsController(ControllerBase):
    @route.post("/discover", response=schemas.DiscoveredProject, operation_id="discover_project")
    def discover(self, request, body: schemas.DiscoverProject):
        return DjangoRequest.resolve(request, ProjectsService).discover_project(body.root)

    @route.get("", response=list[schemas.Project], operation_id="find_projects")
    def find_all(self, request):
        return DjangoRequest.resolve(request, ProjectsService).find_all_projects()

    @route.post("", response={201: schemas.Project}, operation_id="register_project")
    def register(self, request, body: schemas.RegisterProject):
        project = DjangoRequest.resolve(request, ProjectsService).register_project(
            body.discovery,
            body.architecture_root,
            body.boundaries_yaml,
            body.shape_yaml,
            body.scaffolding_id,
            body.record_ids,
        )
        return Status(201, project)

    @route.get("/{project_id}", response=schemas.Project, operation_id="get_project")
    def get(self, request, project_id: str):
        return DjangoRequest.resolve(request, ProjectsService).get_project(project_id)

    @route.get("/{project_id}/health", response=schemas.HealthReport, operation_id="check_project_health")
    def check_health(self, request, project_id: str):
        return DjangoRequest.resolve(request, ProjectsService).check_health(project_id)

    @route.get("/{project_id}/insights", response=schemas.InsightsReport, operation_id="read_project_insights")
    def read_insights(self, request, project_id: str):
        return DjangoRequest.resolve(request, ProjectsService).read_insights(project_id)

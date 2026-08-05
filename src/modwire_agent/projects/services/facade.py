from dataclasses import dataclass

from django.db.models import QuerySet
from wireup import injectable

from ..services.reports.adapters import ArchitectureAdapter

from ..errors import ProjectsError
from ..models import Project
from .adapters import RecordsAdapter, ScaffoldingsAdapter
from .reports import ReportsService
from .repository import ProjectRepository
from .stack import DiscoveredProject, StackDetector


@injectable
@dataclass(frozen=True)
class ProjectsService:
    architecture: ArchitectureAdapter
    records: RecordsAdapter
    scaffoldings: ScaffoldingsAdapter
    stack: StackDetector
    reports: ReportsService
    repository: ProjectRepository

    def discover_project(self, root: str) -> DiscoveredProject:
        stack = self.stack.detect(root)
        return DiscoveredProject(root=root, stack=stack)

    def find_all_projects(self) -> QuerySet[Project]:
        return self.repository.find_all()

    def get_project(self, project_id: str) -> Project:
        return self.repository.get(project_id)

    def register_project(
        self,
        discovery: DiscoveredProject,
        architecture_root: str,
        boundaries_yaml: str,
        shape_yaml: str,
        scaffolding_id: str,
        record_ids: list[str],
    ) -> Project:
        if len(record_ids) != len(set(record_ids)):
            raise ProjectsError("A project cannot bind the same record more than once.")

        self.records.check_records_existence(record_ids)
        self.scaffoldings.check_scaffolding_existence(scaffolding_id)
        self.architecture.validate_yaml_config(boundaries_yaml, shape_yaml)
        
        return self.repository.register(
            {
                "root": discovery.root,
                "architecture_root": architecture_root,
                "language_id": discovery.stack.language,
                "language_version": discovery.stack.language_version,
                "package_manager_id": discovery.stack.package_manager,
                "boundaries_yaml": boundaries_yaml,
                "shape_yaml": shape_yaml,
                "scaffolding_id": scaffolding_id,
            },
            record_ids,
        )

    def check_health(self, project_id: str):
        project = self.repository.get(project_id)
        return self.reports.generate_health_report(
            project.architecture_root,
            project.language_id,
            project.boundaries_yaml,
            project.shape_yaml,
        )

    def read_insights(self, project_id: str):
        project = self.repository.get(project_id)
        return self.reports.generate_insights_report(
            project.architecture_root,
            project.language_id,
            project.boundaries_yaml,
            project.shape_yaml,
        )

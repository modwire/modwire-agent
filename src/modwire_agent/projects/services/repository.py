from collections.abc import Iterable, Mapping
from dataclasses import dataclass, field
from typing import Any

from django.db import IntegrityError, transaction
from wireup import injectable

from ...core.models import DjangoRepository
from ..errors import ProjectsError
from ..models import Project, ProjectRecord


@injectable
@dataclass
class ProjectRepository(DjangoRepository):
    model: type[Project] = field(default=Project, init=False)

    def register(self, data: Mapping[str, Any], record_ids: Iterable[str]) -> Project:
        try:
            with transaction.atomic():
                project = self.save(**data)
                ProjectRecord.objects.bulk_create(
                    ProjectRecord(project=project, record_id=record_id) for record_id in record_ids
                )
                return project
        except IntegrityError as error:
            raise ProjectsError("A project with this root already exists.") from error

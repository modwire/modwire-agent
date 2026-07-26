from dataclasses import dataclass

from wireup import injectable

from modwire_agent.shared import SourceCodeRenderer
from ..models import Scaffolding
from .repository import ScaffoldingRepository


@injectable
@dataclass(frozen=True)
class ScaffoldingService:
    repository: ScaffoldingRepository
    renderer: SourceCodeRenderer

    def create(self, data: dict) -> Scaffolding:
        return self.repository.save(**data)

    def get(self, id: str) -> Scaffolding:
        return self.repository.get(id)

    def find_all(self):
        return self.repository.find_all()

    def update(self, id: str, data: dict) -> Scaffolding:
        return self.repository.update(id, **data)

    def delete(self, id: str) -> None:
        self.repository.delete(id)

    def render(self, id: str, parameters: dict):
        return self.renderer.render(self.get(id).source, parameters).package.files

from dataclasses import dataclass

from ..models import Scaffolding
from .repository import ScaffoldingRepository


@dataclass(frozen=True)
class ScaffoldingService:
    repository: ScaffoldingRepository

    def create(self, data: dict):
        self.repository.save(**data)

    def get(self, id: str) -> Scaffolding:
        return self.repository.get(id)

    def find_all(self) -> list[Scaffolding]:
        return self.repository.find_all()

    def update_scaffolding(self, id: str, data: dict, variables: list[dict], templates: list[dict]):
        pass

    def delete_variables(self, id: str, variable_ids: list[str]):
        pass

    def delete_templates(self, id: str, template_ids: list[str]):
        pass

    def render(self, id: str, parameters: list[str]):
        pass

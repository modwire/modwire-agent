from dataclasses import dataclass
from typing import Any

from ..ports.template_catalog import TemplateCatalog


@dataclass(frozen=True, slots=True)
class TemplateService:
    catalog: TemplateCatalog

    def get(self, identifier: str) -> Any:
        return self.catalog.get(identifier)

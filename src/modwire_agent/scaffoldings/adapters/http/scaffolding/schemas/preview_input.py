from ninja import Field
from pydantic import JsonValue

from modwire_agent.scaffoldings.adapters.http.schema import StrictSchema

from .template_override import TemplateOverrideIn


class ScaffoldingPreviewIn(StrictSchema):
    values: dict[str, JsonValue] = Field(default_factory=dict)
    template_overrides: list[TemplateOverrideIn] = Field(default_factory=list)

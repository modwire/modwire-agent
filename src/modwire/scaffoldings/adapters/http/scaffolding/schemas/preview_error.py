from typing import Literal

from ninja import Field, Schema
from pydantic import JsonValue


class PreviewErrorOut(Schema):
    code: Literal["unknown_variable", "required_variable", "invalid_variable_type", "invalid_template_override", "duplicate_template_override", "jinja_syntax", "jinja_render", "invalid_rendered_path", "rendered_path_collision", "highlighting_failed"]
    message: str
    details: dict[str, JsonValue] = Field(default_factory=dict)

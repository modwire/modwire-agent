from enum import Enum


class PreviewErrorOutCode(str, Enum):
    DUPLICATE_TEMPLATE_OVERRIDE = "duplicate_template_override"
    HIGHLIGHTING_FAILED = "highlighting_failed"
    INVALID_RENDERED_PATH = "invalid_rendered_path"
    INVALID_TEMPLATE_OVERRIDE = "invalid_template_override"
    INVALID_VARIABLE_TYPE = "invalid_variable_type"
    JINJA_RENDER = "jinja_render"
    JINJA_SYNTAX = "jinja_syntax"
    RENDERED_PATH_COLLISION = "rendered_path_collision"
    REQUIRED_VARIABLE = "required_variable"
    UNKNOWN_VARIABLE = "unknown_variable"

    def __str__(self) -> str:
        return str(self.value)

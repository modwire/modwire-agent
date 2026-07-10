from typing import Literal

from ninja import ModelSchema
from pydantic import AnyHttpUrl

from shared.api_types import ShortUUID

from ...models.tool import Tool

type ToolRole = Literal[
    "build",
    "coverage",
    "development_runner",
    "documentation",
    "formatter",
    "linter",
    "security",
    "test_runner",
    "type_checker",
]


class ToolOut(ModelSchema):
    id: ShortUUID
    language: ShortUUID
    roles: list[ToolRole]
    config_paths: list[str]
    homepage_url: AnyHttpUrl

    @staticmethod
    def resolve_language(obj):
        return obj.language_id

    class Meta:
        model = Tool
        fields = "__all__"

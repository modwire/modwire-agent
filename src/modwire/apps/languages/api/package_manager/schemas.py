from typing import Literal

from ninja import ModelSchema
from pydantic import AnyHttpUrl

from modwire.shared.api.types import ShortUUID

from ...models.package_manager import PackageManager


class PackageManagerOut(ModelSchema):
    id: ShortUUID
    language: ShortUUID
    manifest_paths: list[str]
    lockfile_paths: list[str]
    registry_url: Literal[""] | AnyHttpUrl

    @staticmethod
    def resolve_language(obj):
        return obj.language_id

    class Meta:
        model = PackageManager
        fields = "__all__"

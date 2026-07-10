from ninja import ModelSchema, Schema

from ...models.package_manager import PackageManager


class PackageManagerIn(Schema):
    language_id: str
    name: str
    executable: str


class PackageManagerPatchIn(Schema):
    language_id: str | None = None
    name: str | None = None
    executable: str | None = None


class PackageManagerOut(ModelSchema):
    class Meta:
        model = PackageManager 
        fields = "__all__"

from ninja import ModelSchema, Schema

from ...models.package_manager import PackageManager 


class PackageManagerIn(Schema):
    name: str


class PackageManagerPatchIn(Schema):
    name: str


class PackageManagerOut(ModelSchema):
    class Meta:
        model = PackageManager 
        fields = ("id", "name", "created_at", "updated_at")

from ninja import ModelSchema

from ...models.package_manager import PackageManager


class PackageManagerOut(ModelSchema):
    class Meta:
        model = PackageManager 
        fields = "__all__"

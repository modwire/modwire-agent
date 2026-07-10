from django.shortcuts import get_object_or_404
from wireup import injectable

from ..models.package_manager import PackageManager


@injectable
class PackageManagerService:
    model = PackageManager

    def list(self):
        return self.model.objects.order_by("id")

    def get(self, package_manager_id: int):
        return get_object_or_404(self.model, id=package_manager_id)

    def create(self, **data):
        return self.model.objects.create(**data)

    def update(self, package_manager_id: int, **data):
        instance = self.get(package_manager_id)
        for field, value in data.items():
            setattr(instance, field, value)
        instance.save()
        return instance

    def delete(self, package_manager_id: int):
        instance = self.get(package_manager_id)
        instance.delete()

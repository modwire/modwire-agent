from django.shortcuts import get_object_or_404
from wireup import injectable

from ..models.language import Language
from ..models.package_manager import PackageManager


@injectable
class PackageManagerService:
    model = PackageManager

    def list(self):
        return self.model.objects.select_related("language").order_by("name")

    def get(self, package_manager_id: str):
        return get_object_or_404(self.model, id=package_manager_id)

    def create(self, language_id: str, **data):
        instance = self.model(language=get_object_or_404(Language, id=language_id), **data)
        instance.full_clean()
        instance.save()
        return instance

    def update(self, package_manager_id: str, **data):
        instance = self.get(package_manager_id)
        if "language_id" in data:
            instance.language = get_object_or_404(Language, id=data.pop("language_id"))
        for field, value in data.items():
            setattr(instance, field, value)
        instance.full_clean()
        instance.save()
        return instance

    def delete(self, package_manager_id: str):
        instance = self.get(package_manager_id)
        instance.delete()

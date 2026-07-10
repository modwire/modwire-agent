from django.shortcuts import get_object_or_404
from wireup import injectable

from ..models.command import Command
from ..models.package_manager import PackageManager


@injectable
class CommandService:
    model = Command

    def list(self, package_manager_id: str):
        queryset = self.model.objects.select_related("package_manager").order_by("package_manager", "result")
        return queryset.filter(package_manager_id=package_manager_id)

    def upsert(self, *, package_manager, result: str, cmd: str):
        instance, _ = self.model.objects.update_or_create(
            package_manager=package_manager,
            result=result,
            defaults={"cmd": cmd},
        )
        return instance

    def get(self, command_id: str):
        return get_object_or_404(self.model, id=command_id)

    def create(self, package_manager_id: str, **data):
        instance = self.model(
            package_manager=get_object_or_404(PackageManager, id=package_manager_id),
            **data,
        )
        instance.full_clean()
        instance.save()
        return instance

    def update(self, command_id: str, **data):
        instance = self.get(command_id)
        if "package_manager_id" in data:
            instance.package_manager = get_object_or_404(PackageManager, id=data.pop("package_manager_id"))
        for field, value in data.items():
            setattr(instance, field, value)
        instance.full_clean()
        instance.save()
        return instance

    def delete(self, command_id: str):
        instance = self.get(command_id)
        instance.delete()

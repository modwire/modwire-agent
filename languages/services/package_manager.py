from wireup import injectable

from ..models.package_manager import PackageManager


@injectable
class PackageManagerService:
    model = PackageManager

    def list(self):
        return self.model.objects.select_related("language").order_by("name")

    def upsert(self, *, language, name: str, executable: str):
        instance, _ = self.model.objects.update_or_create(
            language=language,
            name=name,
            defaults={"executable": executable},
        )
        return instance

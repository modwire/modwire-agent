from wireup import injectable

from ..models.package_manager import PackageManager


@injectable
class PackageManagerService:
    model = PackageManager

    def list(self, language_id: str):
        queryset = self.model.objects.select_related("language").order_by("name")
        return queryset.filter(language_id=language_id)

    def upsert(self, *, language, name: str, executable: str, **conventions):
        instance, _ = self.model.objects.update_or_create(
            language=language,
            name=name,
            defaults={"executable": executable, **conventions},
        )
        return instance

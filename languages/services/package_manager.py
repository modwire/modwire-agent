from wireup import injectable

from ..models.package_manager import PackageManager


@injectable
class PackageManagerService:
    model = PackageManager

    def list(self):
        return self.model.objects.select_related("language").order_by("name")

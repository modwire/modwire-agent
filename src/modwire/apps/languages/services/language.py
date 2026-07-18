from wireup import injectable

from ..models.language import Language


@injectable
class LanguageService:
    model = Language

    def list(self):
        return self.model.objects.order_by("name")

    def upsert(self, *, name: str, executable: str, stable_version: str):
        instance, _ = self.model.objects.update_or_create(
            name=name,
            defaults={
                "executable": executable,
                "stable_version": stable_version,
            },
        )
        return instance

from wireup import injectable

from ..models.language import Language


@injectable
class LanguageService:
    model = Language

    def list(self):
        return self.model.objects.order_by("name")

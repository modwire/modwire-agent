from wireup import injectable

from ..models.tool import Tool


@injectable
class ToolService:
    model = Tool

    def list(self, language_id: str, role: str):
        queryset = self.model.objects.select_related("language").order_by("language", "name")
        queryset = queryset.filter(language_id=language_id)
        tools = list(queryset)
        return [tool for tool in tools if role in tool.roles]

    def upsert(self, *, language, name: str, **data):
        instance, _ = self.model.objects.update_or_create(
            language=language,
            name=name,
            defaults=data,
        )
        return instance

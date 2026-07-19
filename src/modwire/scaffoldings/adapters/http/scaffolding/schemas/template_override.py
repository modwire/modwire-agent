from modwire.scaffoldings.adapters.http.schema import StrictSchema


class TemplateOverrideIn(StrictSchema):
    template_id: str
    relative_path: str
    file_content: str

from wireup import injectable

from .scaffolding import ScaffoldingService


@injectable
class ScaffoldingBundleService:
    def __init__(self, scaffoldings: ScaffoldingService):
        self.scaffoldings = scaffoldings

    def get(self, scaffolding_id: str):
        scaffolding = self.scaffoldings.get(scaffolding_id)
        return {
            "id": scaffolding.id,
            "name": scaffolding.name,
            "variables": [
                {
                    "id": variable.id,
                    "name": variable.name,
                    "type": variable.type,
                    "description": variable.description,
                    "default_value": variable.default_value,
                    "required": variable.required,
                }
                for variable in scaffolding.variables.order_by("name")
            ],
            "templates": [
                {
                    "id": template.id,
                    "relative_path": template.relative_path,
                    "file_content": template.file_content,
                    "write_mode": template.write_mode,
                }
                for template in scaffolding.templates.order_by("relative_path")
            ],
        }

from .get_scaffolding import GetScaffolding


class GetScaffoldingBundle:
    def __init__(self, get_scaffolding: GetScaffolding):
        self.get_scaffolding = get_scaffolding

    def execute(self, scaffolding_id: str) -> dict:
        scaffolding = self.get_scaffolding.execute(scaffolding_id)
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

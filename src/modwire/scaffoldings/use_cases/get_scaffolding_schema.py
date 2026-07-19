from ..domain.preview import ScaffoldingPreviewPolicy
from .get_scaffolding import GetScaffolding


class GetScaffoldingSchema:
    def __init__(self, get_scaffolding: GetScaffolding, policy: ScaffoldingPreviewPolicy):
        self.get_scaffolding = get_scaffolding
        self.policy = policy

    def execute(self, scaffolding_id: str) -> dict:
        scaffolding = self.get_scaffolding.execute(scaffolding_id)
        variables = scaffolding.variables.order_by("name")
        properties = {
            variable.name: {
                "type": self.policy.json_types[variable.type],
                "description": variable.description,
                "default": variable.default_value,
            }
            for variable in variables
        }
        required = [variable.name for variable in variables if variable.required]
        return {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "type": "object",
            "properties": properties,
            "required": required,
            "additionalProperties": False,
        }

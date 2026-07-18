from wireup import injectable

from .variable_validation import VariableValidationService


@injectable
class ScaffoldingSchemaService:
    def __init__(self, validation: VariableValidationService):
        self.validation = validation

    def build(self, scaffolding) -> dict:
        properties = {}
        required = []
        for variable in scaffolding.variables.order_by("name"):
            properties[variable.name] = {
                "type": self.validation.json_types[variable.type],
                "description": variable.description,
                "default": variable.default_value,
            }
            if variable.required:
                required.append(variable.name)
        return {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "type": "object",
            "properties": properties,
            "required": required,
            "additionalProperties": False,
        }

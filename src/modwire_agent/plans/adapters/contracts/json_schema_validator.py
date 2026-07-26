from typing import Any

from jsonschema import Draft202012Validator, SchemaError, ValidationError

from ...domain.definition.invalid_plan_definition import InvalidPlanDefinition
from ...domain.run.invalid_stage_submission import InvalidStageSubmission
from ...ports.outbound import SchemaValidator


class JsonSchemaValidator(SchemaValidator):
    def require_valid_schema(self, schema: dict[str, Any]) -> None:
        try:
            Draft202012Validator.check_schema(schema)
        except SchemaError as error:
            raise InvalidPlanDefinition(str(error)) from error

    def require_valid_value(self, schema: dict[str, Any], value: dict[str, Any]) -> None:
        try:
            Draft202012Validator(schema).validate(value)
        except ValidationError as error:
            raise InvalidStageSubmission(error.message) from error

    def require_compatible_values(self, output_schema: dict[str, Any], input_schema: dict[str, Any]) -> None:
        if output_schema == input_schema:
            return
        if output_schema.get("type") != "object" or input_schema.get("type") != "object":
            raise InvalidPlanDefinition(
                "Adjacent stage contracts must use identical schemas or compatible object schemas."
            )
        output_properties = output_schema.get("properties", {})
        input_properties = input_schema.get("properties", {})
        output_required = set(output_schema.get("required", []))
        input_required = set(input_schema.get("required", []))
        if not input_required <= output_required:
            raise InvalidPlanDefinition("A stage result does not guarantee every required input of its successor.")
        if any(name not in output_properties for name in input_required):
            raise InvalidPlanDefinition("A stage result must declare every required successor input.")
        if any(
            not self._is_subschema(output_properties[name], input_properties.get(name, {})) for name in input_required
        ):
            raise InvalidPlanDefinition("A stage result property is incompatible with its successor input.")
        if any(
            not self._is_subschema(schema, input_properties[name])
            for name, schema in output_properties.items()
            if name in input_properties
        ):
            raise InvalidPlanDefinition("A stage result property is incompatible with its successor input.")
        if input_schema.get("additionalProperties") is False and not self._has_compatible_properties(
            output_schema, input_schema
        ):
            raise InvalidPlanDefinition("A stage result may contain properties forbidden by its successor.")

    def _is_subschema(self, output_schema: dict[str, Any], input_schema: dict[str, Any]) -> bool:
        if output_schema == input_schema or not input_schema:
            return True
        return set(input_schema) == {"type"} and output_schema.get("type") == input_schema["type"]

    def _has_compatible_properties(self, output_schema: dict[str, Any], input_schema: dict[str, Any]) -> bool:
        if output_schema.get("additionalProperties") is not False:
            return False
        output_properties = set(output_schema.get("properties", {}))
        input_properties = set(input_schema.get("properties", {}))
        return output_properties <= input_properties

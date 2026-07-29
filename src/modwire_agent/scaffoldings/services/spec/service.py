from collections.abc import Mapping
from dataclasses import dataclass

from pydantic import JsonValue
from wireup import injectable

from modwire_agent.shared import SourceCodePackage

from .model import PreparedScaffolding, ScaffoldingSpec


@injectable
@dataclass(frozen=True)
class ScaffoldingSpecService:
    def prepare(
        self,
        value: Mapping[str, object] | ScaffoldingSpec,
        parameters: Mapping[str, JsonValue],
    ) -> PreparedScaffolding:
        spec = self._parse(value)
        return PreparedScaffolding(
            spec=spec,
            source=self._source(spec),
            parameters=self._validate_parameters(spec, parameters),
        )

    def _parse(self, value: Mapping[str, object] | ScaffoldingSpec) -> ScaffoldingSpec:
        if isinstance(value, ScaffoldingSpec):
            return value
        return ScaffoldingSpec.model_validate(value)

    def _source(self, spec: ScaffoldingSpec) -> SourceCodePackage:
        return SourceCodePackage(
            language=spec.language,
            package={"files": {template.path: template.content for template in spec.templates}},
        )

    def _validate_parameters(
        self,
        spec: ScaffoldingSpec,
        parameters: Mapping[str, JsonValue],
    ) -> dict[str, JsonValue]:
        variables = {variable.name: variable for variable in spec.variables}
        supplied = set(parameters)
        missing = variables.keys() - supplied
        unexpected = supplied - variables.keys()

        if missing or unexpected:
            details = []
            if missing:
                details.append(f"missing: {', '.join(sorted(missing))}")
            if unexpected:
                details.append(f"unexpected: {', '.join(sorted(unexpected))}")
            raise ValueError(f"Invalid rendering parameters ({'; '.join(details)}).")

        return {
            name: variable.validate_value(parameters[name])
            for name, variable in variables.items()
        }

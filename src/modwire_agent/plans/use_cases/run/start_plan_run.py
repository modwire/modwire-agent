from dataclasses import dataclass
from typing import Any
from uuid import UUID

from ...domain.run.plan_run import PlanRun
from ...domain.run.plan_run_policy import PlanRunPolicy
from ...ports.outbound import PlanDefinitionStore, PlanRunStore, SchemaValidator


@dataclass(frozen=True, slots=True)
class StartPlanRun:
    definitions: PlanDefinitionStore
    runs: PlanRunStore
    schemas: SchemaValidator
    policy: PlanRunPolicy

    def execute(self, definition_id: UUID, initial_input: dict[str, Any]) -> PlanRun:
        definition = self.definitions.get(definition_id)
        start_stage = definition.stage(definition.start_stage_id)
        self.schemas.require_valid_value(start_stage.input_schema, initial_input)
        run = self.policy.start(definition, initial_input)
        self.runs.save(run)
        return run

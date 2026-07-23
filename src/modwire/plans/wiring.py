from modwire_hex import Module, Providers

from .adapters.artifact.django_plan_artifact_store import DjangoPlanArtifactStore
from .adapters.contracts.json_schema_validator import JsonSchemaValidator
from .adapters.definition.django_plan_definition_store import DjangoPlanDefinitionStore
from .adapters.gate.django_gate_satisfaction_store import DjangoGateSatisfactionStore
from .adapters.operation.django_operation_execution_store import DjangoOperationExecutionStore
from .adapters.operation.registered_operation_catalog import RegisteredOperationCatalog
from .adapters.run.django_plan_run_store import DjangoPlanRunStore
from .adapters.run.django_stage_transition_store import DjangoStageTransitionStore
from .domain.artifact.artifact_policy import ArtifactPolicy
from .domain.definition.artifact_definition_policy import ArtifactDefinitionPolicy
from .domain.definition.plan_definition_policy import PlanDefinitionPolicy
from .domain.gate.gate_policy import GatePolicy
from .domain.operation.operation_policy import OperationPolicy
from .domain.run.plan_run_policy import PlanRunPolicy
from .ports.artifact.plan_artifact_store import PlanArtifactStore
from .ports.contracts.schema_validator import SchemaValidator
from .ports.definition.plan_definition_store import PlanDefinitionStore
from .ports.gate.gate_satisfaction_store import GateSatisfactionStore
from .ports.operation.operation_catalog import OperationCatalog
from .ports.operation.operation_execution_store import OperationExecutionStore
from .ports.run.plan_run_store import PlanRunStore
from .ports.run.stage_transition_store import StageTransitionStore
from .use_cases.definition.publish_plan_definition import PublishPlanDefinition
from .use_cases.gate.satisfy_stage_gate import SatisfyStageGate
from .use_cases.operation.execute_stage_operation import ExecuteStageOperation
from .use_cases.run.start_plan_run import StartPlanRun
from .use_cases.run.submit_stage_result import SubmitStageResult

plans = Module.auto(
    "plans",
    roots=(PublishPlanDefinition, StartPlanRun, SubmitStageResult, SatisfyStageGate, ExecuteStageOperation),
    bindings=(
        Providers.bind(PlanDefinitionStore, DjangoPlanDefinitionStore, "scoped", None),
        Providers.bind(PlanArtifactStore, DjangoPlanArtifactStore, "scoped", None),
        Providers.bind(GateSatisfactionStore, DjangoGateSatisfactionStore, "scoped", None),
        Providers.bind(PlanRunStore, DjangoPlanRunStore, "scoped", None),
        Providers.bind(OperationExecutionStore, DjangoOperationExecutionStore, "scoped", None),
        Providers.bind(OperationCatalog, RegisteredOperationCatalog, "singleton", None),
        Providers.bind(StageTransitionStore, DjangoStageTransitionStore, "scoped", None),
        Providers.bind(SchemaValidator, JsonSchemaValidator, "singleton", None),
        Providers.singleton(ArtifactPolicy, None),
        Providers.singleton(ArtifactDefinitionPolicy, None),
        Providers.singleton(GatePolicy, None),
        Providers.singleton(PlanDefinitionPolicy, None),
        Providers.singleton(PlanRunPolicy, None),
        Providers.singleton(OperationPolicy, None),
    ),
)

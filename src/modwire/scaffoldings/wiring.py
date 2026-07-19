from modwire_hex import Module, Providers

from .use_cases.bundle import ScaffoldingBundleService
from .adapters.convergence.planner import ScaffoldingConvergencePlanner
from .adapters.convergence.service import DjangoScaffoldingConvergence
from .adapters.convergence.validator import ScaffoldingAggregateValidator
from .adapters.convergence.writer import ScaffoldingAggregateWriter
from .adapters.scaffolding.django_scaffolding_store import DjangoScaffoldingStore
from .adapters.template.django_template_store import DjangoTemplateStore
from .adapters.variable.django_variable_store import DjangoVariableStore
from .ports.scaffolding_catalog import ScaffoldingCatalog
from .ports.scaffolding_convergence import ScaffoldingConvergence
from .ports.template_catalog import TemplateCatalog
from .ports.variable_catalog import VariableCatalog
from .use_cases.converge_scaffolding import ConvergeScaffolding
from .use_cases.highlighter import SyntaxHighlightingService
from .use_cases.preview import ScaffoldingPreviewService
from .use_cases.renderer import SandboxedTemplateRenderer
from .use_cases.scaffolding import ScaffoldingService
from .use_cases.schema import ScaffoldingSchemaService
from .use_cases.template import TemplateService
from .use_cases.variable import VariableService
from .use_cases.variable_validation import VariableValidationService


scaffoldings = Module(
    "scaffoldings",
    providers=(
        Providers.service(ScaffoldingService, None),
        Providers.service(TemplateService, None),
        Providers.service(VariableService, None),
        Providers.bind(ScaffoldingCatalog, DjangoScaffoldingStore, "scoped", None),
        Providers.bind(TemplateCatalog, DjangoTemplateStore, "scoped", None),
        Providers.bind(VariableCatalog, DjangoVariableStore, "scoped", None),
        Providers.service(ScaffoldingBundleService, None),
        Providers.service(ConvergeScaffolding, None),
        Providers.bind(ScaffoldingConvergence, DjangoScaffoldingConvergence, "scoped", None),
        Providers.service(ScaffoldingConvergencePlanner, None),
        Providers.service(ScaffoldingAggregateValidator, None),
        Providers.service(ScaffoldingAggregateWriter, None),
        Providers.service(ScaffoldingPreviewService, None),
        Providers.service(ScaffoldingSchemaService, None),
        Providers.service(SyntaxHighlightingService, None),
        Providers.service(SandboxedTemplateRenderer, None),
        Providers.service(VariableValidationService, None),
    ),
)

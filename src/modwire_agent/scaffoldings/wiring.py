from modwire_hex import Module, Providers

from .adapters.convergence.planner import ScaffoldingConvergencePlanner
from .adapters.convergence.service import DjangoScaffoldingConvergence
from .adapters.convergence.validator import ScaffoldingAggregateValidator
from .adapters.convergence.writer import ScaffoldingAggregateWriter
from .adapters.preview import SandboxedTemplateRenderer, SyntaxHighlightingService
from .adapters.scaffolding.django_scaffolding_store import DjangoScaffoldingStore
from .domain.preview import ScaffoldingPreviewPolicy
from .ports.scaffolding_catalog import ScaffoldingCatalog
from .ports.scaffolding_convergence import ScaffoldingConvergence
from .use_cases.converge_scaffolding import ConvergeScaffolding
from .use_cases.get_scaffolding import GetScaffolding
from .use_cases.get_scaffolding_bundle import GetScaffoldingBundle
from .use_cases.get_scaffolding_schema import GetScaffoldingSchema
from .use_cases.preview_scaffolding import PreviewScaffolding

scaffoldings = Module(
    "scaffoldings",
    providers=(
        Providers.service(GetScaffolding, None),
        Providers.bind(ScaffoldingCatalog, DjangoScaffoldingStore, "scoped", None),
        Providers.service(GetScaffoldingBundle, None),
        Providers.service(ConvergeScaffolding, None),
        Providers.bind(ScaffoldingConvergence, DjangoScaffoldingConvergence, "scoped", None),
        Providers.service(ScaffoldingConvergencePlanner, None),
        Providers.service(ScaffoldingAggregateValidator, None),
        Providers.service(ScaffoldingAggregateWriter, None),
        Providers.service(PreviewScaffolding, None),
        Providers.service(GetScaffoldingSchema, None),
        Providers.service(ScaffoldingPreviewPolicy, None),
        Providers.service(SyntaxHighlightingService, None),
        Providers.service(SandboxedTemplateRenderer, None),
    ),
)

from modwire_hex import Module, Providers

from modwire.languages.domain.catalog import BuiltInLanguageCatalog
from modwire.languages.domain.contracts import LanguageCatalog
from modwire.languages.domain.services import LanguageCatalogService, LanguageVersionService

from .use_cases.bundle import ScaffoldingBundleService
from .use_cases.convergence.planner import ScaffoldingConvergencePlanner
from .use_cases.convergence.service import ScaffoldingConvergenceService
from .use_cases.convergence.validator import ScaffoldingAggregateValidator
from .use_cases.convergence.writer import ScaffoldingAggregateWriter
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
        Providers.bind(LanguageCatalog, BuiltInLanguageCatalog, "singleton", None),
        Providers.singleton(LanguageVersionService, None),
        Providers.service(LanguageCatalogService, None),
        Providers.service(ScaffoldingService, None),
        Providers.service(TemplateService, None),
        Providers.service(VariableService, None),
        Providers.service(ScaffoldingBundleService, None),
        Providers.service(ScaffoldingConvergenceService, None),
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

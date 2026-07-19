from modwire_hex import Module, Providers

from .adapters.version.http_version_reader import HttpVersionReader
from .domain.catalog import BuiltInLanguageCatalog
from .domain.contracts import LanguageCatalog
from .ports.version_reader import VersionReader
from .use_cases.language_catalog import LanguageCatalogService

languages = Module(
    "languages",
    providers=(
        Providers.bind(LanguageCatalog, BuiltInLanguageCatalog, "singleton", None),
        Providers.bind(VersionReader, HttpVersionReader, "singleton", None),
        Providers.service(LanguageCatalogService, None),
    ),
)

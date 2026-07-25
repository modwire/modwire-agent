from modwire_hex import Module, Providers

from .adapters.language.http_version_reader import HttpVersionReader
from .domain.catalog import BuiltInLanguageCatalog
from .domain.contracts import LanguageCatalog
from .ports.language.version_reader import VersionReader
from .use_cases.language.get_current_language_version import GetCurrentLanguageVersion
from .use_cases.language.get_language import GetLanguage
from .use_cases.language.list_languages import ListLanguages

languages = Module(
    "languages",
    providers=(
        Providers.bind(LanguageCatalog, BuiltInLanguageCatalog, "singleton", None),
        Providers.bind(VersionReader, HttpVersionReader, "singleton", None),
        Providers.service(ListLanguages, None),
        Providers.service(GetLanguage, None),
        Providers.service(GetCurrentLanguageVersion, None),
    ),
)

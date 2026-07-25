from collections.abc import Sequence

from .contracts import Language, LanguageCatalog
from .mermaid import Mermaid
from .php import PHP
from .python import Python
from .typescript import Typescript


class SharedLanguageCatalog(LanguageCatalog):
    def __init__(self, languages: Sequence[Language]):
        super().__init__(languages=tuple(sorted(languages, key=lambda language: language.name)))


BuiltInLanguageCatalog = type(
    "BuiltInLanguageCatalog",
    (SharedLanguageCatalog,),
    {"__init__": lambda self: SharedLanguageCatalog.__init__(self, (Python(), PHP(), Typescript(), Mermaid()))},
)

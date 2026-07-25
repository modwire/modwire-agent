from collections.abc import Sequence

from .contracts import Language, LanguageCatalog
from .mermaid import Mermaid
from .php import PHP
from .python import Python
from .typescript import Typescript


class SharedLanguageCatalog(LanguageCatalog):
    def __init__(self, languages: Sequence[Language]):
        super().__init__(languages=tuple(sorted(languages, key=lambda language: language.name)))


class BuiltInLanguageCatalog(SharedLanguageCatalog):
    def __init__(self):
        super().__init__((Python(), PHP(), Typescript(), Mermaid()))

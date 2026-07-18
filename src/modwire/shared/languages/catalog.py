from collections.abc import Sequence

from wireup import injectable

from .contracts import Language, LanguageCatalog


@injectable(as_type=LanguageCatalog)
class SharedLanguageCatalog(LanguageCatalog):
    def __init__(self, languages: Sequence[Language]):
        super().__init__(languages=tuple(sorted(languages, key=lambda language: language.name)))

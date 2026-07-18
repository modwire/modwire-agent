from pathlib import Path

from modwire_extraction import ModwireExtraction
from modwire_extraction.code import QueryableCodeMap
from wireup import injectable


@injectable
class QueryableCodeMapReader:
    def read(self, root: Path, language: str) -> QueryableCodeMap:
        return ModwireExtraction(root).generate_queryable_map(language)

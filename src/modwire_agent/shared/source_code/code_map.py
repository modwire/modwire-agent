from dataclasses import dataclass
from pathlib import Path

from modwire_extraction import ModwireExtraction
from modwire_extraction.code import QueryableCodeMap

from .package import SourceCodePackage


@dataclass(frozen=True)
class SourceCodeMap:
    source: SourceCodePackage
    code_map: QueryableCodeMap


class QueryableCodeMapReader:
    def read(self, root: Path, language: str) -> QueryableCodeMap:
        return ModwireExtraction(root).generate_queryable_map(language)

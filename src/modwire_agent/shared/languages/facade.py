from dataclasses import dataclass
from typing import Sequence
from .base import Language

from ..source_code import CodePackage, SourceCodePackage
from .syntax import Highlighter


@dataclass(frozen=True)
class LanguageService:
    languages: Sequence[Language]
    syntax: Highlighter

    def get(self, id: str) -> Language:
        for lang in self.languages:
            if lang.id == id:
                return lang
        raise ValueError("Language not found")

    def highlight_syntax(self, source_code_package: CodePackage) -> str:
        return 

from dataclasses import dataclass
from typing import Sequence
from .base import Language

from ..source_code import CodePackage, SourceCodePackage
from .syntax import Highlighter


@dataclass(frozen=True)
class LanguageService:
    """
    Inventory of supported languages
    """
    languages: Sequence[Language]
    syntax: Highlighter

    def highlight_syntax(self, source_code_package: SourceCodePackage) -> str:
        return  ""

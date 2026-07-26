from dataclasses import dataclass
from pathlib import Path

from ..languages import LanguageService

from .package import CodePackage
from .reader import CodePackageReader
from .writer import CodePackageWriter
from .renderer import CodePackageRenderer


@dataclass(frozen=True)
class SourceCodeService:
    reader: CodePackageReader
    writer: CodePackageWriter
    language: LanguageService
    renderer: CodePackageRenderer

    def read_package(self, root: Path) -> CodePackage:
        return self.reader.read_package(root)

    def read_language_package(self, root: Path, language: str) -> CodePackage:
        lang = self.language.get(language)
        return self.reader.read_package(root, lang.extensions)

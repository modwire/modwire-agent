from django.test import TestCase

from modwire.languages.domain.catalog import BuiltInLanguageCatalog
from modwire.languages.domain.contracts import Language
from modwire.languages.ports.version_reader import VersionReader
from modwire.languages.use_cases.language_catalog import LanguageCatalogService


class StaticVersionReader(VersionReader):
    def read(self, language: Language, timeout: float) -> str:
        return f"{language.id}-current"


class LanguageCatalogScenarios(TestCase):
    def test_resolves_a_supported_language_and_its_current_version(self) -> None:
        catalog = LanguageCatalogService(BuiltInLanguageCatalog(), StaticVersionReader())

        language = catalog.find("PYTHON")

        self.assertEqual(language.id, "python")
        self.assertEqual(catalog.find_current_version("python"), "python-current")

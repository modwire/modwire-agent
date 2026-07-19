from django.test import SimpleTestCase

from modwire.core.siren import siren_modules
from modwire.languages.adapters.siren.contract import (
    ENTITY_PATH,
    GET_OPERATION,
    LIST_OPERATION,
    RESOURCE_NAME,
)


class SirenRegistryScenarios(SimpleTestCase):
    def test_registers_the_languages_siren_resource(self) -> None:
        languages = next(module for module in siren_modules() if module.name == "languages")
        (language,) = languages.resources

        self.assertEqual(language.name, RESOURCE_NAME)
        self.assertEqual(language.path, ENTITY_PATH)
        self.assertEqual(language.collection_operations, (LIST_OPERATION,))
        self.assertEqual(language.operations, (GET_OPERATION,))
        self.assertEqual(languages.controllers[0].__name__, "LanguagesSirenController")

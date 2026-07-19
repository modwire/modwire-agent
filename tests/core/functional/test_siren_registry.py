from django.test import SimpleTestCase

from modwire.core.siren import resources
from modwire.languages.adapters.siren.contract import (
    ENTITY_PATH,
    GET_OPERATION,
    LIST_OPERATION,
    RESOURCE_NAME,
)


class SirenRegistryScenarios(SimpleTestCase):
    def test_registers_the_languages_siren_resource(self) -> None:
        language = next(resource for resource in resources.resources if resource.name == RESOURCE_NAME)

        self.assertEqual(language.name, RESOURCE_NAME)
        self.assertEqual(language.path, ENTITY_PATH)
        self.assertEqual(language.collection_operations, (LIST_OPERATION,))
        self.assertEqual(language.operations, (GET_OPERATION,))

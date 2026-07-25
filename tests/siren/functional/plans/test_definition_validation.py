from tests.plans.functional.attacks import test_definition_validation as _definition_validation

from ..helpers.test_case import SirenFunctionalTestCase


class TestSirenDefinitionValidationAttacks(SirenFunctionalTestCase, _definition_validation.DefinitionValidationAttacks):
    pass

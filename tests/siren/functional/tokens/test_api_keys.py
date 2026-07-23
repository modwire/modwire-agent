from tests.tokens.functional import test_api_keys

from ..helpers.test_case import SirenFunctionalTestCase


class TestSirenApiKeys(SirenFunctionalTestCase, test_api_keys.ApiKeyScenarios):
    pass

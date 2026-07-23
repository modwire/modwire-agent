from ..helpers.test_case import SirenFunctionalTestCase


class TestSirenApiKeys(
    SirenFunctionalTestCase,
    SirenFunctionalTestCase.load_case("tests.tokens.functional.test_api_keys", "ApiKeyScenarios"),
):
    pass

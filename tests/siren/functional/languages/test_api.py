from ..helpers.test_case import SirenFunctionalTestCase


class TestSirenLanguagesApi(
    SirenFunctionalTestCase,
    SirenFunctionalTestCase.load_case("tests.languages.functional.test_languages_api", "LanguagesApiScenarios"),
):
    pass

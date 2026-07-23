from tests.languages.functional import test_languages_api

from ..helpers.test_case import SirenFunctionalTestCase


class TestSirenLanguagesApi(SirenFunctionalTestCase, test_languages_api.LanguagesApiScenarios):
    pass

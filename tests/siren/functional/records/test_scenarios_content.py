from tests.records.functional.scenarios.test_catalogs import CatalogScenarios as _CatalogScenarios
from tests.records.functional.scenarios.test_content import ContentScenarios as _ContentScenarios
from tests.records.functional.scenarios.test_content_history import ContentHistoryScenarios as _ContentHistoryScenarios
from tests.records.functional.scenarios.test_content_kinds import ContentKindScenarios as _ContentKindScenarios

from ..helpers.test_case import SirenFunctionalTestCase


class TestSirenCatalogScenarios(SirenFunctionalTestCase, _CatalogScenarios):
    pass


class TestSirenContentScenarios(SirenFunctionalTestCase, _ContentScenarios):
    pass


class TestSirenContentHistoryScenarios(SirenFunctionalTestCase, _ContentHistoryScenarios):
    pass


class TestSirenContentKindScenarios(SirenFunctionalTestCase, _ContentKindScenarios):
    pass

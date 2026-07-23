from tests.scaffoldings.functional import test_convergence, test_preview_api

from ..helpers.test_case import SirenFunctionalTestCase


class TestSirenScaffoldingConvergence(SirenFunctionalTestCase, test_convergence.ScaffoldingConvergenceScenarios):
    pass


class TestSirenScaffoldingPreview(SirenFunctionalTestCase, test_preview_api.ScaffoldingPreviewApiTests):
    pass

from tests.core.functional import test_error_boundary

from ..helpers.test_case import SirenFunctionalTestCase


class TestSirenErrorBoundary(SirenFunctionalTestCase, test_error_boundary.ErrorBoundaryScenarios):
    pass

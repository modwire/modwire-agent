from ..helpers.test_case import SirenFunctionalTestCase


class TestSirenCors(
    SirenFunctionalTestCase,
    SirenFunctionalTestCase.load_case("tests.core.functional.test_cors", "CorsScenarios"),
):
    pass


class TestSirenErrorBoundary(
    SirenFunctionalTestCase,
    SirenFunctionalTestCase.load_case("tests.core.functional.test_error_boundary", "ErrorBoundaryScenarios"),
):
    pass

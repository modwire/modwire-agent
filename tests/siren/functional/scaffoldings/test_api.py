from ..helpers.test_case import SirenFunctionalTestCase


class TestSirenScaffoldingConvergence(
    SirenFunctionalTestCase,
    SirenFunctionalTestCase.load_case(
        "tests.scaffoldings.functional.test_convergence",
        "ScaffoldingConvergenceScenarios",
    ),
):
    pass


class TestSirenScaffoldingPreview(
    SirenFunctionalTestCase,
    SirenFunctionalTestCase.load_case("tests.scaffoldings.functional.test_preview_api", "ScaffoldingPreviewApiTests"),
):
    pass

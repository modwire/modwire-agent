from tests.scaffoldings.functional.test_convergence import (
    ScaffoldingConvergenceScenarios as _ScaffoldingConvergenceScenarios,
)

from ..helpers.test_case import SirenFunctionalTestCase


class TestSirenScaffoldingConvergence(SirenFunctionalTestCase, _ScaffoldingConvergenceScenarios):
    pass

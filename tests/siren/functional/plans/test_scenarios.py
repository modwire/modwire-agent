from ..helpers.test_case import SirenFunctionalTestCase


class TestSirenDefinitionValidationAttacks(
    SirenFunctionalTestCase,
    SirenFunctionalTestCase.load_case(
        "tests.plans.functional.attacks.test_definition_validation",
        "DefinitionValidationAttacks",
    ),
):
    pass


class TestSirenRunIntegrityAttacks(
    SirenFunctionalTestCase,
    SirenFunctionalTestCase.load_case("tests.plans.functional.attacks.test_run_integrity", "RunIntegrityAttacks"),
):
    pass


class TestSirenGateControlScenarios(
    SirenFunctionalTestCase,
    SirenFunctionalTestCase.load_case("tests.plans.functional.happy.test_gate_control", "GateControlScenarios"),
):
    pass


class TestSirenTerminalPlanScenarios(
    SirenFunctionalTestCase,
    SirenFunctionalTestCase.load_case("tests.plans.functional.happy.test_terminal_plan", "TerminalPlanScenarios"),
):
    pass


class TestSirenPlanRunScenarios(
    SirenFunctionalTestCase,
    SirenFunctionalTestCase.load_case("tests.plans.functional.test_plan_run", "PlanRunScenarios"),
):
    pass

from tests.plans.functional import test_plan_run
from tests.plans.functional.attacks import test_definition_validation, test_run_integrity
from tests.plans.functional.happy import test_gate_control, test_terminal_plan

from ..helpers.test_case import SirenFunctionalTestCase


class TestSirenDefinitionValidationAttacks(
    SirenFunctionalTestCase, test_definition_validation.DefinitionValidationAttacks
):
    pass


class TestSirenRunIntegrityAttacks(SirenFunctionalTestCase, test_run_integrity.RunIntegrityAttacks):
    pass


class TestSirenGateControlScenarios(SirenFunctionalTestCase, test_gate_control.GateControlScenarios):
    pass


class TestSirenTerminalPlanScenarios(SirenFunctionalTestCase, test_terminal_plan.TerminalPlanScenarios):
    pass


class TestSirenPlanRunScenarios(SirenFunctionalTestCase, test_plan_run.PlanRunScenarios):
    pass

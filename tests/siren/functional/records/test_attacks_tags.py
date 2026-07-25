from tests.records.functional.scenarios.attacks.test_tag_assignment import TagAssignmentAttacks as _TagAssignmentAttacks
from tests.records.functional.scenarios.attacks.test_visibility import DraftVisibilityAttacks as _DraftVisibilityAttacks

from ..helpers.test_case import SirenFunctionalTestCase


class TestSirenTagAssignmentAttacks(SirenFunctionalTestCase, _TagAssignmentAttacks):
    pass


class TestSirenDraftVisibilityAttacks(SirenFunctionalTestCase, _DraftVisibilityAttacks):
    pass

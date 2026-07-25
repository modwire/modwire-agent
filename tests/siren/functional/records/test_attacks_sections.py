from tests.records.functional.scenarios.attacks.test_routing import RouteFilteringAttacks as _RouteFilteringAttacks
from tests.records.functional.scenarios.attacks.test_section_details import (
    SectionDetailsAttacks as _SectionDetailsAttacks,
)
from tests.records.functional.scenarios.attacks.test_section_kinds import SectionKindAttacks as _SectionKindAttacks
from tests.records.functional.scenarios.attacks.test_section_placements import (
    SectionPlacementAttacks as _SectionPlacementAttacks,
)

from ..helpers.test_case import SirenFunctionalTestCase


class TestSirenRouteFilteringAttacks(SirenFunctionalTestCase, _RouteFilteringAttacks):
    pass


class TestSirenSectionDetailsAttacks(SirenFunctionalTestCase, _SectionDetailsAttacks):
    pass


class TestSirenSectionKindAttacks(SirenFunctionalTestCase, _SectionKindAttacks):
    pass


class TestSirenSectionPlacementAttacks(SirenFunctionalTestCase, _SectionPlacementAttacks):
    pass

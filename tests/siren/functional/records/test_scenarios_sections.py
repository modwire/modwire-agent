from tests.records.functional.scenarios.test_search import SearchScenarios as _SearchScenarios
from tests.records.functional.scenarios.test_section_details import SectionDetailsScenarios as _SectionDetailsScenarios
from tests.records.functional.scenarios.test_section_placements import (
    SectionPlacementScenarios as _SectionPlacementScenarios,
)
from tests.records.functional.scenarios.test_sections import SectionScenarios as _SectionScenarios

from ..helpers.test_case import SirenFunctionalTestCase


class TestSirenSearchScenarios(SirenFunctionalTestCase, _SearchScenarios):
    pass


class TestSirenSectionDetailsScenarios(SirenFunctionalTestCase, _SectionDetailsScenarios):
    pass


class TestSirenSectionPlacementScenarios(SirenFunctionalTestCase, _SectionPlacementScenarios):
    pass


class TestSirenSectionScenarios(SirenFunctionalTestCase, _SectionScenarios):
    pass

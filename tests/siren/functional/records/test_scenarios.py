from tests.records.functional.scenarios import (
    test_catalogs,
    test_content,
    test_content_history,
    test_content_kinds,
    test_content_proposals,
    test_happy,
    test_publication,
    test_record_archive,
    test_record_details,
    test_record_rename,
    test_record_tags,
    test_records,
    test_search,
    test_section_details,
    test_section_placements,
    test_sections,
    test_tags,
)
from tests.records.functional.scenarios.attacks import (
    test_actor_headers,
    test_content_proposal_details,
    test_content_schema,
    test_request_contract,
    test_routing,
    test_section_kinds,
    test_tag_assignment,
    test_visibility,
)
from tests.records.functional.scenarios.attacks import (
    test_content_proposals as content_proposal_attacks,
)
from tests.records.functional.scenarios.attacks import (
    test_record_archive as record_archive_attacks,
)
from tests.records.functional.scenarios.attacks import (
    test_record_details as record_details_attacks,
)
from tests.records.functional.scenarios.attacks import (
    test_record_rename as record_rename_attacks,
)
from tests.records.functional.scenarios.attacks import (
    test_section_details as section_details_attacks,
)
from tests.records.functional.scenarios.attacks import (
    test_section_placements as section_placement_attacks,
)

from ..helpers.test_case import SirenFunctionalTestCase


class TestSirenActorHeaderAttacks(SirenFunctionalTestCase, test_actor_headers.ActorHeaderAttacks):
    pass


class TestSirenContentProposalDetailsAttacks(
    SirenFunctionalTestCase, test_content_proposal_details.ContentProposalDetailsAttacks
):
    pass


class TestSirenContentProposalAttacks(SirenFunctionalTestCase, content_proposal_attacks.ContentProposalAttacks):
    pass


class TestSirenContentSchemaAttacks(SirenFunctionalTestCase, test_content_schema.ContentSchemaAttacks):
    pass


class TestSirenRecordArchiveAttacks(SirenFunctionalTestCase, record_archive_attacks.RecordArchiveAttacks):
    pass


class TestSirenRecordDetailsAttacks(SirenFunctionalTestCase, record_details_attacks.RecordDetailsAttacks):
    pass


class TestSirenRecordRenameAttacks(SirenFunctionalTestCase, record_rename_attacks.RecordRenameAttacks):
    pass


class TestSirenRequestContractAttacks(SirenFunctionalTestCase, test_request_contract.RequestContractAttacks):
    pass


class TestSirenRouteFilteringAttacks(SirenFunctionalTestCase, test_routing.RouteFilteringAttacks):
    pass


class TestSirenSectionDetailsAttacks(SirenFunctionalTestCase, section_details_attacks.SectionDetailsAttacks):
    pass


class TestSirenSectionKindAttacks(SirenFunctionalTestCase, test_section_kinds.SectionKindAttacks):
    pass


class TestSirenSectionPlacementAttacks(SirenFunctionalTestCase, section_placement_attacks.SectionPlacementAttacks):
    pass


class TestSirenTagAssignmentAttacks(SirenFunctionalTestCase, test_tag_assignment.TagAssignmentAttacks):
    pass


class TestSirenDraftVisibilityAttacks(SirenFunctionalTestCase, test_visibility.DraftVisibilityAttacks):
    pass


class TestSirenCatalogScenarios(SirenFunctionalTestCase, test_catalogs.CatalogScenarios):
    pass


class TestSirenContentScenarios(SirenFunctionalTestCase, test_content.ContentScenarios):
    pass


class TestSirenContentHistoryScenarios(SirenFunctionalTestCase, test_content_history.ContentHistoryScenarios):
    pass


class TestSirenContentKindScenarios(SirenFunctionalTestCase, test_content_kinds.ContentKindScenarios):
    pass


class TestSirenContentProposalScenarios(SirenFunctionalTestCase, test_content_proposals.ContentProposalScenarios):
    pass


class TestSirenHappyRecordsPath(SirenFunctionalTestCase, test_happy.HappyRecordsPath):
    pass


class TestSirenPublicationScenarios(SirenFunctionalTestCase, test_publication.PublicationScenarios):
    pass


class TestSirenRecordArchiveScenarios(SirenFunctionalTestCase, test_record_archive.RecordArchiveScenarios):
    pass


class TestSirenRecordDetailsScenarios(SirenFunctionalTestCase, test_record_details.RecordDetailsScenarios):
    pass


class TestSirenRecordRenameScenarios(SirenFunctionalTestCase, test_record_rename.RecordRenameScenarios):
    pass


class TestSirenRecordTagScenarios(SirenFunctionalTestCase, test_record_tags.RecordTagScenarios):
    pass


class TestSirenRecordScenarios(SirenFunctionalTestCase, test_records.RecordScenarios):
    pass


class TestSirenSearchScenarios(SirenFunctionalTestCase, test_search.SearchScenarios):
    pass


class TestSirenSectionDetailsScenarios(SirenFunctionalTestCase, test_section_details.SectionDetailsScenarios):
    pass


class TestSirenSectionPlacementScenarios(SirenFunctionalTestCase, test_section_placements.SectionPlacementScenarios):
    pass


class TestSirenSectionScenarios(SirenFunctionalTestCase, test_sections.SectionScenarios):
    pass


class TestSirenTagScenarios(SirenFunctionalTestCase, test_tags.TagScenarios):
    pass

from ..helpers.test_case import SirenFunctionalTestCase


class TestSirenActorHeaderAttacks(
    SirenFunctionalTestCase,
    SirenFunctionalTestCase.load_case(
        "tests.records.functional.scenarios.attacks.test_actor_headers",
        "ActorHeaderAttacks",
    ),
):
    pass


class TestSirenContentProposalDetailsAttacks(
    SirenFunctionalTestCase,
    SirenFunctionalTestCase.load_case(
        "tests.records.functional.scenarios.attacks.test_content_proposal_details",
        "ContentProposalDetailsAttacks",
    ),
):
    pass


class TestSirenContentProposalAttacks(
    SirenFunctionalTestCase,
    SirenFunctionalTestCase.load_case(
        "tests.records.functional.scenarios.attacks.test_content_proposals",
        "ContentProposalAttacks",
    ),
):
    pass


class TestSirenContentSchemaAttacks(
    SirenFunctionalTestCase,
    SirenFunctionalTestCase.load_case(
        "tests.records.functional.scenarios.attacks.test_content_schema",
        "ContentSchemaAttacks",
    ),
):
    pass


class TestSirenRecordArchiveAttacks(
    SirenFunctionalTestCase,
    SirenFunctionalTestCase.load_case(
        "tests.records.functional.scenarios.attacks.test_record_archive",
        "RecordArchiveAttacks",
    ),
):
    pass


class TestSirenRecordDetailsAttacks(
    SirenFunctionalTestCase,
    SirenFunctionalTestCase.load_case(
        "tests.records.functional.scenarios.attacks.test_record_details",
        "RecordDetailsAttacks",
    ),
):
    pass


class TestSirenRecordRenameAttacks(
    SirenFunctionalTestCase,
    SirenFunctionalTestCase.load_case(
        "tests.records.functional.scenarios.attacks.test_record_rename",
        "RecordRenameAttacks",
    ),
):
    pass


class TestSirenRequestContractAttacks(
    SirenFunctionalTestCase,
    SirenFunctionalTestCase.load_case(
        "tests.records.functional.scenarios.attacks.test_request_contract",
        "RequestContractAttacks",
    ),
):
    pass


class TestSirenRouteFilteringAttacks(
    SirenFunctionalTestCase,
    SirenFunctionalTestCase.load_case(
        "tests.records.functional.scenarios.attacks.test_routing",
        "RouteFilteringAttacks",
    ),
):
    pass


class TestSirenSectionDetailsAttacks(
    SirenFunctionalTestCase,
    SirenFunctionalTestCase.load_case(
        "tests.records.functional.scenarios.attacks.test_section_details",
        "SectionDetailsAttacks",
    ),
):
    pass


class TestSirenSectionKindAttacks(
    SirenFunctionalTestCase,
    SirenFunctionalTestCase.load_case(
        "tests.records.functional.scenarios.attacks.test_section_kinds",
        "SectionKindAttacks",
    ),
):
    pass


class TestSirenSectionPlacementAttacks(
    SirenFunctionalTestCase,
    SirenFunctionalTestCase.load_case(
        "tests.records.functional.scenarios.attacks.test_section_placements",
        "SectionPlacementAttacks",
    ),
):
    pass


class TestSirenTagAssignmentAttacks(
    SirenFunctionalTestCase,
    SirenFunctionalTestCase.load_case(
        "tests.records.functional.scenarios.attacks.test_tag_assignment",
        "TagAssignmentAttacks",
    ),
):
    pass


class TestSirenDraftVisibilityAttacks(
    SirenFunctionalTestCase,
    SirenFunctionalTestCase.load_case(
        "tests.records.functional.scenarios.attacks.test_visibility",
        "DraftVisibilityAttacks",
    ),
):
    pass


class TestSirenCatalogScenarios(
    SirenFunctionalTestCase,
    SirenFunctionalTestCase.load_case("tests.records.functional.scenarios.test_catalogs", "CatalogScenarios"),
):
    pass


class TestSirenContentScenarios(
    SirenFunctionalTestCase,
    SirenFunctionalTestCase.load_case("tests.records.functional.scenarios.test_content", "ContentScenarios"),
):
    pass


class TestSirenContentHistoryScenarios(
    SirenFunctionalTestCase,
    SirenFunctionalTestCase.load_case(
        "tests.records.functional.scenarios.test_content_history",
        "ContentHistoryScenarios",
    ),
):
    pass


class TestSirenContentKindScenarios(
    SirenFunctionalTestCase,
    SirenFunctionalTestCase.load_case("tests.records.functional.scenarios.test_content_kinds", "ContentKindScenarios"),
):
    pass


class TestSirenContentProposalScenarios(
    SirenFunctionalTestCase,
    SirenFunctionalTestCase.load_case(
        "tests.records.functional.scenarios.test_content_proposals",
        "ContentProposalScenarios",
    ),
):
    pass


class TestSirenHappyRecordsPath(
    SirenFunctionalTestCase,
    SirenFunctionalTestCase.load_case("tests.records.functional.scenarios.test_happy", "HappyRecordsPath"),
):
    pass


class TestSirenPublicationScenarios(
    SirenFunctionalTestCase,
    SirenFunctionalTestCase.load_case("tests.records.functional.scenarios.test_publication", "PublicationScenarios"),
):
    pass


class TestSirenRecordArchiveScenarios(
    SirenFunctionalTestCase,
    SirenFunctionalTestCase.load_case(
        "tests.records.functional.scenarios.test_record_archive", "RecordArchiveScenarios"
    ),
):
    pass


class TestSirenRecordDetailsScenarios(
    SirenFunctionalTestCase,
    SirenFunctionalTestCase.load_case(
        "tests.records.functional.scenarios.test_record_details", "RecordDetailsScenarios"
    ),
):
    pass


class TestSirenRecordRenameScenarios(
    SirenFunctionalTestCase,
    SirenFunctionalTestCase.load_case("tests.records.functional.scenarios.test_record_rename", "RecordRenameScenarios"),
):
    pass


class TestSirenRecordTagScenarios(
    SirenFunctionalTestCase,
    SirenFunctionalTestCase.load_case("tests.records.functional.scenarios.test_record_tags", "RecordTagScenarios"),
):
    pass


class TestSirenRecordScenarios(
    SirenFunctionalTestCase,
    SirenFunctionalTestCase.load_case("tests.records.functional.scenarios.test_records", "RecordScenarios"),
):
    pass


class TestSirenSearchScenarios(
    SirenFunctionalTestCase,
    SirenFunctionalTestCase.load_case("tests.records.functional.scenarios.test_search", "SearchScenarios"),
):
    pass


class TestSirenSectionDetailsScenarios(
    SirenFunctionalTestCase,
    SirenFunctionalTestCase.load_case(
        "tests.records.functional.scenarios.test_section_details",
        "SectionDetailsScenarios",
    ),
):
    pass


class TestSirenSectionPlacementScenarios(
    SirenFunctionalTestCase,
    SirenFunctionalTestCase.load_case(
        "tests.records.functional.scenarios.test_section_placements",
        "SectionPlacementScenarios",
    ),
):
    pass


class TestSirenSectionScenarios(
    SirenFunctionalTestCase,
    SirenFunctionalTestCase.load_case("tests.records.functional.scenarios.test_sections", "SectionScenarios"),
):
    pass


class TestSirenTagScenarios(
    SirenFunctionalTestCase,
    SirenFunctionalTestCase.load_case("tests.records.functional.scenarios.test_tags", "TagScenarios"),
):
    pass

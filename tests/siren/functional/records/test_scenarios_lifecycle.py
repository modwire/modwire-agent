from tests.records.functional.scenarios.test_content_proposals import (
    ContentProposalScenarios as _ContentProposalScenarios,
)
from tests.records.functional.scenarios.test_happy import HappyRecordsPath as _HappyRecordsPath
from tests.records.functional.scenarios.test_publication import PublicationScenarios as _PublicationScenarios
from tests.records.functional.scenarios.test_record_archive import RecordArchiveScenarios as _RecordArchiveScenarios

from ..helpers.test_case import SirenFunctionalTestCase


class TestSirenContentProposalScenarios(SirenFunctionalTestCase, _ContentProposalScenarios):
    pass


class TestSirenHappyRecordsPath(SirenFunctionalTestCase, _HappyRecordsPath):
    pass


class TestSirenPublicationScenarios(SirenFunctionalTestCase, _PublicationScenarios):
    pass


class TestSirenRecordArchiveScenarios(SirenFunctionalTestCase, _RecordArchiveScenarios):
    pass

from tests.records.functional.scenarios.test_record_details import RecordDetailsScenarios as _RecordDetailsScenarios
from tests.records.functional.scenarios.test_record_rename import RecordRenameScenarios as _RecordRenameScenarios
from tests.records.functional.scenarios.test_record_tags import RecordTagScenarios as _RecordTagScenarios
from tests.records.functional.scenarios.test_records import RecordScenarios as _RecordScenarios

from ..helpers.test_case import SirenFunctionalTestCase


class TestSirenRecordDetailsScenarios(SirenFunctionalTestCase, _RecordDetailsScenarios):
    pass


class TestSirenRecordRenameScenarios(SirenFunctionalTestCase, _RecordRenameScenarios):
    pass


class TestSirenRecordTagScenarios(SirenFunctionalTestCase, _RecordTagScenarios):
    pass


class TestSirenRecordScenarios(SirenFunctionalTestCase, _RecordScenarios):
    pass

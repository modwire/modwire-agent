from tests.records.functional.scenarios.attacks import test_record_archive as _record_archive
from tests.records.functional.scenarios.attacks import test_record_details as _record_details
from tests.records.functional.scenarios.attacks import test_record_rename as _record_rename
from tests.records.functional.scenarios.attacks import test_request_contract as _request_contract

from ..helpers.test_case import SirenFunctionalTestCase


class TestSirenRecordArchiveAttacks(SirenFunctionalTestCase, _record_archive.RecordArchiveAttacks):
    pass


class TestSirenRecordDetailsAttacks(SirenFunctionalTestCase, _record_details.RecordDetailsAttacks):
    pass


class TestSirenRecordRenameAttacks(SirenFunctionalTestCase, _record_rename.RecordRenameAttacks):
    pass


class TestSirenRequestContractAttacks(SirenFunctionalTestCase, _request_contract.RequestContractAttacks):
    pass

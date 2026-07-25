from tests.records.functional.scenarios.attacks import test_actor_headers as _actor_headers
from tests.records.functional.scenarios.attacks import test_content_proposal_details as _content_proposal_details
from tests.records.functional.scenarios.attacks import test_content_proposals as _content_proposals
from tests.records.functional.scenarios.attacks import test_content_schema as _content_schema

from ..helpers.test_case import SirenFunctionalTestCase


class TestSirenActorHeaderAttacks(SirenFunctionalTestCase, _actor_headers.ActorHeaderAttacks):
    pass


class TestSirenContentProposalDetailsAttacks(
    SirenFunctionalTestCase, _content_proposal_details.ContentProposalDetailsAttacks
):
    pass


class TestSirenContentProposalAttacks(SirenFunctionalTestCase, _content_proposals.ContentProposalAttacks):
    pass


class TestSirenContentSchemaAttacks(SirenFunctionalTestCase, _content_schema.ContentSchemaAttacks):
    pass

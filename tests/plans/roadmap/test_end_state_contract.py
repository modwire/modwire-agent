import unittest


class EndStatePlanContract(unittest.TestCase):
    @unittest.skip("MILESTONE: awaiting an owning operation handler for an end-to-end artifact contract.")
    def test_an_accepted_typed_artifact_can_be_required_by_a_later_operation(self) -> None:
        """Generic operations exchange declared artifacts without plans knowing Mermaid or architecture."""

    @unittest.skip("MILESTONE: concurrent transition testing is not implemented.")
    def test_concurrent_submissions_accept_exactly_one_transition(self) -> None:
        """A failed transition leaves neither a submission nor changed run state behind."""

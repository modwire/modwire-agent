from enum import StrEnum


class ProposalStatus(StrEnum):
    ACCEPTED = "accepted"
    PROPOSED = "proposed"
    REJECTED = "rejected"

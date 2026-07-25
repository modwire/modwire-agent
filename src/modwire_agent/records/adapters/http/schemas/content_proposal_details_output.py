from ninja import Schema


class ContentProposalDetailsOutput(Schema):
    id: str
    markdown: str
    proposed_by_id: str
    proposed_by_type: str
    status: str

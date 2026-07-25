from ninja import Schema


class SearchResultOutput(Schema):
    id: str
    title: str
    reason: str

from ninja import Schema


class RoutedRecordOutput(Schema):
    id: str
    title: str
    reason: str | None = None

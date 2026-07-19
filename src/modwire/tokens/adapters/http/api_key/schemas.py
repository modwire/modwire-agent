from datetime import datetime

from ninja import Schema

from modwire.scaffoldings.adapters.http.schema import StrictSchema


class ApiKeyIn(StrictSchema):
    name: str


class ApiKeyOut(Schema):
    id: int
    name: str
    created_at: datetime
    updated_at: datetime


class ApiKeyCreatedOut(ApiKeyOut):
    key: str

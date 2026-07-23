from datetime import datetime

from ninja import Schema

from modwire.core.schema import StrictSchema

ApiKeyIn = type("ApiKeyIn", (StrictSchema,), {"__annotations__": {"name": str}})
ApiKeyOut = type(
    "ApiKeyOut",
    (Schema,),
    {"__annotations__": {"id": int, "name": str, "created_at": datetime, "updated_at": datetime}},
)


class ApiKeyCreatedOut(ApiKeyOut):
    key: str

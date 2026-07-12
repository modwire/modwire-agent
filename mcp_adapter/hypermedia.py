from collections.abc import Callable
from contextlib import AbstractAsyncContextManager
from typing import Annotated, Literal

from modwire_siren import SirenClient, SirenTransport
from pydantic import BaseModel, ConfigDict, Field, JsonValue


class AdapterModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class RelationStep(AdapterModel):
    kind: Literal["relation"]
    relation: str = Field(min_length=1)


class ItemStep(AdapterModel):
    kind: Literal["item"]
    identifier: JsonValue
    identifier_field: str = Field(default="id", min_length=1)


NavigationStep = Annotated[RelationStep | ItemStep, Field(discriminator="kind")]


class InspectRequest(AdapterModel):
    kind: Literal["inspect"]
    path: tuple[NavigationStep, ...] = ()


class ExecuteRequest(AdapterModel):
    kind: Literal["execute"]
    path: tuple[NavigationStep, ...] = ()
    action: str = Field(min_length=1)
    values: dict[str, JsonValue] = Field(default_factory=dict)


ModwireRequest = Annotated[InspectRequest | ExecuteRequest, Field(discriminator="kind")]


class ModwireResult(AdapterModel):
    document: dict[str, JsonValue]


class ModwireHypermedia:
    def __init__(
        self,
        root_url: str,
        transport_factory: Callable[[], AbstractAsyncContextManager[SirenTransport]],
    ):
        self.root_url = root_url
        self.transport_factory = transport_factory

    async def handle(self, request: ModwireRequest) -> ModwireResult:
        async with self.transport_factory() as transport:
            client = SirenClient(self.root_url, transport)
            document = await client.root()
            for step in request.path:
                if isinstance(step, RelationStep):
                    document = await client.follow(document, step.relation)
                else:
                    document = await client.collection_item(
                        document,
                        step.identifier,
                        identifier_field=step.identifier_field,
                    )
            if isinstance(request, ExecuteRequest):
                document = await client.execute(document, request.action, request.values)
            return ModwireResult(document=document)

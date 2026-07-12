from collections.abc import Callable
from typing import Annotated, Any, Literal

import httpx
from pydantic import BaseModel, ConfigDict, Field, JsonValue

from .siren import AdapterError, SirenNavigator

ScaffoldingId = Annotated[str, Field(pattern=r"^[A-Za-z0-9_-]{22}$")]
WriteMode = Literal["managed", "create_if_missing"]


class AdapterModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class ScaffoldingSummary(AdapterModel):
    id: ScaffoldingId
    language: ScaffoldingId
    name: str
    description: str


class ScaffoldingsResult(AdapterModel):
    count: int
    scaffoldings: list[ScaffoldingSummary]


class VariableSchema(AdapterModel):
    type: Literal["string", "integer", "number", "boolean", "array", "object"]
    description: str
    default: JsonValue


class ScaffoldingSchema(AdapterModel):
    model_config = ConfigDict(extra="forbid", populate_by_name=True)

    schema_uri: Literal["https://json-schema.org/draft/2020-12/schema"] = Field(alias="$schema")
    type: Literal["object"]
    properties: dict[str, VariableSchema]
    required: list[str]
    allow_additional_properties: Literal[False] = Field(alias="additionalProperties")


class BundleVariable(AdapterModel):
    id: ScaffoldingId
    name: str
    type: Literal["str", "int", "float", "bool", "list", "dict"]
    description: str
    default_value: JsonValue
    required: bool


class BundleTemplate(AdapterModel):
    id: ScaffoldingId
    relative_path: str
    file_content: str
    write_mode: WriteMode


class ScaffoldingBundle(AdapterModel):
    id: ScaffoldingId
    name: str
    variables: list[BundleVariable]
    templates: list[BundleTemplate]


class ScaffoldingUpdate(AdapterModel):
    name: str
    description: str


class ScaffoldingCreate(ScaffoldingUpdate):
    language_id: ScaffoldingId


class TemplateCreate(AdapterModel):
    scaffolding_id: ScaffoldingId
    relative_path: str
    file_content: str
    write_mode: WriteMode = "managed"


class TemplateUpdate(AdapterModel):
    scaffolding_id: ScaffoldingId
    template_id: ScaffoldingId
    relative_path: str
    file_content: str
    write_mode: WriteMode


class UpdatedTemplate(AdapterModel):
    id: ScaffoldingId
    scaffolding: ScaffoldingId
    relative_path: str
    file_content: str
    write_mode: WriteMode


class VariableCreate(AdapterModel):
    scaffolding_id: ScaffoldingId
    name: str
    type: Literal["str", "int", "float", "bool", "list", "dict"]
    description: str
    default_value: JsonValue
    required: bool = False


class VariableUpdate(VariableCreate):
    variable_id: ScaffoldingId


class CreatedVariable(AdapterModel):
    id: ScaffoldingId
    scaffolding: ScaffoldingId
    name: str
    type: Literal["str", "int", "float", "bool", "list", "dict"]
    description: str
    default_value: JsonValue
    required: bool


class TemplateOverride(AdapterModel):
    template_id: ScaffoldingId
    relative_path: str
    file_content: str


class PreviewFile(AdapterModel):
    template_id: ScaffoldingId
    path: str
    source: str
    html: str
    language: str
    write_mode: WriteMode


class ScaffoldingPreview(AdapterModel):
    files: list[PreviewFile]


class ScaffoldingCapabilities:
    action_names = (
        "list_scaffoldings",
        "get_scaffolding_schema",
        "get_scaffolding_bundle",
        "preview_scaffolding",
        "update_scaffolding",
        "update_scaffolding_template",
    )

    def __init__(
        self,
        root_url: str,
        api_key: str,
        *,
        transport_factory: Callable[[], httpx.AsyncBaseTransport | None] | None = None,
    ):
        self.root_url = root_url
        self.api_key = api_key
        self.transport_factory = transport_factory or (lambda: None)

    async def list_scaffoldings(self) -> ScaffoldingsResult:
        async with self._navigator() as navigator:
            collection = await self._collection(navigator)
            navigator.require_action(collection, "list_scaffoldings")
            entities = collection.get("entities", [])
            if not isinstance(entities, list):
                raise AdapterError({"kind": "invalid-siren-contract", "detail": "Entities are not a list"})
            scaffoldings = [
                ScaffoldingSummary.model_validate(entity.get("properties", {}))
                for entity in entities
                if isinstance(entity, dict)
            ]
            return ScaffoldingsResult(count=len(scaffoldings), scaffoldings=scaffoldings)

    async def schema(self, scaffolding_id: ScaffoldingId) -> ScaffoldingSchema:
        document = await self._execute(scaffolding_id, "get_scaffolding_schema")
        return ScaffoldingSchema.model_validate(document.get("properties", {}))

    async def bundle(self, scaffolding_id: ScaffoldingId) -> ScaffoldingBundle:
        document = await self._execute(scaffolding_id, "get_scaffolding_bundle")
        return ScaffoldingBundle.model_validate(document.get("properties", {}))

    async def preview(
        self,
        scaffolding_id: ScaffoldingId,
        values: dict[str, JsonValue],
        template_overrides: list[TemplateOverride],
    ) -> ScaffoldingPreview:
        document = await self._execute(
            scaffolding_id,
            "preview_scaffolding",
            {
                "values": values,
                "template_overrides": [override.model_dump() for override in template_overrides],
            },
        )
        return ScaffoldingPreview.model_validate(document.get("properties", {}))

    async def update(
        self,
        scaffolding_id: ScaffoldingId,
        update: ScaffoldingUpdate,
    ) -> ScaffoldingSummary:
        async with self._navigator() as navigator:
            collection = await self._collection(navigator)
            item = await self._item(navigator, collection, scaffolding_id)
            properties = item.get("properties", {})
            if not isinstance(properties, dict) or not isinstance(properties.get("language"), str):
                raise AdapterError({"kind": "invalid-siren-contract", "detail": "Scaffolding language is missing."})
            document = await navigator.execute(
                item,
                "update_scaffolding",
                {"language_id": properties["language"], **update.model_dump()},
            )
        return ScaffoldingSummary.model_validate(document.get("properties", {}))

    async def create(self, create: ScaffoldingCreate) -> ScaffoldingSummary:
        document = await self._create("scaffoldings", "create_scaffolding", create.model_dump())
        return ScaffoldingSummary.model_validate(document.get("properties", {}))

    async def create_template(self, create: TemplateCreate) -> UpdatedTemplate:
        document = await self._create("templates", "create_template", create.model_dump())
        return UpdatedTemplate.model_validate(document.get("properties", {}))

    async def create_variable(self, create: VariableCreate) -> CreatedVariable:
        document = await self._create("variables", "create_variable", create.model_dump())
        return CreatedVariable.model_validate(document.get("properties", {}))

    async def update_template(self, update: TemplateUpdate) -> UpdatedTemplate:
        document = await self._update_owned(
            relation="templates",
            item_id=update.template_id,
            scaffolding_id=update.scaffolding_id,
            action_name="update_template",
            payload=update.model_dump(exclude={"template_id"}),
        )
        return UpdatedTemplate.model_validate(document.get("properties", {}))

    async def update_variable(self, update: VariableUpdate) -> CreatedVariable:
        document = await self._update_owned(
            relation="variables",
            item_id=update.variable_id,
            scaffolding_id=update.scaffolding_id,
            action_name="update_variable",
            payload=update.model_dump(exclude={"variable_id"}),
        )
        return CreatedVariable.model_validate(document.get("properties", {}))

    async def _update_owned(
        self,
        *,
        relation: str,
        item_id: str,
        scaffolding_id: str,
        action_name: str,
        payload: dict[str, Any],
    ) -> dict[str, Any]:
        resource = relation.removesuffix("s")
        async with self._navigator() as navigator:
            collection = await navigator.follow(await navigator.root(), relation)
            item = await self._collection_item(navigator, collection, item_id, resource)
            properties = item.get("properties", {})
            if not isinstance(properties, dict) or properties.get("scaffolding") != scaffolding_id:
                raise AdapterError(
                    {
                        "kind": f"{resource}-scaffolding-mismatch",
                        "detail": f"The {resource} does not belong to the requested scaffolding.",
                        "scaffolding_id": scaffolding_id,
                        f"{resource}_id": item_id,
                    }
                )
            return await navigator.execute(item, action_name, payload)

    async def _create(
        self,
        relation: str,
        action_name: str,
        payload: dict[str, Any],
    ) -> dict[str, Any]:
        async with self._navigator() as navigator:
            collection = await navigator.follow(await navigator.root(), relation)
            return await navigator.execute(collection, action_name, payload)

    async def advertised_capabilities(self) -> list[str]:
        async with self._navigator() as navigator:
            collection = await self._collection(navigator)
            navigator.require_action(collection, "list_scaffoldings")
            entities = collection.get("entities", [])
            if not isinstance(entities, list) or not entities:
                return ["list_scaffoldings"]
            item = await self._item(navigator, collection, self._entity_id(entities[0]))
            advertised = item.get("actions", [])
            return ["list_scaffoldings"] + [
                action_name
                for action_name in self.action_names[1:]
                if any(isinstance(action, dict) and action.get("name") == action_name for action in advertised)
            ]

    async def _execute(
        self,
        scaffolding_id: str,
        action_name: str,
        payload: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        async with self._navigator() as navigator:
            collection = await self._collection(navigator)
            item = await self._item(navigator, collection, scaffolding_id)
            return await navigator.execute(item, action_name, payload)

    async def _collection(self, navigator: SirenNavigator) -> dict[str, Any]:
        return await navigator.follow(await navigator.root(), "scaffoldings")

    async def _item(
        self,
        navigator: SirenNavigator,
        collection: dict[str, Any],
        scaffolding_id: str,
    ) -> dict[str, Any]:
        entities = collection.get("entities", [])
        if not isinstance(entities, list):
            raise AdapterError({"kind": "invalid-siren-contract", "detail": "Entities are not a list"})
        for entity in entities:
            if isinstance(entity, dict) and self._entity_id(entity) == scaffolding_id:
                return await navigator.follow(entity, "self")
        raise AdapterError(
            {
                "kind": "scaffolding-not-advertised",
                "detail": f"Scaffolding '{scaffolding_id}' is not in the advertised collection.",
                "scaffolding_id": scaffolding_id,
            }
        )

    async def _collection_item(
        self,
        navigator: SirenNavigator,
        collection: dict[str, Any],
        item_id: str,
        resource: str,
    ) -> dict[str, Any]:
        entities = collection.get("entities", [])
        if not isinstance(entities, list):
            raise AdapterError({"kind": "invalid-siren-contract", "detail": "Entities are not a list"})
        for entity in entities:
            if isinstance(entity, dict) and self._entity_id(entity) == item_id:
                return await navigator.follow(entity, "self")
        raise AdapterError(
            {
                "kind": f"{resource}-not-advertised",
                "detail": f"{resource.title()} '{item_id}' is not in the advertised collection.",
                f"{resource}_id": item_id,
            }
        )

    @staticmethod
    def _entity_id(entity: Any) -> str:
        if not isinstance(entity, dict):
            return ""
        properties = entity.get("properties", {})
        return properties.get("id", "") if isinstance(properties, dict) else ""

    def _navigator(self) -> SirenNavigator:
        return SirenNavigator(
            self.root_url,
            self.api_key,
            transport=self.transport_factory(),
        )

from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.siren_action import SirenAction
    from ..models.siren_embedded_entity_properties import SirenEmbeddedEntityProperties
    from ..models.siren_link import SirenLink


T = TypeVar("T", bound="SirenEmbeddedEntity")


@_attrs_define
class SirenEmbeddedEntity:
    """
    Attributes:
        rel (list[str]):
        class_ (list[str] | Unset):
        properties (SirenEmbeddedEntityProperties | Unset):
        entities (list[SirenEmbeddedEntity] | Unset):
        actions (list[SirenAction] | Unset):
        links (list[SirenLink] | Unset):
    """

    rel: list[str]
    class_: list[str] | Unset = UNSET
    properties: SirenEmbeddedEntityProperties | Unset = UNSET
    entities: list[SirenEmbeddedEntity] | Unset = UNSET
    actions: list[SirenAction] | Unset = UNSET
    links: list[SirenLink] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        rel = self.rel

        class_: list[str] | Unset = UNSET
        if not isinstance(self.class_, Unset):
            class_ = self.class_

        properties: dict[str, Any] | Unset = UNSET
        if not isinstance(self.properties, Unset):
            properties = self.properties.to_dict()

        entities: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.entities, Unset):
            entities = []
            for entities_item_data in self.entities:
                entities_item = entities_item_data.to_dict()
                entities.append(entities_item)

        actions: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.actions, Unset):
            actions = []
            for actions_item_data in self.actions:
                actions_item = actions_item_data.to_dict()
                actions.append(actions_item)

        links: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.links, Unset):
            links = []
            for links_item_data in self.links:
                links_item = links_item_data.to_dict()
                links.append(links_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "rel": rel,
            }
        )
        if class_ is not UNSET:
            field_dict["class"] = class_
        if properties is not UNSET:
            field_dict["properties"] = properties
        if entities is not UNSET:
            field_dict["entities"] = entities
        if actions is not UNSET:
            field_dict["actions"] = actions
        if links is not UNSET:
            field_dict["links"] = links

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.siren_action import SirenAction
        from ..models.siren_embedded_entity_properties import SirenEmbeddedEntityProperties
        from ..models.siren_link import SirenLink

        d = dict(src_dict)
        rel = cast(list[str], d.pop("rel"))

        class_ = cast(list[str], d.pop("class", UNSET))

        _properties = d.pop("properties", UNSET)
        properties: SirenEmbeddedEntityProperties | Unset
        if isinstance(_properties, Unset):
            properties = UNSET
        else:
            properties = SirenEmbeddedEntityProperties.from_dict(_properties)

        _entities = d.pop("entities", UNSET)
        entities: list[SirenEmbeddedEntity] | Unset = UNSET
        if _entities is not UNSET:
            entities = []
            for entities_item_data in _entities:
                entities_item = SirenEmbeddedEntity.from_dict(entities_item_data)

                entities.append(entities_item)

        _actions = d.pop("actions", UNSET)
        actions: list[SirenAction] | Unset = UNSET
        if _actions is not UNSET:
            actions = []
            for actions_item_data in _actions:
                actions_item = SirenAction.from_dict(actions_item_data)

                actions.append(actions_item)

        _links = d.pop("links", UNSET)
        links: list[SirenLink] | Unset = UNSET
        if _links is not UNSET:
            links = []
            for links_item_data in _links:
                links_item = SirenLink.from_dict(links_item_data)

                links.append(links_item)

        siren_embedded_entity = cls(
            rel=rel,
            class_=class_,
            properties=properties,
            entities=entities,
            actions=actions,
            links=links,
        )

        siren_embedded_entity.additional_properties = d
        return siren_embedded_entity

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties

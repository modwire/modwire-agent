from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.siren_action import SirenAction
    from ..models.siren_entity_properties import SirenEntityProperties
    from ..models.siren_link import SirenLink


T = TypeVar("T", bound="SirenEntity")


@_attrs_define
class SirenEntity:
    """
    Attributes:
        class_ (list[str]):
        links (list[SirenLink]):
        rel (list[str] | Unset):
        properties (SirenEntityProperties | Unset):
        entities (list[SirenEntity] | Unset):
        actions (list[SirenAction] | Unset):
    """

    class_: list[str]
    links: list[SirenLink]
    rel: list[str] | Unset = UNSET
    properties: SirenEntityProperties | Unset = UNSET
    entities: list[SirenEntity] | Unset = UNSET
    actions: list[SirenAction] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        class_ = self.class_

        links = []
        for links_item_data in self.links:
            links_item = links_item_data.to_dict()
            links.append(links_item)

        rel: list[str] | Unset = UNSET
        if not isinstance(self.rel, Unset):
            rel = self.rel

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

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "class": class_,
                "links": links,
            }
        )
        if rel is not UNSET:
            field_dict["rel"] = rel
        if properties is not UNSET:
            field_dict["properties"] = properties
        if entities is not UNSET:
            field_dict["entities"] = entities
        if actions is not UNSET:
            field_dict["actions"] = actions

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.siren_action import SirenAction
        from ..models.siren_entity_properties import SirenEntityProperties
        from ..models.siren_link import SirenLink

        d = dict(src_dict)
        class_ = cast(list[str], d.pop("class"))

        links = []
        _links = d.pop("links")
        for links_item_data in _links:
            links_item = SirenLink.from_dict(links_item_data)

            links.append(links_item)

        rel = cast(list[str], d.pop("rel", UNSET))

        _properties = d.pop("properties", UNSET)
        properties: SirenEntityProperties | Unset
        if isinstance(_properties, Unset):
            properties = UNSET
        else:
            properties = SirenEntityProperties.from_dict(_properties)

        _entities = d.pop("entities", UNSET)
        entities: list[SirenEntity] | Unset = UNSET
        if _entities is not UNSET:
            entities = []
            for entities_item_data in _entities:
                entities_item = SirenEntity.from_dict(entities_item_data)

                entities.append(entities_item)

        _actions = d.pop("actions", UNSET)
        actions: list[SirenAction] | Unset = UNSET
        if _actions is not UNSET:
            actions = []
            for actions_item_data in _actions:
                actions_item = SirenAction.from_dict(actions_item_data)

                actions.append(actions_item)

        siren_entity = cls(
            class_=class_,
            links=links,
            rel=rel,
            properties=properties,
            entities=entities,
            actions=actions,
        )

        siren_entity.additional_properties = d
        return siren_entity

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

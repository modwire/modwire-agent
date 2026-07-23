from typing import Any


class SirenResponse:
    """Expose Siren documents through the existing REST test assertions."""

    def __init__(self, response: Any, collection_response: bool) -> None:
        self._response = response
        self._collection_response = collection_response

    def __getitem__(self, key: str) -> str:
        return self._response[key]

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    def json(self, **kwargs: Any) -> Any:
        document = self._response.json(**kwargs)
        if "application/vnd.siren+json" not in self._response.get("Content-Type", ""):
            return document
        if document.get("class") == ["command"]:
            return document["properties"]
        if "entities" in document:
            entities = [entity["properties"] for entity in document["entities"]]
            return entities if self._collection_response else entities[0] if entities else {}
        return document.get("properties", {})

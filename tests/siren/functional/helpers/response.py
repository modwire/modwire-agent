from typing import Any


class SirenResponse:
    def __init__(self, response: Any, collection_response: bool) -> None:
        self._response = response
        self._collection_response = collection_response

    def __getitem__(self, key: str) -> str:
        return self._response[key]

    @property
    def status_code(self) -> int:
        self._require_siren_media_type()
        return self._response.status_code

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    def json(self) -> Any:
        self._require_siren_media_type()
        document = self._response.json()
        if document.get("class") == ["command"]:
            return document["properties"]
        if document.get("class") == ["error"]:
            return document["properties"]
        if "entities" in document:
            entities = [entity["properties"] for entity in document["entities"]]
            return entities if self._collection_response else entities[0] if entities else {}
        return document.get("properties", {})

    def _require_siren_media_type(self) -> None:
        content_type = self._response.get("Content-Type", "")
        if "application/vnd.siren+json" not in content_type:
            raise AssertionError(f"Expected a Siren response, received Content-Type: {content_type!r}")

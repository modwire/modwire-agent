import json
from urllib.request import Request, urlopen

from ...domain.contracts import Language
from ...ports.outbound import VersionReader


class HttpVersionReader(VersionReader):
    def read(self, language: Language, timeout: float) -> str:
        request = Request(
            language.version_provider.url,
            headers={"Accept": "application/json", "User-Agent": "modwire-languages-cms/1.0"},
        )
        try:
            with urlopen(request, timeout=timeout) as response:
                value = self._extract(json.load(response), language)
        except (OSError, ValueError, IndexError, KeyError, TypeError) as error:
            raise RuntimeError(f"Could not obtain the current {language.name} version: {error}") from error
        if not isinstance(value, str) or not value:
            raise RuntimeError(f"The version provider returned an invalid current {language.name} version.")
        return value

    @staticmethod
    def _extract(data: object, language: Language) -> object:
        value = data
        for item in language.version_provider.result_path:
            value = value[item]
        return value

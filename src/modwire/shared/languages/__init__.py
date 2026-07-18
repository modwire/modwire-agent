from .mermaid import Mermaid
from .php import PHP
from .python import Python
from .typescript import Typescript

LANGUAGE_DEFINITIONS = (Python(), Typescript(), PHP(), Mermaid())


def language_definition(value: str):
    normalized = value.strip().lower()
    for definition in LANGUAGE_DEFINITIONS:
        if normalized in {definition.name.lower(), definition.executable.lower()}:
            return definition
    raise ValueError(f"Unsupported language: {value}")


__all__ = [
    "PHP",
    "Mermaid",
    "Python",
    "Typescript",
    "language_definition",
]

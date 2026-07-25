from typing import TypedDict


class ChangeSet(TypedDict):
    create: list[str]
    update: list[str]
    delete: list[str]

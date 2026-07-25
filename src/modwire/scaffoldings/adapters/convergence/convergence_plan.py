from typing import Literal, TypedDict

from .change_set import ChangeSet


class ConvergencePlan(TypedDict):
    scaffolding: Literal["create", "update", "unchanged"]
    variables: ChangeSet
    templates: ChangeSet

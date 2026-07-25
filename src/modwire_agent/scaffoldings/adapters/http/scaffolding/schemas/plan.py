from typing import Literal

from ninja import Schema

from .changes import ConvergenceChangesOut


class ConvergencePlanOut(Schema):
    scaffolding: Literal["create", "update", "unchanged"]
    variables: ConvergenceChangesOut
    templates: ConvergenceChangesOut

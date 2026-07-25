from ninja import Schema

from .plan import ConvergencePlanOut

type NullableIdentifier = str | None


class ScaffoldingConvergenceOut(Schema):
    id: NullableIdentifier
    name: str
    dry_run: bool
    changed: bool
    plan: ConvergencePlanOut

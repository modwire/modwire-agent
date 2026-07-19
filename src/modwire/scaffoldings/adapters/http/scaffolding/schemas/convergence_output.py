from ninja import Schema

from .plan import ConvergencePlanOut


class ScaffoldingConvergenceOut(Schema):
    id: str | None
    name: str
    dry_run: bool
    changed: bool
    plan: ConvergencePlanOut

from ninja import Schema


class ConvergenceChangesOut(Schema):
    create: list[str]
    update: list[str]
    delete: list[str]

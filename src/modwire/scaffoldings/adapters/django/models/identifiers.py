from uuid import uuid4


def short_uuid() -> str:
    return uuid4().hex[:22]

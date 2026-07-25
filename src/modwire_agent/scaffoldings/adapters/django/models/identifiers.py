from uuid import uuid4


class ShortUuid:
    def __call__(self) -> str:
        return uuid4().hex[:22]


short_uuid = ShortUuid()

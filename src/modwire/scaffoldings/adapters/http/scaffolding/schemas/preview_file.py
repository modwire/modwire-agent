from typing import Literal

from ninja import Schema


class PreviewFileOut(Schema):
    template_id: str
    path: str
    source: str
    html: str
    language: str
    write_mode: Literal["managed", "create_if_missing"]

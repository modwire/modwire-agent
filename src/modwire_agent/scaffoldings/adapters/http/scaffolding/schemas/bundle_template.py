from typing import Literal

from ninja import Schema


class ScaffoldingBundleTemplateOut(Schema):
    id: str
    relative_path: str
    file_content: str
    write_mode: Literal["managed", "create_if_missing"]

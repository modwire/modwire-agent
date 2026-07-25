from typing import TypedDict


class TemplateSpec(TypedDict):
    relative_path: str
    file_content: str
    write_mode: str

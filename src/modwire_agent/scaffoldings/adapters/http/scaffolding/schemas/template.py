from typing import Literal

from modwire_agent.scaffoldings.adapters.http.schema import StrictSchema


class ScaffoldingConvergenceTemplateIn(StrictSchema):
    relative_path: str
    file_content: str
    write_mode: Literal["managed", "create_if_missing"] = "managed"

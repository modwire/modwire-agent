from pydantic import Field
from typing import Literal

from shared.code import CopierArchive


class DjangoApiProject(CopierArchive):
    project_name: str = Field(
        default="new_project",
        description="Python distribution name.",
    )

    project_package: str = Field(
        default="core",
        description="Importable Django project package.",
    )

    project_title: str = Field(
        default="New Project",
        description="API title.",
    )

    package_manager: Literal["uv", "poetry", "pdm"] = Field(
        default="uv",
        description="Package manager used by generated jobs.",
    )

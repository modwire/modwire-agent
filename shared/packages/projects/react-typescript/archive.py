from typing import Literal

from pydantic import Field

from shared.code import CopierArchive


class ReactTypescriptProject(CopierArchive):
    project_name: str = Field(default="react-app", description="Application and npm package name.")
    project_title: str = Field(default="React App", description="Human-readable application title.")
    package_manager: Literal["npm", "pnpm", "yarn"] = Field(
        default="npm",
        description="Package manager used in the generated README.",
    )

from pydantic import BaseModel


class DetectedStack(BaseModel):
    language: str
    language_version: str
    package_manager: str


class DiscoveredProject(BaseModel):
    root: str
    stack: DetectedStack

from ninja import Schema
from pydantic import JsonValue

from ..services.stack import DiscoveredProject


class DiscoverProject(Schema):
    root: str


class RegisterProject(Schema):
    discovery: DiscoveredProject
    architecture_root: str
    boundaries_yaml: str
    shape_yaml: str
    scaffolding_id: str
    record_ids: list[str]


class Project(Schema):
    id: str
    root: str
    architecture_root: str
    language_id: str
    language_version: str
    package_manager_id: str
    boundaries_yaml: str
    shape_yaml: str
    scaffolding_id: str


class HealthReport(Schema):
    healthy: bool
    reports: tuple[dict[str, JsonValue], ...]


class InsightsReport(Schema):
    reports: tuple[dict[str, JsonValue], ...]

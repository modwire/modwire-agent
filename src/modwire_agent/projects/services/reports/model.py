from pydantic import BaseModel, JsonValue


class HealthReport(BaseModel):
    healthy: bool
    reports: tuple[dict[str, JsonValue], ...]


class InsightsReport(BaseModel):
    reports: tuple[dict[str, JsonValue], ...]

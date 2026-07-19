from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True, slots=True)
class ApiKey:
    identifier: int | None
    name: str
    prefix: str
    secret_hash: str
    is_active: bool
    created_at: datetime | None
    updated_at: datetime | None
    last_used_at: datetime | None

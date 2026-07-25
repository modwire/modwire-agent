from dataclasses import dataclass
from datetime import datetime

type Nullable[T] = T | None


@dataclass(frozen=True, slots=True)
class ApiKey:
    identifier: Nullable[int]
    name: str
    prefix: str
    secret_hash: str
    is_active: bool
    created_at: Nullable[datetime]
    updated_at: Nullable[datetime]
    last_used_at: Nullable[datetime]

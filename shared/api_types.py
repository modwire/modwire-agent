from typing import Annotated

from pydantic import StringConstraints

type ShortUUID = Annotated[
    str,
    StringConstraints(min_length=22, max_length=22, pattern=r"^[A-Za-z0-9_-]{22}$"),
]
type Slug = Annotated[
    str,
    StringConstraints(min_length=1, max_length=80, pattern=r"^[a-z0-9]+(?:-[a-z0-9]+)*$"),
]
type RecordSlug = Annotated[
    str,
    StringConstraints(min_length=3, max_length=180, pattern=r"^[a-z0-9]+(?:-[a-z0-9]+)*/[a-z0-9]+(?:-[a-z0-9]+)*$"),
]

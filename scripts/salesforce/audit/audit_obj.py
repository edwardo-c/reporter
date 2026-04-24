from dataclasses import dataclass
from utils.validators import normalize_path
from data_toolkit.readers.sources import SFQuery, OData
from pathlib import Path


@dataclass(frozen=True, slots=True)
class AuditObj:
    sources: list[SFQuery | OData]
    sql: Path | str
    artifacts: dict[str, str]

    def __post_init__(self):
        object.__setattr__(self, "sql", normalize_path(self.sql))



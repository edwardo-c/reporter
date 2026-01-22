from dataclasses import dataclass, field

@dataclass(frozen=True)
class TableRef():
    sheet: str
    table: str

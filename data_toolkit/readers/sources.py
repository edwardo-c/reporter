from dataclasses import dataclass, field
from pathlib import Path
from utils.validators import validate_path
from enum import Enum

class Sources(Enum):
    BUNDLE="xl_bundle"

# ======== used for reading multiple tables in one sheet ==========
@dataclass(frozen=True)
class XLBundlePart:
    sheet_name: str
    header: int
    part_id: str

@dataclass(frozen=True)
class XLBundle:
    path: Path | str
    parts: list[XLBundlePart]
    src_type: str = field(default="xl_bundle", init=False)

    def __post_init__(self):
        
        if isinstance(self.path, str):
            object.__setattr__(self, "path", Path(self.path))

        validate_path(self.path)


# ======== NOT READER YET Reading a single frame from a single file ==========

@dataclass(frozen=True)
class XLBase:
    path: Path | str
    header: int

    def __post_init__(self):
        
        if isinstance(self.path, str):
            self.path = Path(self.path)
        
        validate_path(self.path)

@dataclass(frozen=True)
class CSV(XLBase):
    pass

@dataclass(frozen=True)
class XL(XLBase):
    sheet_name: str
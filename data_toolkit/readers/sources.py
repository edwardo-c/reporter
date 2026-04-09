from dataclasses import dataclass, field
from pathlib import Path
from utils.validators import normalize_path
from enum import Enum

class DispatchEnum(Enum):
    BUNDLE="xl_bundle"
    SF="salesforce"
    CSV="csv"
    ODATA="odata"


def normalize_df_id(df_id: str) -> str:
    return df_id.replace(" ", "_")

@dataclass(frozen=True)
class XLBundlePart():
    """Reading multiple sheets in one file"""
    sheet_name: str
    header: int
    df_id: str

    def __post_init__(self):
            object.__setattr__(self, "df_id", self.df_id.replace(" ", "_"))

@dataclass(frozen=True)
class XLBundle:
    path: Path | str
    parts: list[XLBundlePart]
    src_type: str = field(default=DispatchEnum.BUNDLE.value, init=False)

    def __post_init__(self):                
            object.__setattr__(self, "path", normalize_path(self.path))

@dataclass(frozen=True)
class CSV:
    path: Path | str
    header: int
    df_id: str
    src_type: str = field(default=DispatchEnum.CSV.value, init=False)
    
    def __post_init__(self):
            object.__setattr__(self, "path", normalize_path(self.path))
            object.__setattr__(self, "df_id", normalize_df_id(self.df_id))

@dataclass(frozen=True)
class SFQuery:
    soql: str
    df_id: str
    src_type: str = field(default=DispatchEnum.SF.value, init=False)

@dataclass(frozen=True)
class OData:
    params: dict | None
    url: str
    df_id: str
    src_type: str = field(default=DispatchEnum.ODATA.value, init=False)

    def normalize_params(self) -> dict[str, str]:
        p = self.params or {}
        p.setdefault("$format", "json")
        return p

    def __post_init__(self):
        object.__setattr__(self, "params", self.normalize_params())
        object.__setattr__(self, "df_id", normalize_df_id(self.df_id))

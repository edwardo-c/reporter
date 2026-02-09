from dataclasses import dataclass, field
import duckdb
from pathlib import Path
import pandas as pd
from typing import Mapping, Any


"""
Issues post code review:
1. Frame is holding data to load a data frame but also changes over time (stateful)
   because of .df, also .df should be .load() or .get_df() if there is caching involved

2. responsibilities between FramesCache and Frame are blurred.
   seperate these so you have a dataclass that holds the params required to load

   make a loader that can load based off inputs from Frame

   Do you even need a cache once loaded?
   
"""

@dataclass
class CsvFrame:
    ...

@dataclass
class ExcelFrame:
    ...

def validate_csv_frame():
    ...

def validate_excel_frame():
    ...

VALIDATOR_REGISTRY = {
    ".csv"  : validate_csv_frame,
    ".xlsm" : validate_excel_frame,
    ".xlsx" : validate_excel_frame
}

def read_frame():
    ...

def register_frame():
    ...

def create_frame_objects():
    ...

def register_frames():
    ...

""" what do you want your surface to look like?

entry goal: register_frames(conn, cfg)

in order to do this...
loop through config
check what type of frame it should be (csv, excel, not implemented)
validate params in post init for each type? leaning towards yes since it belongs to that type

"""

@dataclass
class Frame:
    kind: str
    path: Path
    sheet: str
    register_as: str
    header: int
    data: None = field(default=None, repr=False)
    _reader: None = field(default=None, repr=False)

    def __post_init__(self):

        ext = self.path.suffix.lower()
        if ext == ".csv":
            self._reader = pd.read_csv
        elif ext in (".xlsx", ".xlsm"):
            self._reader = pd.read_excel   
    
    def df(self):
        if self.data is None:
            self.data = self._reader(
                str(self.path),
                sheet_name = self.sheet,
                header=self.header
            )   
        return self.data

@dataclass
class FramesCache():
    cache: tuple[Frame, ...]

    @classmethod
    def from_mapping(
        cls,
        raw_cfg: Mapping[str, Mapping[str, str | Path | int | None]]
    ):
        
        cache = []

        for _, c in raw_cfg.items():

            """
            decided not to abstract null and/or type checking,
            to allow for adjustments if needed
            e.g: default sheet or header to 0
            """
            if "kind" not in c:    
                raise ValueError(f"'kind' key not provided")
            else:
                kind = c["kind"]
                if not isinstance(kind, str):
                    raise ValueError(f"'kind' must be a string object")
                elif (len(kind) == 0):
                    raise ValueError(f"'kind' cannot be a blank string")

            if "path" not in c:
                raise ValueError(f"'path' key not provided")
            else:
                path = c["path"] 
                if not isinstance(path, (Path, str)):
                    raise ValueError(f"'path' must be a Path or string object")
                elif isinstance(path, str):
                    path = Path(path)
                
                if not path.exists():
                    raise FileNotFoundError(f"path not found, {path}")

            if "sheet" not in c:
                """
                decided not to default to index 0 for missing sheet; 
                intentionally requiring an explicit config
                """
                raise ValueError(f"'sheet' key not provided")
            else:
                sheet = c["sheet"]
                if not isinstance(sheet, str):
                    raise ValueError(f"'header' must be type str, got {type(sheet)}")
                else:
                    if len(sheet) == 0:
                        raise ValueError(f"'sheet' cannot be blank string")
                
            if "header" not in c:
                """
                - base 0 because pandas is used for reading
                
                - decided not to default to index 0 for missing header; 
                  intentionally requiring an explicit config
                """
                raise ValueError(f"'header' key not provided")
            else:
                header = c["header"]
                if not isinstance(header, int):
                    raise ValueError(f"'header' must be type int, got {type(header)}")

            if "register_as" not in c:
                raise ValueError(f"'register_as' key not provided")
            else:
                register_as = c["register_as"]
                if not isinstance(register_as, str):
                    raise ValueError(f"'register_as' must be type str, got {type(register_as)}")
                else:
                    if len(register_as) == 0:
                        raise ValueError(f"'register_as' cannot be blank string")
        
            cache.append(
                Frame(
                    kind=kind,
                    path=path,
                    sheet=sheet,
                    header=header,
                    register_as=register_as
                )
            )

        return cls(tuple(cache))



def _register_frames(
        conn: duckdb.DuckDBPyConnection,
        cfg: dict[str, dict[str, str, int]],
    ) -> FramesCache:

    frames_cache = FramesCache.from_mapping(cfg)

    for frame in frames_cache.cache:

        conn.register(frame.register_as, frame.df())
    
    return frames_cache
    
    
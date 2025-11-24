import pandas as pd

from pathlib import Path

from typing import Callable

class StandardAdapter:
    def __init__(self):
        pass

    def _reader(sfx: str) -> Callable | None:
        
        if sfx == ".csv":
            return pd.read_csv
        elif sfx == ".xlsx":
            return pd.read_excel
        else:
            return None
    
    @classmethod
    def df(cls, file_path: Path | str, cfg: dict | None = None):

        if isinstance(file_path, str) and Path(file_path).is_file():
            file_path = Path(file_path)

        reader = cls._reader(file_path.suffix.casefold())

        if cfg is not None:
            sheet_name = cfg.get("sheet_name", 0)
            header = cfg.get("header", 0)
            return reader(str(file_path), sheet_name=sheet_name, header=header)
        else:
            return reader(str(file_path))
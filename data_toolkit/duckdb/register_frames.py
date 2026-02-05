from dataclasses import dataclass, field
import duckdb
from pathlib import Path
import pandas as pd

@dataclass
class SourceConfig:
    kind: str
    path: str
    sheet: str
    register_as: str
    header: int = 0
    ext: str = field(default="")

    def __post_init__(self):
        test_path = Path(self.path)

        assert test_path.exists() and test_path.is_file(), (
            f"invalid path {self.path} for {self.register_as}"
        )

        if not self.ext:
            self.ext = test_path.suffix


def register_frames(
        conn: duckdb.DuckDBPyConnection,
        cfg: dict[str, dict[str, str, int]],
    ) -> list[str]:
    
    registered = []

    for _, src_params in cfg.items():
        
        src_cfg = SourceConfig(**src_params)
        
        if src_cfg.ext == "csv":
            df = pd.read_csv(
                src_cfg.path, 
                header=src_cfg.header
            )
        elif (src_cfg.ext == ".xlsx") or (src_cfg.ext == "xlsm"):
            df = pd.read_excel(
                src_cfg.path, 
                header=src_cfg.header, 
                sheet_name=src_cfg.sheet
            )
        else:
            raise NotImplementedError(
                f"unable to read {src_cfg.path}, invalid extension"
            )

        conn.register(src_cfg.register_as, df)

        registered.append(src_cfg.register_as)
    
    return registered
    
    
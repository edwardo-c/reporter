"""Reads and stacks multiple tables from a single file"""
import pandas as pd
from pathlib import Path
from contextlib import contextmanager
import shutil
import tempfile

def read_data(cfg: dict):
    """Iterate over params in cfg, read from same file"""    
    frames = []
    with _local_copy(Path(cfg.get("file_path"))) as safe_path:
        for p in cfg.get("params"):
            df = pd.read_excel(
                    io=str(safe_path), 
                    sheet_name=p["sheet_name"],
                    header=p["header"],
                    usecols=p["usecols"]
            )
            renamed = _column_renamer(df, p["rename_map"])
            frames.append(renamed)
    
    return pd.concat(frames)

def _column_renamer(df: pd.DataFrame, rename_map: dict):
    """return dataframe with renamed column"""
    copy = df.copy()
    copy = copy.rename(columns=rename_map)
    return copy

@contextmanager
def _local_copy(file_path: Path):
    """set up and tear down of temporary directory with local copy"""
    try:
        temp_dir = Path(tempfile.mkdtemp())
        dst = temp_dir / file_path.name
        shutil.copy2(file_path, dst)
        yield dst
    finally:
        shutil.rmtree(temp_dir)
    
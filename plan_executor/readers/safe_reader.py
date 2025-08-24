from pathlib import Path
import shutil as sh
import tempfile
from typing import TypedDict, NotRequired
from typing import Callable

import pandas as pd

from utils.validators import valid_path

READERS_REGISTRY = {}

class PathCFG(TypedDict):
    """
    src_path (str | pathlib.Path): Required, file to be read via pandas

    Not Required: 

    header (int): header row of table

    sheet_name (str): sheet name in file to read, case sensative

    use_cols (list): List of column names to use in return frame    
    """

    src_path: str | Path
    header: NotRequired[int]
    sheet_name: NotRequired[str]
    use_cols: NotRequired[list]
    dtype: NotRequired[list]

def register_reader(name):
    def inner_wrapper(func):
        READERS_REGISTRY[name] = func
        return func
    return inner_wrapper

@register_reader(".xlsx")
def _read_excel(file_path: Path, cfg: PathCFG) -> pd.DataFrame:
    header = cfg.get('header', 0)
    sheet_name = cfg.get('sheet_name', 0)
    use_cols = cfg.get('use_cols', None)
    dtype = cfg.get('dtype', None)
    return pd.read_excel(file_path, header=header, sheet_name=sheet_name, usecols=use_cols, dtype=dtype)

@register_reader(".csv")
def _read_csv(file_path: str) -> pd.DataFrame:
    return pd.read_csv(file_path)

def get_func(sfx) -> Callable:
    func = READERS_REGISTRY.get(sfx, None)
    if not func:
        raise NameError(f"reader for {func} does not exist in registry")
    return func

def read_safely(cfg: PathCFG) -> pd.DataFrame:
    """Validate source path, copy to local temp folder, return dataframe"""
    _valid_config(cfg)
    src_path = valid_path(cfg['src_path'])
    safe_path: Path = _copy_safe_path(src_path)
    sfx = safe_path.suffix
    reader_func = get_func(sfx)
    try:
        return reader_func(safe_path, cfg)
    except:
        raise KeyError(f"Unable to read dataframe, check cfg: {cfg}")
    finally:
        sh.rmtree(safe_path.parent)

def _valid_config(cfg: PathCFG):
    try:
        src_path = cfg['src_path']
    except KeyError:
        raise KeyError(f"_valid_config: src_path required, recieved None")

def _copy_safe_path(src_path: Path) -> Path | None:
    """Copies file to a safe directory, returns entire path to file"""
    try:
        dst_dir: Path = Path(tempfile.mkdtemp())
        dst_path = dst_dir / src_path.name
        sh.copy2(src_path, dst_path)
        return dst_path
    except:
        sh.rmtree(dst_dir)
        return None

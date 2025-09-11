"""
Copies a csv to a local temp dir, reads from temp, deletes temp after
Only works for csvs.
"""

from pathlib import Path
import shutil as sh
import tempfile

import pandas as pd

from utils.validators import valid_path

def _read_csv(file_path: str) -> pd.DataFrame:
    return pd.read_csv(file_path)

def read_safely(file_path: Path) -> pd.DataFrame:
    """Validate source path, copy to local temp folder, return dataframe"""
    src_path = valid_path(file_path)
    safe_path: Path = _copy_safe_path(src_path)
    try:
        return _read_csv(safe_path)
    except:
        raise KeyError(f"Unable to read dataframe from: {file_path}")
    finally:
        sh.rmtree(safe_path.parent)

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

def read_xlsx_safely(path, sheet_name=0, header=0, usecols=None) -> pd.DataFrame:
    """Validate source path, copy to local temp folder, return dataframe"""
    src_path = valid_path(path)
    safe_path = _copy_safe_path(src_path)
    read_path = str(safe_path.resolve())
    try:
        return pd.read_excel(read_path, sheet_name=sheet_name, header=header, usecols=usecols)
    except:
        raise KeyError(f"Unable to read dataframe from: {path}")
    finally:
        sh.rmtree(safe_path.parent)

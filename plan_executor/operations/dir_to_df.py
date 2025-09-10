"""
reads all csv files from a directory to a single dataframe
notes*: 'safely' = copy to local file, read from copy
configuration of column names not yet implemented
"""

# Standard library imports
from pathlib import Path

# Third party imports
import pandas as pd

# Internal application imports
from plan_executor.registry import register_operation
from plan_executor.operations.safe_reader import read_safely

def _collect_files(
        directory: Path,
        suffixes: tuple[str, ...] = ('.csv', '.xlsx'),
        recursive: bool = False        
    ) -> list[Path]:
    """
    Capture all valid file paths from a directory
    args:
      directory: The directory to read file paths from
      recursive (bool) capture all files in subdirectories
      suffixes: suffix of file to be captured in return list
    """

    if not directory.is_file() and not directory.exists():
        raise NotADirectoryError(f"not a directory: {directory}")

    files: list[Path] = []
    for sfx in suffixes:
        pattern = '**/*' if recursive else '*'
        files.extend(directory.glob(f"{pattern}{sfx}"))
    files = sorted(p for p in files if p.is_file())
    if not files:
        raise ValueError(f"no {suffixes} files found in {directory}, recursive={recursive}")
    return files

def _concat_with_safe_reader(file_paths: list[Path], add_source: bool = True) -> pd.DataFrame:
    """
    concat all files safely* from a list
    """
    frames: list[pd.DataFrame] = []
    for p in file_paths:
        df = read_safely(p)
        if add_source:
            df = df.copy()
            df["__source_file"] = p.name
        frames.append(df)
    return pd.concat(frames, ignore_index=True, sort=False) if frames else pd.DataFrame()

@register_operation('dir_to_df')
def dir_to_df(cfg: dict):
    """
    Read configuration and orchestrate safe reading and concat
    cfg:
      directory: str|Path (required)
      recursive: bool = False
      suffixes: list[str] = ['.csv',] # currently only accepts csvs
      add_source_col: bool = True
    """

    directory = Path(cfg['directory'])
    recursive = bool(cfg.get('recursive', False))
    suffixes = tuple(cfg.get('suffixes', [".csv"]))
    add_source = bool(cfg.get('add_source', True))

    files = _collect_files(directory=directory, suffixes=suffixes, recursive=recursive)
    return _concat_with_safe_reader(files, add_source)
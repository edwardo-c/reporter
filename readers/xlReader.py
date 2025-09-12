from contextlib import contextmanager
from pathlib import Path
import shutil, tempfile
import pandas as pd
import win32com.client as win32
from typing import Callable
from functools import partial

# hidden lifecycle: copy to temp, auto-cleanup
@contextmanager
def safe_local_copy(src: Path, is_dir: bool = False):
    td = tempfile.TemporaryDirectory(prefix="safe_")
    try:
        if is_dir:
            dst = Path(td.name) / 'sub'
            shutil.copytree(src, dst)
        else:
            dst = Path(td.name) / Path(src).name
            shutil.copy2(src, dst)
        yield dst
    finally:
        td.cleanup()

# hidden lifecycle: Excel COM convert, auto-quit
@contextmanager
def convert_to_xlsx(local_path: Path, excel: object = None):
    wb = None
    try:
        # Unblock the temp file before Excel touches it
        import subprocess
        subprocess.run(
            ["powershell", "-NoProfile", "-Command", f'Unblock-File -Path "{str(local_path)}"'],
            check=False
        )

        wb = excel.Workbooks.Open(str(local_path))  # or CorruptLoad=1 if you use it
        xlsx_path = local_path.with_suffix(".xlsx")
        wb.SaveAs(Filename=str(xlsx_path), FileFormat=51)
        yield xlsx_path
    finally:
        if wb:
            wb.Close(SaveChanges=False)

# hidden lifecycle: Excel app
@contextmanager
def excel_app_init():
    """initialize excel app, performance boost for batches"""
    app = win32.gencache.EnsureDispatch("Excel.Application")
    app.DisplayAlerts = False
    app.Visible = False
    app.AutomationSecurity = 3 # force disable macros
    try:
        yield app
    finally:
        app.Quit()

# D) your force reader FUNCTION (passable to read_safely)
def force_reader(local_path: Path, *, app: object | None = None, **cfg) -> pd.DataFrame:
    """attempt to read file, if unable convert to temp xlsx and attempt again"""
    sfx = local_path.suffix.lower()

    if sfx == ".csv":
        return pd.read_csv(local_path, **cfg)

    def _read_xlsx(p: Path) -> pd.DataFrame:
        return pd.read_excel(p, **cfg)

    def _convert_and_read(p: Path) -> pd.DataFrame:
        if app is not None:
            with convert_to_xlsx(p, app) as xlsx_path:
                return _read_xlsx(xlsx_path)
        else:
            # create app for conversion
            with excel_app_init() as temp_app:
                with convert_to_xlsx(p, temp_app) as xlsx_path:
                    return _read_xlsx(xlsx_path)
    
    if sfx == ".xlsx":
        try:
            return _read_xlsx(local_path)
        except Exception:
            return _convert_and_read(local_path)

    # other extensions -> convert then read
    return _convert_and_read(local_path)

def _path_validator(src: Path | str) -> dict:
    """checks if path is valid file or dir, returns dict"""
    # is it a string?        
    if not isinstance(src, (str, Path)):
        raise TypeError(f"_path_validator: expected str|Path, received: {type(src)}")
    
    # is it a valid file path?
    if isinstance(src, str):
        try:
            src = Path(src)
        except Exception as e:
            raise ValueError(f"_path_validator: invalid file path, {src}")

    # does the file exist?
    if not src.exists():
        raise FileNotFoundError(f"_path_validator: {src} does not exist")
   
    if src.is_dir():
        return {'dir': src}
    else:
        return {'file': src}


def _collect_files(dir: Path, pattern: str, recursive: bool = False) -> list[Path]:
    return sorted(dir.rglob(pattern) if recursive else dir.glob(pattern))

def _dir_reader(src, pattern, recursive, reader, **cfg):
    """read files in a directory matching pattern"""
    with excel_app_init() as app:
        with safe_local_copy(src, is_dir=True) as local:
            rd = partial(reader, app=app, **cfg)
            frames = [rd(local_path=f) for f in _collect_files(local, pattern, recursive)]
    return frames

def _cfg_validator():
    ...

# Public api call, converts to local path and manages clean up
def read_safely(
        src: Path,
        recursive: bool = False,
        reader: Callable = force_reader,
        pattern: str = '*',
        stack: bool = True,
        **cfg
    ) -> pd.DataFrame:
    """
    reads file or files in dir matching pattern
    accepts all pandas args in **cfg
    TODO: wire pandas args
    args:
      stack: if stack and src is dir, stack dataframes
      pattern: glob pattern for dir reading
      reader: 

    ---TODO: Goal:
    1. read from a directory and stack (price lists)
        input: dir, stack = True
    2. read from a directory recursively, rename columns then stack (pos)
        input: dir, recursive = True, cfg for each, global rename map 
    3. read multiple sheets from a single worksheet (
        incentive comp / sar detail PQ interface ws
        )

    """

    validated = _path_validator(src)
    (path_type, src), = validated.items()
    
    if cfg: 
        raise NotImplementedError()

    if path_type == "file":
        raise NotImplementedError()

    if path_type == "dir":
        return _dir_reader(src=src, 
                           pattern=pattern, 
                           recursive=recursive, 
                           reader=reader) 

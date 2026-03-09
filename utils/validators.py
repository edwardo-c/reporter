from pathlib import Path
from typing import Mapping, Any

def validate_dir(directory: str | Path ) -> None:
    
    if not isinstance(directory, (str, Path)):
        raise TypeError(f"Expected str or Path, received {type(directory)}")

    if isinstance(directory, str):
        try:
            directory = Path(directory)
        except:
            raise NotADirectoryError(f"{directory} is not a valid path")

    if not directory.exists() and directory.is_dir():
        raise NotADirectoryError(f"{directory} is not a valid directory")

def validate_path(file_path: str | Path) -> None:
    
    if not isinstance(file_path, (str, Path)):
        raise TypeError(f"expected Path or str, got: {type(file_path)}")
    
    if isinstance(file_path, str):
        if len(file_path) == 0:
            raise ValueError(f"path cannot be an empty string")
        else:
            file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(f"path does not exist, {file_path}")

def validate_str(s: str, allow_zero: bool = False) -> None:
    if not isinstance(s, str):
        raise TypeError(f"expected type str, got {type(s)}")
    elif not allow_zero:
        if len(s) == 0:
            raise ValueError(
                f"cannot be 0 length str"
                "bypass: set allow_zero = True"
            )

def validate_positive_int(val: int) -> None:
    if not isinstance(val, int):
        raise ValueError(f"must be integer, got {type(val)}")
    elif val < 0:
        raise ValueError(f"must be a positive integer")
    
def validate_key_existence(keys: str | list[str], cfg: Mapping[Any, Any]) -> None:
    if isinstance(keys, str):
        keys = [keys]

    for k in keys:
        if k not in cfg:
            raise KeyError(
                f"key '{k}' not found in cfg"
            )

def validate_list_str(
        list_to_validate: list[str], 
        allow_zero: bool = False
    ):
    if not isinstance(list_to_validate, list):
        raise ValueError(f"Execpted type list, got {type(list_to_validate)}")
    
    for s in list_to_validate:
        validate_str(s, allow_zero=allow_zero)


def cols_in_df(cols: str | list[str], existing_cols: tuple[str]) -> None:

    if isinstance(cols, str):
        cols = [cols]

    missing = [c for c in cols if c not in existing_cols]
    if missing:
        raise ValueError(f"df is missing columns: {missing}")
    
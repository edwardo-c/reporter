from pathlib import Path
from typing import Mapping, Any

def verify_key_existance(key_name: str, raw_cfg):
    if key_name not in raw_cfg:
        raise ValueError(f"{key_name} not found in config")

def get_kind(raw_cfg, kind_registry):
    """
    checks for kind key in raw_cfg. 
    that key must also exist in the registry provided
    
    example: 
    REGISTRY = {"csv": CsvFrame, "xlsm" : ExcelFrame} 
    cfg = {"kind": "csv"} 
    """
    

def get_path(cfg) -> Path | None:

    verify_key_existance("path", cfg)
    path = cfg["path"]

    if isinstance(path, str):
        
        if len(path) == 0:
            raise ValueError(f"path is an empty string, did dotenv load?")
        else:
            path = Path(path)

    elif not isinstance(path, Path):
        raise ValueError(f"path must be Path or str type")

    if not path.exists():
        raise FileNotFoundError(f"path does not exist, {path}")

    return path

def get_sheet(cfg) -> str:
    
    verify_key_existance("sheet", cfg)
    sheet = cfg["sheet"]

    if not isinstance(sheet, str):
        raise ValueError(f"sheet must be a string, got {type(sheet)}")
    elif len(sheet) == 0:
        raise ValueError(f"sheet cannot be a 0 length string")

    return sheet

def get_header(cfg) -> int:

    verify_key_existance("header", cfg)
    header = cfg["header"]

    if not isinstance(header, int):
        raise ValueError(f"header must be integer, got {type(header)}")
    elif header < 0:
        raise ValueError(f"header must be a positive integer, got {type(header)}")

    return header


def get_register_as(cfg) -> str:
    """
    clean "register_as" key

    add double quotes if it start with a number, 
    allow only non_alpha, numeric, underscore, and double quote characters
    """
    import re

    verify_key_existance("register_as", cfg)
    raw_register_as = cfg["register_as"]

    if not isinstance(raw_register_as, str):
        raise ValueError(f"register as must be str, got {type(register_as)}")
    elif len(raw_register_as) == 0:
        raise ValueError(f"register as cannot be 0 length string")

    pattern = r"[^a-zA-Z0-9_\"]"

    register_as = re.sub(pattern, "_", raw_register_as.strip())
    
    if register_as[0].isdecimal():
        register_as = "\"" + register_as + "\""

    if register_as != raw_register_as:
        # TODO: log the change!
        pass

    return register_as


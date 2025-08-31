# pass in cfg for file, read each separetly, option to convert into single df

from pathlib import Path

import pandas as pd

from plan_executor.registry import register_operation
from utils.validators import valid_path
from plan_executor.operations.safe_reader import read_xlsx_safely


@register_operation("xlsx_reader")
def read_xlsx(file_cfgs: list[dict] | dict | str) -> pd.DataFrame | list[dict[str, pd.DataFrame]]:
    """
    Safely read network xlsx files with pandas.read_excel arguements
    for single str, or missing config options, pandas defaults are used
    'path' is required for single config
    'path' and 'alias' required for multiple configs
    
    cfg options:    
        [{
          "sheet_name": "my_sheet", 
          "header": 0, 
          "usecols": ['col_a', 'col_b'], 
          "rename_map": {"col_a: "COL_A", "col_b": "COL_B"}
        }]
    Return:
        - single str returns dataframe, 
        - single cfg(dict) returns dataframe
        - list of cfgs returns {alias: df,}
    """
    # normalize file config
    file_cfgs = _config_normalizer(file_cfgs)

    return orchestrator(file_cfgs) 

def orchestrator(file_cfgs: dict):
    """captures return dataframes with aliases and renamed columns"""

    # single str or single config
    if len(file_cfgs) == 1:
        cfg: dict = file_cfgs[0]
        if not isinstance(cfg, dict):
            raise ValueError(f"expected dict, recieved {type(cfg)}")

        alias = cfg.get("alias", "dummy")
        path = cfg["path"]
        if not valid_path(path):
            raise TypeError(f"{path} is invalid path")

        return {
            "alias" : alias,
            "data": read_xlsx_safely(path=path)
        }

   # multiple configs passed, return alias: df structure
    result = []
    for cfg in file_cfgs:
        alias = cfg.get("alias")
        path = cfg.get("path")
        if not alias:
            raise KeyError(f"alias required for multiple data frames")
        temp = {"alias": alias, "data": _read_xlsx_cfg(cfg)}

        result.append(temp)

    return result


def _read_xlsx_cfg(cfg: dict[str, Path | str | int | list]) -> pd.DataFrame:
    """safely reads data frame using config"""
    
    
    path = cfg.get("path")
    sheet_name = cfg.get("sheet_name", 0)
    header = cfg.get("header", 0)
    usecols = cfg.get("usecols", None)
    rename_map = cfg.get("rename_map", None)

    df = read_xlsx_safely(path=path, sheet_name=sheet_name, header=header, usecols=usecols)
    
    return _column_rename(df, rename_map)

def _column_rename(df: pd.DataFrame, rename_map: dict = None) -> pd.DataFrame:
    if rename_map:
        # TODO: ensure all columns in rename map exist


        return df.rename(columns=rename_map)
    
    # return unchanged df if no rename map
    return df

def _config_normalizer(file_cfgs: list[dict]) -> list[dict[str, Path | str | int | list]]:
    """confirms only valid arguements are passed in"""
    
    n = __name__
    expected_args = ("alias", "path", "sheet_name", "header", "usecols", "rename_map")

    # check proper data types
    if not isinstance(file_cfgs, (list, dict, str, Path)):
        raise TypeError(f"{n}: invalid cfg type, recieved {type(file_cfgs)}")
    
    if isinstance(file_cfgs, (str, Path)):
        return [{'path': file_cfgs}]

    # convert to list if single cfg was inputed
    if isinstance(file_cfgs, dict):
        file_cfgs = [file_cfgs]

    alias_required: bool = True if len(file_cfgs) > 1 else False

    # check for valid arguements in cfg
    for cfg in file_cfgs:

        recieved_args = tuple(cfg.keys())
        
        invalid_args = [r for r in recieved_args if r not in expected_args]
        
        if invalid_args:
            raise ValueError(f"{n}: recieved unexpeted arguements {invalid_args}")

        if alias_required and not cfg.get("alias"):
            raise ValueError(f"{n}: attempting to read multiple files, aliases required per dataframe")    

        # check for valid path, fill dict with path object
        p = valid_path(cfg.get('path'))

        if not p.suffix in (".xlsx", "xlsm"):
            raise (ValueError(f"{n}: invalid file type, recieved {p.suffix}"))
        
        cfg["path"] = p

    # return normalized cfg
    return file_cfgs

# pass in cfg for file, read each separetly, option to convert into single df

from pathlib import Path

import pandas as pd

from plan_executor.registry import register_operation
from utils.validators import valid_path


def _config_normalizer(file_cfgs: list[dict]) -> list[dict[str, Path | str | int]]:
    """confirms only valid arguements are passed in"""
    
    n = __name__
    expected_args = ("path", "sheet_name", "header", "use_cols")

    # check proper data types
    if not isinstance(file_cfgs, (list, dict, str)):
        raise TypeError(f"{n}: invalid cfg type, recieved {type(file_cfgs)}")
    
    # convert to list if single cfg was inputed
    if isinstance(file_cfgs, dict):
        file_cfgs = [file_cfgs]
    elif isinstance(file_cfgs, str):
        file_cfgs = [{'path': file_cfgs}]

    # check for valid arguements in cfg
    for cfg in file_cfgs:

        recieved_args = tuple(cfg.keys())
        
        invalid_args = [r for r in recieved_args if r not in expected_args]
        
        if invalid_args:
            raise ValueError(f"{n}: recieved unexpeted arguements {invalid_args}")

        # check for valid path, fill dict with path object
        cfg['path'] = valid_path(cfg.get('path'))
    
    # return normalized cfg
    return file_cfgs

@register_operation
def read_xlsx(file_cfgs: list[dict] | dict | str):
    """
    Safely read network xlsx files with pandas.read_excel arguements
    """

    # normalize file config
    file_cfgs = _config_normalizer(file_cfgs)

    # 
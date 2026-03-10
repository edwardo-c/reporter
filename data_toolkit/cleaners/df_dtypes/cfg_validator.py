from typing import Callable
from dataclasses import dataclass

from utils.validators import (
    cols_in_df, 
    validate_str, 
    validate_list_str, 
    validate_key_existence
)

def _normalize_keys_in_cfg(raw_cfg: dict) -> dict:
    result = {}
    
    for k, v in raw_cfg.items():
        norm_k = k.strip().lower()

        validate_str(norm_k)
        if norm_k in result:
            raise ValueError(
                f"duplicate key ({k}) in raw_cfg! , each key must be unique"
            )
        result[norm_k] = v

    return result

@dataclass(frozen=True)
class DateSection:
    format: str
    columns: list[str]

def _validate_date_cfg(date_cfg: list[dict], existing_columns: tuple[str, ...]) -> list[dict]:
        """
        expected shape: 
            date_cfg = {
                'int':   ['int_col_1', 'int_col_2'],
                'str':   ['str_col_1', 'str_col_2'],
                'date':  [{'format': '%Y-%m-%d', 'columns': ['date_col_a', 'date_col_b']}]
            }
        """

        if not isinstance(date_cfg, list):
            raise TypeError(
                f"invalid date_cfg data type, expected list, got: {type(date_cfg).__name__}"
            )

        result = []

        for sub in date_cfg:
            norm_cfg = _validate_date_sub_cfg(sub, existing_columns)
            result.append(norm_cfg)
        
        return result

def _validate_date_sub_cfg(date_sub_cfg: dict, existing_columns: tuple[str, ...]):
        if not isinstance(date_sub_cfg, dict):
            raise ValueError(f"expected dict for date sub config, got: {type(date_sub_cfg).__name__}")
        else:
            validate_key_existence('format', date_sub_cfg)
            validate_key_existence('columns', date_sub_cfg)
            cols_in_df(date_sub_cfg['columns'], existing_columns)
  
        return DateSection(**date_sub_cfg)


@dataclass(frozen=True)
class SimpleSection:
    columns: list[str]

def _validate_simple_cfg(raw_cfg: dict, existing_columns: tuple[str, ...]):
        validate_list_str(raw_cfg)
        cols_in_df(raw_cfg, existing_columns)
        return SimpleSection(raw_cfg)


VALID_CFG_REGISTRY = {
    'int': _validate_simple_cfg,
    'str': _validate_simple_cfg,
    'date': _validate_date_cfg
}

def get_valid_cfg_func(key: str) -> Callable:
    if key not in VALID_CFG_REGISTRY:
        raise KeyError(f"invalid key provided, must be 'int', 'str', or 'date', got: {key}")
    else:
        return VALID_CFG_REGISTRY[key]

@dataclass(frozen=True)
class DtypeCfg:
    int: SimpleSection
    str: SimpleSection
    date: DateSection

def walk_cfg(raw_cfg: dict, existing_cols: tuple[str, ...]) -> DtypeCfg:
    
    result_cfg = {}
    cfg = _normalize_keys_in_cfg(raw_cfg)

    for k, v in cfg.items():

        validate_cfg_func = get_valid_cfg_func(k)
        
        valid_cfg = validate_cfg_func(v, existing_cols)
            
        result_cfg[k] = valid_cfg

    return DtypeCfg(**result_cfg)

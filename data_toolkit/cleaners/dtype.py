"""pass in dataframe, specify columns and types get a cleaned dataframe to spec"""
"""
{
    int:   [int_col_1, int_col_2]
    str:   [str_col_1, str_col_2]
    date:  [
        {format: '...', columns=[date_col_a, date_col_b]}, 
        {...},
    ]
}
"""

import pandas as pd

from utils.validators import (
    cols_in_df, 
    validate_str, 
    validate_list_str, 
    validate_key_existence
)

def _normalize_key(key: str) -> str:
    validate_str(key)
    return key.strip().lower()

def _normalize_keys_in_cfg(raw_cfg):
    return {_normalize_key(k): v for k, v in raw_cfg.items()}

def _validate_date_cfg(date_cfg):
    if not isinstance(date_cfg, list):
        ...

def _validate_date_sub_cfg(date_sub_cfg):
        if not isinstance(date_sub_cfg, dict):
            # TODO: make this better
            raise ValueError(f"invalid type")
        else:
            norm_cfg = _normalize_keys_in_cfg(v)
            # is it a dictionary?
            # do the expected keys exist?
            # do the mentioned columns exist?
            # add the cleaned dict back to the clean_date_cfg
        ...

def walk_cfg(raw_cfg, existing_cols: tuple[str, ...]):
    
    normalized_cfg = {}
    
    for k, v in raw_cfg.items():

        norm_key = _normalize_key(k)
        validate_str(k, allow_zero=False)

        if norm_key in ('int', 'str'):
            validate_list_str(v)
            cols_in_df(v, existing_cols)
            normalized_cfg[norm_key] = v

        elif norm_key == 'date':
            clean_date_cfg = []
            for cfg in v:
                

    return normalized_cfg



# DtypeCleaner.clean(df, cfg)
def clean(cls, df: pd.DataFrame, raw_cfg) -> pd.DataFrame:
    cfg = cls._clean_raw_cfg(raw_cfg)

    ...




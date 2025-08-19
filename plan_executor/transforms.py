import logging
from typing import TypedDict, NotRequired

import pandas as pd

from plan_executor.registry import register_transform

logging.basicConfig(level=logging.WARNING)

def raise_err_required(func, attribute: str):
    raise KeyError(f"")

@register_transform("groupby")
def groupby(df: pd.DataFrame, cfg: dict):
    by = cfg['by']
    if not by:
        raise KeyError(f"groupby: 'by' is required, none was given")
    
    sort = cfg.get('sort', False)
    dropna = cfg.get('dropna', True)

    df_copy = df.copy(deep=True)

    return df_copy.groupby(by=by, sort=sort, dropna=dropna)


class FilterConfig(TypedDict):
    col: str
    val: str
    case_insensative: NotRequired[bool]

@register_transform("filter_in")
def filter_in(df: pd.DataFrame, cfg: FilterConfig):
    
    temp_df: pd.DataFrame = df.copy()
    col = cfg['col']
    if not col:
        raise_err_required(__name__, 'col')
    
    val = cfg['val']
    if not val:
        logging.warning(f"expected val, none was given, result not filtered")

    case_insensative: bool = cfg.get('case_insensative', True)
    temp_series: pd.Series = temp_df[col]

    if case_insensative:
        mask: pd.Series = temp_series.str.lower() == val.lower()
    else:
        mask: pd.Series = temp_df[col] == val

    return temp_df[mask]
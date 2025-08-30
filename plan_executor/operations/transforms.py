import logging
from typing import TypedDict, NotRequired

import pandas as pd

from plan_executor.registry import register_operation

logging.basicConfig(level=logging.WARNING)

def raise_err_required(func, attribute: str):
    raise KeyError(f"{func} {attribute} is required, none was given")

@register_operation("groupby")
def groupby(df: pd.DataFrame, cfg: dict):
    by = cfg['by']
    if not by:
        raise KeyError(f"groupby: 'by' is required, none was given")
    
    sort = cfg.get('sort', False)
    dropna = cfg.get('dropna', False)

    df_copy = df.copy(deep=True)

    return df_copy.groupby(by=by, sort=sort, dropna=dropna)


class FilterConfig(TypedDict):
    col: str
    val: str
    filter_in: NotRequired[bool]
    case_insensitive: NotRequired[bool]

@register_operation("filter")
def filter_in(
    df: pd.DataFrame,
    *,
    col: str,
    val: str | None = None,
    filter_in: bool = True,
    case_insensitive: bool = True
) -> pd.DataFrame:
    # (1) validate
    if col not in df.columns:
        raise KeyError(f"Missing column: {col}")
    if val is None:
        return df  # or warn+return

    # (2) normalize
    s = df[col].astype("string")
    left  = s.str.strip()
    right = str(val).strip()

    if case_insensitive:
        left = left.str.casefold()
        right = right.casefold()

    # (3) mask
    mask = (left == right) if filter_in else (left != right)
    return df[mask]

@register_operation("filter_list")
def filter_list(df: pd.DataFrame, values : list, col: str):
    
    # if not list
    if not isinstance(values, list):
        raise TypeError(f"expected type list, recieved {type(values)}")

    # if col not in df
    if col not in df.columns:
        raise KeyError(f"filter_list: column {col} not in df")

    result = df[~df[col].isin(values)]
    
    return result

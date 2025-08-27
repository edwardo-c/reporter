

import pandas as pd

from plan_executor.registry import register_operation

@register_operation("drop_null_dups")
def drop_null_dups(df: pd.DataFrame, null_col: str = None, keep_null: bool = False, subset: list | str = None):
    """
    drops duplicates where column is null
    option to keep or drop nulls

    cfg["null_col"] (str) = column where nulls are found
    cfg["keep_null"] (bool)
    cfg["subset"] (list), if single str, place in list
    """

    if null_col is None:
        raise ValueError("['null_col'] is required.")

    if not subset:
        raise ValueError("['subset'] is required.")
    if isinstance(subset, str):
        subset = [subset]

    na_position = 'first' if keep_null else 'last'
    
    # validate columns
    missing = [c for c in [null_col, *subset] if c not in df.columns]
    if missing:
        raise KeyError(f"Columns not found in DataFrame: {missing}")

    return (
        df.sort_values(by=null_col, na_position=na_position)
        .drop_duplicates(subset=subset, keep="first")
        .reset_index(drop=True)
    )
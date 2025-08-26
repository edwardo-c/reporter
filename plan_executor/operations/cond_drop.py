

import pandas as pd

from plan_executor.registry import register_operation

@register_operation("drop_dup")
def drop_null_dups(df: pd.DataFrame, cfg: dict):
    """
    drops duplicates where column is null
    option to keep or drop nulls

    cfg["null_col"] (str) = column where nulls are found
    cfg["keep_null"] (bool)
    cfg["subset"] (list), if single str, place in list
    """

    null_col = cfg.get("null_col")
    if null_col is None:
        raise ValueError("cfg['null_col'] is required.")

    subset = cfg.get("subset")
    if subset is None:
        raise ValueError("cfg['subset'] is required.")
    if isinstance(subset, str):
        subset = [subset]

    keep_null = bool(cfg.get("keep_null", False))
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
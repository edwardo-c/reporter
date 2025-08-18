
import pandas as pd

from plan_executor.registry import register_transform

@register_transform("groupby")
def groupby(df: pd.DataFrame, cfg: dict):
    by = cfg['by']
    if not by:
        raise KeyError(f"groupby: 'by' is required, none was given")
    
    sort = cfg.get('sort', False)
    dropna = cfg.get('dropna', True)

    df_copy = df.copy(deep=True)

    return df_copy.groupby(by=by, sort=sort, dropna=dropna)
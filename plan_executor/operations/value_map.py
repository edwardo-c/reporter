import pandas as pd
from plan_executor.registry import register_operation

@register_operation("value_map")
def replace_values(df: pd.DataFrame, value_map: dict, *, case_insensitive: bool = True) -> pd.DataFrame:
    """
    fill each "col_name" (key) with value_map (value)
    """
    if not isinstance(value_map, dict):
        raise TypeError(
            f"{__name__}: expected type dict, received {type(value_map)}"
        )
    
    # check for missing columns
    missing = set(value_map) - set(df.columns)
    
    # raise to avoid silent errors in will happen downstream
    if missing:
        raise KeyError(f"{__name__} missing columns {missing}")

    out: pd.DataFrame = df.copy()
    cols = list(value_map)

    # quick exit for exact matches
    if not case_insensitive:
        out[cols] = out[cols].replace(value_map)
        return out

    ci_map = {
        col: {str(k).casefold(): v for k, v in col_map.items()}
        for col, col_map in value_map.items()
    }

    for col in cols:
        
        # the column to change
        base = out[col]
        
        # the shadow values to be matched against
        s = base.astype('string').str.strip().str.casefold()
        
        # match the values
        repl = s.map(ci_map[col])

        # fill values not matched
        base = repl.fillna(base)

        out[col] = base
    
    return out
import pandas as pd
from plan_executor.registry import register_operation

@register_operation("value_map")
def replace_values(df: pd.DataFrame, value_map: dict, case_insensitive: bool = True) -> pd.DataFrame:
    """
    fill each "col_name" (key) with value_map (value)
    """
    if not isinstance(value_map, dict):
        raise TypeError(
            f"{__name__}: expected type dict, received {type(value_map)}"
        )
    
    # check for missing columns
    missing = [col for col in value_map.keys() if col not in df.columns]
    # if even one is missing, raise because silent errors will happen downstream
    if missing:
        raise KeyError(f"{__name__} missing columns {missing}")

    df_copy: pd.DataFrame = df.copy()

    if case_insensitive:
        value_map = _lower_map(value_map)
        df_copy = _lower_df(df, value_map)

    for col, map in value_map.items():
        df_copy[col] = df_copy[col].replace(map)

    return df_copy

def _lower_df(df: pd.DataFrame, value_map: dict[str, dict]):
    """
    convert column values to lower case
    """
    for col in value_map.keys():
        df[col] = df[col].str.lower()
    
    return df

def _lower_map(replace_values_map: dict[str, dict]):
    return {
    col: {str(k).lower(): v for k, v in rename_map.items()} 
    for col, rename_map in replace_values_map.items()
    }

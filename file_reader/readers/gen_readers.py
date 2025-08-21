import pandas as pd

from file_reader.registry import register_reader

@register_reader(".xlsx")
def _read_excel(file_path, sheet_name=0, header=0, usecols=None, dtype= None) -> pd.DataFrame:
    return pd.read_excel(file_path, sheet_name=sheet_name, header=header, usecols=usecols, dtype=dtype)

@register_reader(".csv")
def _read_csv(file_path: str) -> pd.DataFrame:
    return pd.read_csv(file_path)
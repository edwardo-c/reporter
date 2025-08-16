from file_reader.registry import register
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO)

def _read_excel(file_path, sheet_name=0, header=0, usecols=None, dtype= None) -> pd.DataFrame:
    return pd.read_excel(file_path, sheet_name=sheet_name, header=header, usecols=usecols, dtype=dtype)

def _read_csv(file_path: str) -> pd.DataFrame:
    return pd.read_csv(file_path)

register('.xlsx', _read_excel)
register('.csv', _read_csv)
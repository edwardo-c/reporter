"""Refresh of direct sales in duckdb"""

# Third Party Imports
import pandas as pd

from data_toolkit.readers.single_file import read_data
from data_toolkit.duckdb.duck_query import create_or_replace

def refresh_data(*, data_cfg: dict, conn: object):
    """Read, clean, and load sales data from network file to duckdb"""

    raw_sales = read_data(cfg=data_cfg)
    cleaned = _clean_data(raw_sales)
    create_or_replace(table_name="category_sales", df=cleaned, conn=conn)

def _clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """consolidate and normalize data"""
    out = (
        df
        # clean/add columns
        .assign(
            year=lambda d: d["invoice_date"].dt.year,
            part_category=lambda d: d["part_category"].str.upper()
        )
        # drop rows with null part_category
        .dropna(subset=["part_category"])
    )
    return out
    
"""Refresh of direct sales in duckdb"""

# Standard library imports
from contextlib import contextmanager
from pathlib import Path
import shutil
import tempfile

# Third Party Imports
import pandas as pd

def refresh_data(*, data_cfg: dict, conn: object):
    """Read, clean, and load sales data from network file to duckdb"""

    raw_sales = read_raw_sales_data(cfg=data_cfg)
    cleaned = _clean_data(raw_sales)
    _duckdb_load(cleaned, conn=conn)

def _duckdb_load(df: pd.DataFrame, *, conn: object):
    conn.execute(f"CREATE OR REPLACE TABLE category_sales AS SELECT * FROM df")

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
        # group + aggregate
        .groupby(["part_category", "acct_num", "year"], sort=False, as_index=False)
        .agg(total=("amount", "sum"))
    )
    return out

def read_raw_sales_data(cfg: dict):
    """Iterate over params in cfg, read from same file"""    
    frames = []
    with _local_copy(Path(cfg.get("file_path"))) as safe_path:
        for p in cfg.get("params"):
            df = pd.read_excel(
                    io=str(safe_path), 
                    sheet_name=p["sheet_name"],
                    header=p["header"],
                    usecols=p["usecols"]
            )
            renamed = _column_renamer(df, p["rename_map"])
            frames.append(renamed)
    
    return pd.concat(frames)

def _column_renamer(df: pd.DataFrame, rename_map: dict):
    """return dataframe with renamed column"""
    copy = df.copy()
    copy = copy.rename(columns=rename_map)
    return copy

@contextmanager
def _local_copy(file_path: Path):
    """set up and tear down of temporary directory with local copy"""
    try:
        temp_dir = Path(tempfile.mkdtemp())
        dst = temp_dir / file_path.name
        shutil.copy2(file_path, dst)
        yield dst
    finally:
        shutil.rmtree(temp_dir)
    
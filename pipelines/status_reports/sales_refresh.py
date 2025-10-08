"""Refresh of direct sales in duckdb"""

# Standard library imports
from contextlib import contextmanager
from pathlib import Path
import shutil
import tempfile

# Third Party Imports
import pandas as pd
import duckdb

def refresh_data(*, data_cfg: dict, database: str):
    
    raw_sales = read_raw_sales_data(cfg=data_cfg)

    with duckdb.connect(database=database) as conn:
        customers = _get_customers(conn=conn)
        cleaned = _clean_data(raw_sales, customers)
        _duckdb_load(cleaned, conn=conn)

def _duckdb_load(df: pd.DataFrame, *, conn: object):
    conn.execute(f"CREATE TABLE category_sales AS SELECT * FROM df")

def _get_customers(conn: object):
        return set(conn.query(
            """
            SELECT 
                DISTINCT(acct_num)
            FROM customers
            """).fetchdf()["acct_num"])

def _clean_data(df: pd.DataFrame, customers: set) -> pd.DataFrame:
    out = (
        df
        # keep only valid customers
        .query("acct_num in @customers") 
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
    
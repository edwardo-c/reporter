"""Refresh of direct sales in duckdb"""

from dotenv import load_dotenv
from config.paths import STATUS_REPORTS_ENV, STATUS_REPORTS_YAML, ACUMATICA_CREDENTIALS
from os import getenv
from utils.yaml_loader import load_yaml
from utils.acumatica_odata import get_acumatica_table
from pathlib import Path
import tempfile
import shutil
from contextlib import contextmanager
import pandas as pd
from os import getenv

load_dotenv(STATUS_REPORTS_ENV)

def refresh_data():

    cfg = load_yaml(STATUS_REPORTS_YAML)["all_sales"]
    
    raw_sales = read_raw_sales_data(cfg=cfg)

    cleaned = _clean_data(raw_sales)

    _duckdb_load(cleaned)

def _duckdb_load(df: pd.DataFrame):
    breakpoint()
    ...

def _clean_data(df: pd.DataFrame) -> pd.DataFrame:
    # temporary solution for testing, pull from acumatica eventually
    customers = {"AVI062740", "ELE232213", "KAN482651"}

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
    
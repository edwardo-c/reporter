from data_toolkit.readers.sources import XLBundle, XLBundlePart, CSV
from os import getenv
from dotenv import load_dotenv
from config.paths import ALL_SALES_ENV
from pathlib import Path


load_dotenv(ALL_SALES_ENV)

SOURCES = [
    CSV(path=Path(getenv("XREF")), header=0, df_id="xRef"),
    XLBundle(
        path=Path(getenv("INCENTIVE_COMP_2025")),
        parts=[
            XLBundlePart(
                sheet_name="All Direct",
                header=5,
                df_id="all_direct_2025",
            ),
            XLBundlePart(
                sheet_name="POS",
                header=5,
                df_id="pos_2025" 
            )
        ]
    )
]

from data_toolkit.duckdb.sql_dir import SqlDir
SQL_DIR = SqlDir(getenv("ORDERED_SQL"))

ORDERED_SQL: list[Path] = SQL_DIR.paths_list(
    [
        "all_direct_2025",
        "pos_2025"
    ]
)


from data_toolkit.duckdb.union_all_cfg import UnionAllCfg
from data_toolkit.duckdb.client import SQLCol

UNION_ALL_CFG = UnionAllCfg(
    name="All_Sales",
    
    branches=[
        "all_direct_2025_logic",
        "pos_2025_logic",
    ],

    schema=[
        SQLCol("Distributor",         "VARCHAR",    "NULL"),
        SQLCol("Account Number",      "VARCHAR",    "NULL"),
        SQLCol("Customer Name",       "VARCHAR",    "NULL"),
        SQLCol("Part Number",         "VARCHAR",    "NULL"),
        SQLCol("Part Description",    "VARCHAR",    "NULL"),
        SQLCol("Quantity",            "BIGINT",     "NULL"),
        SQLCol("Extended Sales",      "DOUBLE",     "NULL"),
        SQLCol("Order Number",        "VARCHAR",    "NULL"),
        SQLCol("Period Date",         "DATE",       "NULL"),
        SQLCol("Ship To State",       "VARCHAR",    "NULL"),
    ]
)
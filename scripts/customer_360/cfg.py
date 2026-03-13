from data_toolkit.readers.sources import XLBundle, XLBundlePart
from data_toolkit.duckdb.execute_sql.ordered_sql import OrderedSqlCfg
from os import getenv
from dotenv import load_dotenv
from config.paths import ALL_SALES_ENV
from pathlib import Path
from data_toolkit.duckdb.union_all.execute import Col, UnionAllCfg

load_dotenv(ALL_SALES_ENV)

SOURCES = [
  XLBundle(
      path=Path(getenv("INCENTIVE_COMP_2025")),
      parts=[
          XLBundlePart(
              sheet_name="All Direct",
              header=5,
              part_id="all_direct_2025"
          ),
          XLBundlePart(
            sheet_name="POS",
            header=5,
            part_id="pos_2025" 
          )
        ]
  )
]

ORDERED_SQL = OrderedSqlCfg(
    base_dir=Path(getenv("ORDERED_SQL")),
    steps=[
        "all_direct_2025.sql",
        "pos_2025.sql"
      ]
)

UNION_ALL_CFG = UnionAllCfg(
    name="All_Sales",
    
    branches=[
    "all_direct_2025_logic",
    "pos_2025_logic",
    ],

    schema=[
        Col("Distributor",         "VARCHAR",    "NULL"),
        Col("Account Number",      "VARCHAR",    "NULL"),
        Col("Customer Name",       "VARCHAR",    "NULL"),
        Col("Part Number",         "VARCHAR",    "NULL"),
        Col("Part Description", "VARCHAR",    "NULL"),
        Col("Quantity",            "BIGINT",     "NULL"),
        Col("Extended Sales",      "DOUBLE",     "NULL"),
        Col("Order Number",        "VARCHAR",    "NULL"),
        Col("Period Date",         "DATE",       "NULL"),
        Col("Ship To State",       "VARCHAR",    "NULL"),
    ]
)

from dataclasses import dataclass
@dataclass
class AllSalesCfg:
    sources: list[XLBundle]
    ordered_sql: OrderedSqlCfg
    union_all_cfg: UnionAllCfg

CFG = AllSalesCfg(
    sources=SOURCES,
    ordered_sql=ORDERED_SQL,
    union_all_cfg=UNION_ALL_CFG
)
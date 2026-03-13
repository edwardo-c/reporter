import duckdb
from typing import Any, Mapping
from data_toolkit.duckdb.execute_sql.dep_sql_cfg import (
    get_ordered_sql, 
    OrderedSql
)

import logging
logging.basicConfig(level=logging.INFO)

def run_ordered_sql(
        conn: duckdb.DuckDBPyConnection,
        raw_cfg: Mapping[str, Any],
):
    
    sql_files: OrderedSql = get_ordered_sql(raw_cfg)
    for f in sql_files.files:
        logging.info(f"executing sql file: {f}")
        sql = f.read_text(encoding="utf-8")
        conn.execute(sql)


from data_toolkit.duckdb.execute_sql.ordered_sql import OrderedSqlCfg
def run_sql_steps(
        conn: duckdb.DuckDBPyConnection,
        cfg: OrderedSqlCfg,
    ):
    for f in cfg.paths:
        sql = f.read_text(encoding="utf-8")
        conn.execute(sql)
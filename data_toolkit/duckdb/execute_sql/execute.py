import duckdb
from typing import Any, Mapping
from data_toolkit.duckdb.execute_sql.sql_cfg import (
    get_ordered_sql, 
    OrderedSql
)

def run_ordered_sql(
        conn: duckdb.DuckDBPyConnection,
        raw_cfg: Mapping[str, Any],
):
    sql_files: OrderedSql = get_ordered_sql(raw_cfg)
    for f in sql_files.files:
        sql = f.read_text(encoding="utf-8")
        conn.execute(sql)


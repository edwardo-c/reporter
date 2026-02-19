import duckdb
from typing import Any, Mapping
from data_toolkit.duckdb.execute_sql.sql_cfg import SqlCfg


def run_ordered_sql(
        conn: duckdb.DuckDBPyConnection,
        cfg: Mapping[str, Any],
):
    """
    runs all files from config
    """
    sql_cfg = SqlCfg.from_mapping(cfg)

    for f in sql_cfg.files:
        sql = f.read_text(encoding="utf-8")
        conn.execute(sql)

    return sql_cfg.files


"""Interface with duck database files"""

from pathlib import Path

import duckdb
import pandas as pd

from plan_executor.registry import register_operation

@register_operation("duckdb_upload")
def duckdb_upload(
        df: pd.DataFrame, 
        duckdb_path: str | Path, 
        table: str,
        mode: str
        ):
    """
    Upload dataframe into persistent duckdb
    args: 
      df: data set to be placed into file
      duckdb_file: str or filepath to import data to
      table: the table name to import data into
      action: options replace' or 'append'; drop existing and input data or add data to existing
    """
    con = duckdb.connect(duckdb_path)

    # TODO: enforce strict schema matching

    if mode == "replace":
        # overwrite or create fresh table
        con.execute(f"CREATE OR REPLACE TABLE {table} AS SELECT * FROM df")
    elif mode == "append":
        try:
            con.append(table, df)
        except duckdb.CatalogException:
            # table doesn’t exist yet, so create it
            con.execute(f"CREATE TABLE {table} AS SELECT * FROM df")
    else:
        raise ValueError("mode must be 'replace' or 'append'")

    

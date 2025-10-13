import pandas as pd
from pathlib import Path
import duckdb


def create_or_replace(
        table_name: str, 
        df: pd.DataFrame, 
        conn: object = None,
        db_path: str | Path = None) -> None:
    """Create or replace table in duckdb file"""

    def _q(conn: object, df: pd.DataFrame, table_name: str):
        conn.execute(f"CREATE OR REPLACE TABLE {table_name} AS SELECT * FROM df")

    if conn:
        try:
            _q(conn=conn, df=df, table_name=table_name)
        except Exception as e:
            f"conn must be a duckdb.connect() object; {e}"
    else:
        
        if not db_path:
            raise KeyError(f"create_or_replace requires conn or db_path, received none")

        try:
            with duckdb.connect(database=db_path) as conn:
                _q(conn=conn, df=df, table_name=table_name)
        except Exception as e:
            raise TypeError(f"unable to create table on {db_path} {e}")
        
def query_to_df(*, 
        query: str, 
        conn: object | None = None, 
        db_path: str | Path | None = None
    ) -> pd.DataFrame:
    
    if not conn:
        conn = duckdb.connect(db_path)
    
    return conn.execute(query=query).fetch_df()
    
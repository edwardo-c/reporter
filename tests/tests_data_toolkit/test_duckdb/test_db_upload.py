import duckdb
import pytest
import pandas as pd
from pathlib import Path

from data_toolkit.duckdb.duck_query import create_or_replace, query_to_df


def test_create_or_replace_with_conn(df, persistent_duckdb, table_name):
    with duckdb.connect(persistent_duckdb) as conn:
        create_or_replace(table_name=table_name, df=df, conn=conn)
        result: pd.DataFrame = conn.query(f"SELECT * FROM {table_name}").fetchdf()

    pd.testing.assert_frame_equal(result, df)


def test_create_or_replace_without_conn(df, persistent_duckdb, table_name):
    create_or_replace(table_name=table_name, df=df, db_path=persistent_duckdb)
    
    conn = duckdb.connect(persistent_duckdb)
    try:
        result = conn.query(f"SELECT * FROM {table_name}").fetchdf()
    finally:
        conn.close()

    pd.testing.assert_frame_equal(result, df)

def test_query_to_df(df, persistent_duckdb, table_name):
    conn = duckdb.connect(persistent_duckdb)
    create_or_replace(table_name=table_name, df=df, db_path=persistent_duckdb)
    query = f"SELECT * FROM {table_name}"
    result = query_to_df(query=query, conn=conn)
    pd.testing.assert_frame_equal(result, df, check_like=True)

@pytest.fixture
def table_name() -> str:
    return 'my_table'

@pytest.fixture
def df() -> pd.DataFrame:
    """Expected dataframe post stacking of through cfg"""
    return pd.DataFrame(
        {
            'part_number': ['a123', 'b456', 'd456', 'e456'], 
            'category': ['electronic', 'furniture', 'electronic', 'lighting'], 
            'amount': [100, 250, 35, 180]
        }
    )

@pytest.fixture
def persistent_duckdb(tmp_path) -> Path:
    p = tmp_path / "t.duckdb"
    return p
import pytest
from data_toolkit.duckdb.union_all.dep_contract_projection import Col, get_columns, create_projection_query

import duckdb
import pandas as pd

@pytest.fixture
def conn():
    with duckdb.connect() as conn:

        conn.execute(
            """
            CREATE OR REPLACE TABLE tbl (a INTEGER, b INTEGER); 
            INSERT INTO tbl 
              VALUES (5, 42)
            """)
        yield conn

@pytest.fixture
def schema():
    s = [
        Col("str_one", "VARCHAR", "NULL"),
        Col("str_two", "VARCHAR", "NULL"),
        Col("a",   "BIGINT", "NULL"),
        Col("b",   "BIGINT", "NULL")
    ]
    yield s


def test_get_columns(conn):
    columns = get_columns(conn, "tbl")
    assert ('a', 'b') == columns

def test_create_contract_projection(conn: duckdb.DuckDBPyConnection, schema: list[Col]):
    projection_sql = create_projection_query(conn, 'tbl', schema)
    result = conn.execute(projection_sql).df()

    """ensure the contract was applied"""
    result["str_one"] = result["str_one"].astype("string")
    result["str_two"] = result["str_two"].astype("string")
    result["a"] = result["a"].astype("int64")
    result["b"] = result["b"].astype("int64")


    

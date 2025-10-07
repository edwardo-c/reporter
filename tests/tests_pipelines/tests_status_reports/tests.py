"""All tests for status report pipeline"""
import pytest
import pandas as pd
import duckdb

def test_duckdb_upload(tmp_path):
    from pipelines.status_reports.sales_refresh import _duckdb_load
    
    
    df = pd.DataFrame({"col_a": [42]})
    temp_db = tmp_path / "t.duckdb"

    _duckdb_load(df, database=temp_db, table_name="my_table")

    con = duckdb.connect(temp_db)
    result = con.query("SELECT * FROM my_table").df()

    pd.testing.assert_frame_equal(df, result)
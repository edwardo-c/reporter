import pytest
import logging
from data_reporter.reporting.reporter import QueryReader
from data_reporter.data.config import FACT_TABLE_PATH
import pandas as pd

logging.basicConfig(level=logging.INFO)


def test_class_import():
    qr = QueryReader(FACT_TABLE_PATH)
    result = qr._successful_conn()
    assert result

def test_csv_str():
    qr = QueryReader(FACT_TABLE_PATH)
    assert qr.csv == f"read_csv_auto('{FACT_TABLE_PATH}')"

def test_query():
    qr = QueryReader(FACT_TABLE_PATH)
    exp_cols = ['order_id' , 'customer_id', 'product_id', 'quantity', 'price', 'order_date']
    df = qr._query_csv(f"SELECT * FROM")
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 10
    assert all(exp in df.columns for exp in exp_cols)

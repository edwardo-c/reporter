import pytest
from data_reporter.data.config import FACT_TABLE_PATH
from file_reader.safe_reader import SafeReader
from data_reporter.reporter import ReportGenerator
import pandas as pd

def test_report_generator():
    r = ReportGenerator(FACT_TABLE_PATH)
    assert r.data is not None

    
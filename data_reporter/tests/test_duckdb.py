import pytest
from data_reporter.reporter import DuckDB

def test_class_import():
    quack = DuckDB()
    assert quack._successful_import() == True



from pathlib import Path
from dataclasses import dataclass

@dataclass
class DuckDB():
    """instantiate duckdb to read different data sources"""
    import duckdb
    def __init__(self):
        self.csv: str | Path = None

    def _successful_import(self):
        """specifically created for pytest to ensure it is connecting to the class"""
        return True


    def _read_csv():
        ...
    




    duckdb.sql("SELECT 42").show()


class ReportGenerator():
    def __init__(self):
        ...


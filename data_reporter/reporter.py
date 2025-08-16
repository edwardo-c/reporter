

from dataclasses import dataclass
from file_reader.safe_reader import SafeReader
import pandas as pd
import duckdb
from pathlib import Path


"""
DataShaper
Uses duck db to read queries that shape data to specified output
"""


@dataclass
class QueryReader():
    """instantiate duckdb to read query data sources in memory"""
    def __init__(self, csv_path: str | Path):
        self.cursor = duckdb.connect()
        self.csv = self._gen_csv_str(csv_path)
        self.data: pd.DataFrame = {}

    @staticmethod
    def query_data():
        
        ...

    def _successful_conn(self):
        """specifically created for pytest to ensure it is connecting to the class"""
        return True

    def _gen_csv_str(self, csv_path):
        return f"read_csv_auto('{csv_path}')"

    def _query_csv(self, query: str) -> pd.DataFrame:
        return duckdb.sql(
            f"""
            {query} {self.csv};
            """
        ).df()

class ReportGenerator():
    def __init__(self, file_path):
        self.data = self._read_safely(file_path) # load data
        self.processed_data: pd.DataFrame = {} # query data with duckdb

    def _read_safely(self, file_path):
        with SafeReader(file_path) as sr:
            return sr.data

    @classmethod
    def create_with_dataframe(cls, data: pd.DataFrame):
        cls.data = data

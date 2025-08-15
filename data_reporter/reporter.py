from dataclasses import dataclass
import pandas as pd
import duckdb

@dataclass
class QueryReader():
    """instantiate duckdb to read query data sources in memory"""
    def __init__(self, csv_path):
        self.cursor = duckdb.connect()
        self.csv = self._gen_csv_str(csv_path)

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
    def __init__(self):
        ...


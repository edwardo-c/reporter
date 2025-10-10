"""Refresh benefits table in status report duckdb"""

import duckdb
import pandas as pd
from os import getenv
from dotenv import load_dotenv
from config.internal_paths import STATUS_REPORTS_ENV

load_dotenv(STATUS_REPORTS_ENV)

def main():
    
    df = pd.read_csv(getenv("CUSTOMER_BENEFITS"))

    with duckdb.connect(getenv("DUCKDB")) as con:
        con.execute(
            "CREATE OR REPLACE TABLE customers AS SELECT * FROM df"
        )

if __name__ == "__main__":
    main()
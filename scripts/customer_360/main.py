
from data_toolkit.readers.readers import get_dataframe_from_source
from data_toolkit.duckdb.client import DuckRunner
import pandas as pd
from scripts.customer_360.cfg import SOURCES, ORDERED_SQL, UNION_ALL_CFG, SQL_DIR

# MUST ADD IN EXPORT PATH

def main():
    
    with DuckRunner(db_path=None) as duck:

        for src in SOURCES:

            data = get_dataframe_from_source(src, context=None)

            if isinstance(data, dict):
                for k, v in data.items():
                    duck.conn.register(k, v)

            elif isinstance(data, pd.DataFrame):
                duck.conn.register(src.df_id, data)

            else:
                raise TypeError(f"unexpected data type: {type(data).__name__}")
                
        # clean data types? # create table and cast?

        duck.run_ordered_sql(ORDERED_SQL)

        duck.contract_enforced_union_all(
            final_name=UNION_ALL_CFG.name,
            branches=UNION_ALL_CFG.branches,
            schema=UNION_ALL_CFG.schema)

        duck.run_sql_file(SQL_DIR.get_path("xref"))

        duck.conn.execute(f"SELECT * FROM enriched").df().dropna(how="all").to_csv(r"___", index=False)

if __name__ == "__main__":
    main()
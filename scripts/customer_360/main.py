from scripts.customer_360.cfg import CFG
from data_toolkit.readers.readers import get_dataframe_from_source
from data_toolkit.duckdb.execute_sql.execute import run_sql_steps
from data_toolkit.duckdb.union_all.execute import contract_enforced_union_all

import duckdb
import pandas as pd

def main():
    
    with duckdb.connect() as conn:

        for src in CFG.sources:

            data: dict[str, pd.DataFrame] = get_dataframe_from_source(src)

            if isinstance(data, dict):
                for k, v in data.items():
                    conn.register(k, v)
            else:
                raise TypeError(f"unexpected data type: {type(data).__name__}")
                
            # clean data types? # create table and cast?
            run_sql_steps(conn, CFG.ordered_sql)

            contract_enforced_union_all(CFG.union_all_cfg, conn)

            df = conn.execute(f"SELECT * FROM {CFG.union_all_cfg.name}").df().dropna(how="all")

            breakpoint()

if __name__ == "__main__":
    main()
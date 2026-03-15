from data_toolkit.duckdb.client import DuckRunner
from scripts.activity_ledger.cfg import (
    SOURCES,
    ORDERED_SQL, 
    UNION_ALL_CFG, 
    SQL_DIR, 
    CTX,
    OUTPUT_SCHEMA,
    BULK_OBJ
)

from data_toolkit.readers.readers import get_dataframe_from_source
from data_toolkit.cleaners.df_dtypes.dtype import enforce_schema
from data_toolkit.salesforce.payload.payload import build_bulk_payload
from data_toolkit.salesforce.payload.results import build_failed_df

import logging
logging.basicConfig(level=logging.INFO)

def main():

    with DuckRunner(db_path=None) as duck:

        for src in SOURCES:
            
            df = get_dataframe_from_source(src, CTX)

            duck.conn.register(src.df_id, df)

        duck.run_ordered_sql(ORDERED_SQL)

        duck.contract_enforced_union_all(
            final_name=UNION_ALL_CFG.name, 
            branches=UNION_ALL_CFG.branches, 
            schema=UNION_ALL_CFG.schema
        )

        duck.run_sql_file(SQL_DIR.get_path("finalize"))

        df = enforce_schema(
            OUTPUT_SCHEMA,
            duck.conn.execute(f"SELECT * FROM final_payload").df()
        )
    
    payload = build_bulk_payload(df, BULK_OBJ, validate=True)

    result = getattr(
        CTX.sf.bulk, BULK_OBJ.name
        ).upsert(payload, BULK_OBJ.external_id_name)

    failed_df = build_failed_df(result, payload)

    if len(failed_df) > 0:
        failed_df.to_csv(r"C:\Users\eddiec11us\Desktop\failed.csv")
        print(f"Failed rows saved to desktop")
    else:
        print("Successfuly ran Activity Ledger upsert")

if __name__ == "__main__":
    main()
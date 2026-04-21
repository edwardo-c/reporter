from data_toolkit.duckdb.client import DuckRunner
from scripts.salesforce.activity_tracker.ledger.cfg import (
    SOURCES,
    ORDERED_SQL, 
    UNION_ALL_CFG, 
    SQL_DIR, 
    CTX,
    ACTIVITY_LEDGER_NAME,
    ACTIVITY_LEDGER_SCHEMA,
    ACTIVITY_LEDGER_EXT_ID
)

from data_toolkit.readers.readers import get_dataframe_from_source
from data_toolkit.salesforce.bulk_upsert import SFBulkObj

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

        stacked_df = duck.conn.execute(f"SELECT * FROM final_payload").df()

    # check to see if results have changed, only upsert if changes found

    activity_ledger = SFBulkObj(
        object_name=ACTIVITY_LEDGER_NAME,
        external_id=ACTIVITY_LEDGER_EXT_ID,
        schema=ACTIVITY_LEDGER_SCHEMA,
        df=stacked_df
    )
    
    activity_ledger.upsert(CTX.sf)

    if activity_ledger.has_failed_rows:
        activity_ledger.failed_df_to_csv(r"C:\Users\eddiec11us\Desktop\failed.csv")
        print("exported failed rows")
    else:
        print("Successfuly ran Activity Ledger upsert")

if __name__ == "__main__":
    main()
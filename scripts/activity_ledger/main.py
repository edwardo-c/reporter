from dotenv import load_dotenv

import duckdb
from config.paths import SF_ACTIVITIES_ENV, SF_ACTIVITIES_REPORT_CFG
from data_toolkit.duckdb.execute_sql.execute import run_ordered_sql
from data_toolkit.duckdb.union_all.dep_contract_projection import contract_enforced_union_all
from data_toolkit.salesforce.client import SFClient
from data_toolkit.cleaners.df_dtypes.dtype import enforce_schema
from scripts.activity_ledger.schema import OUTPUT_SCHEMA, BULK_OBJ
from data_toolkit.salesforce.payload.payload import build_bulk_payload
from utils.yaml_loader import load_yaml
from scripts.activity_ledger.SOQL.registry import get_query, load_queries
from data_toolkit.salesforce.payload.results import build_failed_df

import logging
logging.basicConfig(level=logging.INFO)

# the configuration file to use for the pipeline
YAML = "activities.yaml"

def main():

    load_dotenv(SF_ACTIVITIES_ENV)
    cfg = load_yaml(SF_ACTIVITIES_REPORT_CFG)
    load_queries()

    sf = SFClient(**cfg["credentials"])

    with duckdb.connect() as conn:

        for report in cfg["reports"]:
            
            df = sf.query(get_query(report["query_key"]), df=True)

            conn.register(report["register_as"], df)
        
        run_ordered_sql(conn, cfg["sql"])

        contract_enforced_union_all(cfg["union_all"], conn)

        run_ordered_sql(conn, cfg["enrich"])

        # clean dataframe types and values
        df = enforce_schema(
            OUTPUT_SCHEMA,
            conn.execute(f"SELECT * FROM final_payload").df()
        )

        payload = build_bulk_payload(df, BULK_OBJ, validate=True)

    result = sf.upsert(BULK_OBJ, payload)

    failed_df = build_failed_df(result, payload)

    if len(failed_df) > 0:
        failed_df.to_csv(r"C:\Users\eddiec11us\Desktop\failed.csv")
        print(f"Failed rows saved to desktop")
    else:
        print("Successfuly ran Activity Ledger upsert")

if __name__ == "__main__":
    main()
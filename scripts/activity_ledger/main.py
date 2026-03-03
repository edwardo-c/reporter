from dotenv import load_dotenv

import duckdb

from config.paths import SF_ACTIVITIES_ENV, SF_ACTIVITIES_REPORT_CFG
from data_toolkit.duckdb.execute_sql.execute import run_ordered_sql
from data_toolkit.duckdb.union_all.contract_projection import contract_enforced_union_all
from data_toolkit.salesforce.client import SFClient
from data_toolkit.salesforce.reports_tabular.payload_to_df import payload_to_df

from utils.yaml_loader import load_yaml

import logging
logging.basicConfig(level=logging.INFO)

# the configuration file to use for the pipeline
YAML = "activities.yaml"

def main():

    load_dotenv(SF_ACTIVITIES_ENV)
    cfg = load_yaml(SF_ACTIVITIES_REPORT_CFG)
    sf = SFClient(**cfg["credentials"])

    with duckdb.connect() as conn:

        for report in cfg["reports"]:
            
            payload = sf.get_report(report["sf_id"])
            
            df = payload_to_df(payload, report["human_readable"])

            conn.register(report["register_as"], df)
        
        run_ordered_sql(conn, cfg["sql"])

        stacked_view = contract_enforced_union_all(cfg["union_all"], conn)

        finalize_sql = run_ordered_sql(conn, cfg["enrich"])

        df = conn.execute(f"SELECT * FROM enriched").df()

    df.to_csv(cfg["test_out"], index=False)

if __name__ == "__main__":
    main()
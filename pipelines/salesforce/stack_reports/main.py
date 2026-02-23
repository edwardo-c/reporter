from data_toolkit.salesforce.client import SFClient
from utils.yaml_loader import load_yaml
from dotenv import load_dotenv
from pipelines.paths.cfg_paths import SALESFORCE_REPORT_STACK_CFGS
from config.paths import SF_ACTIVITIES_ENV
from data_toolkit.salesforce.reports_tabular.payload_to_df import payload_to_df
from data_toolkit.duckdb.execute_sql.execute import run_ordered_sql
import duckdb

# the configuration file to use for the pipeline
YAML = "activities.yaml"

def main():

    load_dotenv(SF_ACTIVITIES_ENV)
    cfg = load_yaml(SALESFORCE_REPORT_STACK_CFGS / YAML)
    sf = SFClient(**cfg["credentials"])

    conn = duckdb.connect()

    for report in cfg["reports"]:
        payload = sf.get_report(report["sf_id"])
        df = payload_to_df(payload)
        conn.register(report["register_as"], df)
    
    run_ordered_sql(conn, cfg["sql"])
    breakpoint()

if __name__ == "__main__":
    main()
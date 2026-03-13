from dotenv import load_dotenv
import logging

import duckdb

from config.paths import CREDIT_EVENTS_ENV, CREDIT_EVENTS_CFG
from data_toolkit.duckdb.execute_sql.execute import run_ordered_sql
from data_toolkit.duckdb.register_frames.register_frames import register_frames_from_cfg
from data_toolkit.duckdb.union_all.dep_contract_projection import contract_enforced_union_all
from utils.yaml_loader import load_yaml

logging.basicConfig(level=logging.INFO)

def main():

    load_dotenv(CREDIT_EVENTS_ENV)
    
    cfg = load_yaml(CREDIT_EVENTS_CFG)
    
    db = cfg["database"]
    sources = cfg["sources"]
    ordered_sql = cfg["sql"]
    union_all_cfg = cfg["union_all"]
    final_name = union_all_cfg["final_view"]["name"]

    with duckdb.connect(db) as conn:

        register_frames_from_cfg(sources, conn)
        logging.info(f"frames registered")

        # holds all business logic
        run_ordered_sql(conn, ordered_sql)
        logging.info(f"ordered sql ran")

        contract_enforced_union_all(union_all_cfg, conn)

        df = conn.execute(f"SELECT * FROM {final_name}").df()

    df.to_csv(cfg["out_path"], index=False)

"""
will need to implement a refresh on reclass interface
with xlwings.app.RefreshAll() 
and poll refresh state 
with xlwings.app.CalculateState == 0
"""

if __name__ == "__main__":
    main()
import duckdb
from utils.yaml_loader import load_yaml
from config.paths import CREDIT_EVENTS_ENV, CREDIT_EVENTS_CFG
from dotenv import load_dotenv
from data_toolkit.duckdb.execute_sql import run_ordered_sql
from data_toolkit.duckdb.register_frames.register_frames import register_frames_from_cfg

import logging
logging.basicConfig(level=logging.INFO)

def main():

    load_dotenv(CREDIT_EVENTS_ENV)
    
    cfg = load_yaml(CREDIT_EVENTS_CFG)
    
    db = cfg["database"]
    
    
    sources = cfg["credit_events_pipeline"]["sources"]

    ordered_sql = cfg["credit_events_pipeline"]["sql"]

    with duckdb.connect(db) as conn:

        register_frames_from_cfg(sources, conn)
        logging.info(f"frames registered")

    breakpoint()
    
    # holds all business logic
    # run_ordered_sql(conn, ordered_sql)

    # TODO: enforce CanonicalSchema and apply UNION ALL
    
    # TODO: export


"""
will need to implement a refresh on reclass interface
with xlwings.app.RefreshAll() 
and poll refresh state 
with xlwings.app.CalculateState == 0
"""

if __name__ == "__main__":
    main()
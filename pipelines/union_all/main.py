import duckdb
from utils.yaml_loader import load_yaml
from config.paths import CREDIT_EVENTS_ENV, CREDIT_EVENTS_CFG
from dotenv import load_dotenv
import pandas as pd
from pathlib import Path
from data_toolkit.duckdb.register_frames import register_frames
from data_toolkit.duckdb.execute_sql import run_ordered_sql


def main():

    load_dotenv(CREDIT_EVENTS_ENV)
    
    cfg = load_yaml(CREDIT_EVENTS_CFG)
    
    db = cfg["database"]
    
    sources = cfg["credit_events_pipeline"]["sources"]
    
    ordered_sql = cfg["credit_events_pipeline"]["sql"]

    with duckdb.connect(db) as conn:
        
        _ = register_frames(conn, sources)
       
        breakpoint()

        run_ordered_sql(conn, ordered_sql)

        # enforce CanonicalSchema and apply UNION ALL
    
        # inspect export manually - escape hatch:
        # df = conn.execute("select * from stg_credit_events").df()
        # df.to_csv(r"C:\Users\eddiec11us\Documents\credit_events.csv", index=False)


"""
will need to implement a refresh on reclass interface
with xlwings.app.RefreshAll() 
and poll refresh state 
with xlwings.app.CalculateState == 0
"""

if __name__ == "__main__":
    main()
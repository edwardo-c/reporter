import duckdb
from utils.yaml_loader import load_yaml
from config.paths import CREDIT_EVENTS_ENV, CREDIT_EVENTS_CFG
from dotenv import load_dotenv
from data_toolkit.duckdb.execute_sql import run_ordered_sql
from data_toolkit.duckdb.register_frames.config_normalizer import ConfigNormalizer

def main():

    load_dotenv(CREDIT_EVENTS_ENV)
    
    cfg = load_yaml(CREDIT_EVENTS_CFG)
    
    db = cfg["database"]
    conn = duckdb.connect(db)
    
    sources = cfg["credit_events_pipeline"]["sources"]
    cfg_normalizer = ConfigNormalizer()
    
    ordered_sql = cfg["credit_events_pipeline"]["sql"]


    for cfg_id, raw_src_cfg in sources.items():

        clean_cfg = cfg_normalizer.from_cfg(raw_src_cfg)

        # TODO: register frame
        ...

    # holds all business logic
    run_ordered_sql(conn, ordered_sql)

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
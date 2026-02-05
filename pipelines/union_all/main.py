import duckdb
from utils.yaml_loader import load_yaml
from config.paths import CREDIT_EVENTS_ENV, CREDIT_EVENTS_CFG
from dotenv import load_dotenv
import pandas as pd
from pathlib import Path
from data_toolkit.duckdb.register_frames import register_frames

"""
=============

provide config, 
read all, 
process through sql pipeline, 
fill table,

==============

when new data comes in?
refresh the entire year

"""

"""
can you convert this into a non-specific pipeline?
as in: provide a config to do 'this thing' for any cfg?
"""


def load_credit_events():

    load_dotenv(CREDIT_EVENTS_ENV)
    cfg = load_yaml(CREDIT_EVENTS_CFG)
    db = cfg["database"]
    sources = cfg["credit_events_pipeline"]["sources"]
    sql = cfg["credit_events_pipeline"]["sql"]
    sql_base_dir = Path(sql["base_dir"])

    with duckdb.connect(db) as conn:
        
        register_frames(conn, sources)
       
        breakpoint()
        
        # business logic
        for step in sql["steps"]:

            sql = Path(sql_base_dir / step).read_text()
            conn.execute(sql)

        # enforce CananicalSchema and apply UNION ALL
    
        
        
        
        # df = conn.execute("select * from stg_credit_events").df()
        # df.to_csv(r"C:\Users\eddiec11us\Documents\credit_events.csv", index=False)


"""
will need to implement a refresh on reclass interface
with xlwings.app.RefreshAll() 
and poll refresh state 
with xlwings.app.CalculateState == 0
"""

if __name__ == "__main__":

    load_credit_events()
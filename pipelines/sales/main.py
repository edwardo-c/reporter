import duckdb
from utils.yaml_loader import load_yaml
from config.paths import SALES_ENV, SALES_CFG
from dotenv import load_dotenv
import pandas as pd
from pathlib import Path

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

def load_credit_events():

    load_dotenv(SALES_ENV)
    cfg = load_yaml(SALES_CFG)
    db = cfg["database"]
    sources = cfg["credit_events_pipeline"]["sources"]
    sql = cfg["credit_events_pipeline"]["sql"]
    sql_base_dir = Path(sql["base_dir"])

    with duckdb.connect(db) as conn:
        
        # register all sources
        for src, params in sources.items():

            path = params["path"]
            sheet = params["sheet"]
            header = params["header"]

            df = pd.read_excel(path, sheet_name=sheet, header=header)

            conn.register(params["register_as"], df)

        for step in sql["steps"]:

            sql = Path(sql_base_dir / step).read_text()
            conn.execute(sql)
        
        df = conn.execute("select * from stg_credit_events").df()
        df.to_csv(r"my_test_csv", index=False)


"""
will need to implement a refresh on reclass interface
with xlwings.app.RefreshAll() 
and poll refresh state 
with xlwings.app.CalculateState == 0
"""

if __name__ == "__main__":

    load_credit_events()
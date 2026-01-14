from pathlib import Path

from utils.yaml_loader import load_yaml
from dotenv import load_dotenv
from config.paths import POS_XREF_ENV_VARS, POS_XREF_CFG

import duckdb

load_dotenv(dotenv_path=Path(POS_XREF_ENV_VARS))

STEP = "promote"

"""
Tables:
customers:       confirmed (ParentName, BillToState, BillToZip) - distinct ParentName 
cross_Reference  ParentName -> ChildName - duplicate parents to 1 ChildName 
candidates       names to be reviewed (ChildName, BillToCustomerZip, BillToCustomerState)
decisions        bridge to promote candidate to customer and remove from candidates

What It Does:
Identifies new ChildNames and adds them to a queue for review

How To Run: 

when new pos data is available, cut csv, format dates as mm/dd/yyy

run export_candidates

Manual User Intervention: 

review candidates to match with existing ParentNames
review candidates with other candidates for new ParentNames

run promote_candidates

"""

BATCH_ID = "2025_11_POS"

cfg = load_yaml(POS_XREF_CFG)


def export_candidates():
    
    db_path = cfg["xref_db"]
    conn = duckdb.connect(db_path)

    # load raw pos sales for history tracking
    sql_load = Path(cfg["sql_load_raw_pos"]).read_text()
    pos_sales_path = cfg["pos_sales"]
    conn.execute(sql_load, [BATCH_ID, pos_sales_path])

    # update candidates
    sql_insert_candidates = Path(cfg["sql_candidates"]).read_text()
    conn.execute(sql_insert_candidates)

    # export candidates
    candidates_out = cfg["candidates_out"]
    candidates_df = conn.execute("SELECT * FROM candidates").df()
    candidates_df.to_csv(candidates_out, index=False)

    # export xref?

    # export latest customers so user may compare new candidates with existing customers
    customers_out = cfg["customers_out"]
    customers_df = conn.execute("SELECT * FROM customers").df()
    customers_df.to_csv(customers_out, index=False)


def promote_candidates():
    ...


if __name__ == "__main__":
    
    main()
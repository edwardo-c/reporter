from pathlib import Path

from utils.yaml_loader import load_yaml
from dotenv import load_dotenv
from config.paths import POS_XREF_ENV_VARS, POS_XREF_CFG

import duckdb

load_dotenv(dotenv_path=Path(POS_XREF_ENV_VARS))

STEP = "promote"

"""
What It Does:
Identifies new ChildNames and adds them to a queue for review

How To Run: 
when new pos data is available, cut csv, format dates as mm/dd/yyy

STEP = "candidates"
python -m pipelines.pos_xref.main

Manual Intervention: 
review candidates: 
1. match candidates ChildNames to existing ParentNames
2. match candidates with other candidates for NEW ParentNames
3. add ParentName, ChildName, BillToState (nullable), BillToZip (nullable) to decisions.csv

STEP = "promote"
python -m pipelines.pos_xref.main

"""

BATCH_ID = "2025_11_POS"
STEP = "promote"
CFG = load_yaml(POS_XREF_CFG)

def get_candidates(conn: object):
    
    # ========== Exports for manual step ======================

    # load raw pos sales for history tracking
    raw_sales_path = CFG["raw_pos_sales"]
    sql_load_raw_pos = Path(CFG["sql_load_raw_pos"]).read_text()
    conn.execute(sql_load_raw_pos, [BATCH_ID, raw_sales_path])

    # load candidates
    sql_load_candidates = Path(CFG["sql_load_candidates"]).read_text()
    conn.execute(sql_load_candidates)

    # ========== Exports for manual step ======================
    candidates_out = CFG["candidates_out"]
    candidates_df = conn.execute("SELECT * FROM candidates").df()
    candidates_df.to_csv(candidates_out, index=False)

    xref_out = CFG["xref_out"]
    xref_df = conn.execute("SELECT * FROM cross_reference").df()
    xref_df.to_csv(xref_out, index=False)

    customers_out = CFG["customers_out"]
    customers_df = conn.execute("SELECT * FROM customers").df()
    customers_df.to_csv(customers_out, index=False)


def commit_decisions(conn: object):
    
    decisions_path = CFG["decisions_path"]

    decisions_df = conn.execute("SELECT * FROM read_csv_auto(?);", [decisions_path]).df()
    conn.execute(f"""
        CREATE OR REPLACE TEMP TABLE decisions AS
        SELECT DISTINCT
          ParentName,
          ChildName,
          BillToState,
          BillToZip
        FROM decisions_df;
    """)

    decisions_sql = Path(CFG["decisions_sql"]).read_text()
    conn.execute(decisions_sql)


if __name__ == "__main__":
    
    db_path = CFG["db"]

    with duckdb.connect(db_path) as conn:
        
        if STEP == "candidates":
            get_candidates(conn)
        
        elif STEP == "promote":
            commit_decisions(conn)
        
        else:
            raise ValueError(f"invalid STEP: {STEP}. Must be 'candidates' or 'promote'")
from data_toolkit.duckdb.union_all.contract_projection import Col

FINAL_SCHEMA = [
    Col("SalesRepID18",   "VARCHAR", "NULL"),
    Col("ActivityCode",   "VARCHAR", "NULL"),
    Col('ActivityDate',   "DATE",    "NULL")
]
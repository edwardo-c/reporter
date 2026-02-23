from data_toolkit.duckdb.union_all.contract_projection import Col

FINAL_SCHEMA = [
    Col("SalesRep",       "VARCHAR", "NULL"),
    Col("CreditType",     "VARCHAR", "NULL"),
    Col("ActivityDate",   "DATE",    "NULL"),
    Col("ActivityScore",  "BIGINT",  "NULL"),
    Col("ActivityID",     "VARCHAR", "NULL")
]
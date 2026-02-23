from data_toolkit.duckdb.union_all.contract_projection import Col
FINAL_SCHEMA = [
    Col("SalesRep",       "dtype", "NULL"),
    Col("CreditType",     "dtype", "NULL"),
    Col("ActivityDate",   "dtype", "NULL"),
    Col("ActivityScore",  "dtype", "NULL"),
    Col("ActivityID",     "dtype", "NULL")
]
from scripts.salesforce_audit.customer_price_groups.config import SOURCES, ENV_VAR_PATH, SQL_PATH
from scripts.salesforce_audit.customer_price_groups.loaders import query_and_load
from scripts.salesforce_audit.secrets import load_env_vars
from scripts.salesforce_audit.builders import get_reader_ctx
import duckdb
from data_toolkit.duckdb.client import execule_sql_path

def main():

    env_vars = load_env_vars(ENV_VAR_PATH)
    conn = duckdb.connect()
    ctx = get_reader_ctx(env_vars)

    query_and_load(sources=SOURCES, context=ctx, conn=conn)

    execule_sql_path(SQL_PATH, conn)

    df = conn.execute("SELECT * FROM result").df()

if __name__ == "__main__":
    main()
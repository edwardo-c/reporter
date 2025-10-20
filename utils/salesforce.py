from simple_salesforce import Salesforce
import pandas as pd

def get_salesforce_table(
        username: str,
        password: str,
        security_token: str, 
        soql_query: str | list[str]) -> pd.DataFrame:
    """soql_query = SOQL, df bool if you want the plain dict from the json response or a pandas dataframe"""

    # --- auth (prod) ---
    sf = Salesforce(
        username=username,
        password=password,
        security_token=security_token,
        domain="login"
    )

    # --- run SOQL ---
    records = sf.query_all(query=soql_query)["records"]
    
    return pd.json_normalize(records).drop(columns="attributes", errors="ignore")





from simple_salesforce import Salesforce
import pandas as pd

def run_SOQL(
        auth: dict[str, str], 
        query: str,
        df: bool) -> pd.DataFrame | dict:
    
    # --- auth (prod) ---
    sf = Salesforce(
        username=auth.get("username"),
        password=auth.get("password"),
        security_token=auth.get("security_token"),
        domain="login"
    )

    # --- run SOQL ---
    records = sf.query_all(query=query)["records"]

    if df:
        return (pd.json_normalize(records)
               .drop(columns="attributes", errors="ignore"))
    else:
        return records

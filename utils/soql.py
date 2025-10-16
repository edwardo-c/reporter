from simple_salesforce import Salesforce
import pandas as pd

def run_SOQL(
        auth: dict[str, str], 
        query: str | list[str],
        df: bool) -> list[pd.DataFrame | dict] :
    
    # --- auth (prod) ---
    sf = Salesforce(
        username=auth.get("username"),
        password=auth.get("password"),
        security_token=auth.get("security_token"),
        domain="login"
    )

    if isinstance(query, str):
        query = query[query]

    out = []

    # --- run SOQL ---
    for q in query:    
        records = sf.query_all(query=q)["records"]
        if df:
            out.append(
                    pd.json_normalize(records)
                    .drop(columns="attributes", errors="ignore"))
        else:
            out.append(records)
    
    return out





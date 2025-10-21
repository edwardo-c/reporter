from simple_salesforce import Salesforce
import pandas as pd

def get_salesforce_table(
        soql_query: str | list[str],
        sf: Salesforce = None,
        username: str = None,
        password: str = None,
        security_token: str = None) -> pd.DataFrame:

    if not sf:
        # --- auth (prod) ---
        sf = Salesforce(
            username=username,
            password=password,
            security_token=security_token,
            domain="login"
        )

    # --- run SOQL ---
    records = sf.query_all(query=soql_query)["records"]
    
    df = pd.json_normalize(records)

    return df.drop(columns=[c for c in list(df.columns) if 'attributes.' in c], errors="ignore")





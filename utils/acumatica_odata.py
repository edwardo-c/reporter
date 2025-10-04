import requests
import pandas as pd

def get_acumatica_table(url: str, username: str, password: str, params: dict) -> pd.DataFrame:
    """returns data table from odata url in acumatica"""

    resp = requests.get(url, auth=(username, password), params=params)
    resp.raise_for_status()

    data = resp.json().get("value", [])
    return pd.DataFrame(data)
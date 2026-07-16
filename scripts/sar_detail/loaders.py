import pandas as pd
import requests
from os import getenv

class EnvVarStrings:
    user = "ACUMATICA_USERNAME"
    pw = "ACUMATICA_PASSWORD"

class DirectSalesOdata:
    url = r'https://peerless-av.acumatica.com/OData/Peerless-AV/EOM%20Line%20Details%20-%20Sales%20Ops?'
    params = {
        "$filter": """
            (
              AccountCD eq '5040'
              or AccountCD eq '5000'
            )
            and (
              AccountOwner eq 'CW7092' 
              or PROAccountTypeBillToShipTo eq 'Ship To'
            ) 
            and (
                ShipToRegion eq 'North Central - Great Lakes'
            )
            """,
        "$select": """
            CustomerAccountNumber,CustomerName,PROAccountTypeBillToShipTo,
            InventoryCD,UnitPrice,Qty,Amount,InvoiceDate,ClassificationSalesCategory,
            ShipToAddressLine1,ShipToCity,ShipToState,ShipToZipCode
            """,
        "$format": "json"
    }

"""
debugging - for browser:
  https://peerless-av.acumatica.com/OData/Peerless-AV/
    EOM%20Line%20Details%20-%20Sales%20Ops?
    $filter=AccountOwner%20eq%20%27CW7092%27%
    20or%20PROAccountTypeBillToShipTo%20eq%20%27Ship%20To%27%20
    and%20ShipToRegion%20eq%20%27North%20Central%20-%20Great%20Lakes%27
    &$top=5
"""

def authenticate_acumatica() -> requests.Session:
    s = requests.Session()
    u = getenv(EnvVarStrings.user)
    pw = getenv(EnvVarStrings.pw)
    if u is None:
        raise KeyError(f"unable to retrieve Acumatica username from dot env")
    if pw is None:
        raise KeyError(f"unable to retrieve Acumatica password from dot env")
    s.auth = (u, pw)
    return s

def get_direct_sales_df() -> pd.DataFrame:

    acu_client = authenticate_acumatica()
    
    res = acu_client.get(DirectSalesOdata.url, params=DirectSalesOdata.params)
    res.raise_for_status()

    try:
        payload: dict = res.json()
    except ValueError:
        raise ValueError(f"Non-JSON response from Acumatica: {res.text[:200]}")

    data = payload.get("value", [])

    return pd.json_normalize(data)



def get_indirect_sales():
    
    ...

def load_sales_data_to_db():
    direct_sales_df = get_direct_sales_df()
    breakpoint()
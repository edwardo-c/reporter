import pandas as pd
import requests
from os import getenv
from pathlib import Path
from dataclasses import dataclass

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
            ShipToAddressLine1,ShipToCity,ShipToState
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


@dataclass
class POSDataCfg:
    path: Path
    sheet_name: str
    header: int
    use_cols: list[str]
    register_as: str

POS_2024_CFG = POSDataCfg(
    path = Path(r"\\peernet\DavWWWRoot\Reporting\POS DATA\2024 - 2025 POS Pivot IncentiveComp.xlsx"),
    sheet_name="RawData",
    header=0,
    use_cols=[
        "Customer", "SoldToName",
        "PiiPartNumber", "ShipQuantity", "ExtendedSales", "SaleDate", "PeriodDate", "PiiCategory", 
        "ShipToState", "SalesRep"
    ],
    register_as="raw_pos_2024"
)

POS_2025_TO_2026_CFG = POSDataCfg(
    path = Path(r"\\peernet\DavWWWRoot\Reporting\POS DATA\2025 - 2026 POS Pivot Incentive Comp.xlsx"),
    sheet_name="POS - 2025 to 2026",
    header=0,
    use_cols=[
        "Customer", "Sold To Name",
        "Part Number", "Quantity", "Extended Sales", "Sale Date", "Period Date", "Category", 
        "Ship To State", "Sales Rep"
    ],
    register_as="raw_pos_2025_to_2026"
)

def get_pos_sales_df(cfg: POSDataCfg) -> pd.DataFrame:
    if not cfg.path.exists():
        raise FileNotFoundError("2024 pos file does not exist")

    df = pd.read_excel(
        io=str(cfg.path), 
        sheet_name=cfg.sheet_name, 
        header=cfg.header, 
        usecols=cfg.use_cols
    )  

    if df.empty:
        raise Exception(f"{cfg.register_as} dataframe is empty!")

    return df

def filter_2024_pos_df(df: pd.DataFrame) -> pd.DataFrame:
    _df = df.copy()
    _df = _df.query("SalesRep == 'SCHNEIDER'")
    mask = pd.to_datetime(_df["PeriodDate"]).dt.year == 2024
    _df = _df[mask]
    if _df.empty:
        raise Exception("2024 pos dataframe is empty!")
    _df.reset_index(drop=True)
    return _df


def filter_2025_to_2026_pos_df(df: pd.DataFrame) -> pd.DataFrame:
    _df = df.copy()
    _df = _df.query("`Sales Rep` == 'SCHNEIDER' | `Sales Rep` == 'North Central - Great Lakes'")
    years = pd.to_datetime(_df["Period Date"]).dt.year
    mask = years.isin([2025, 2026])
    _df = _df[mask]
    if _df.empty:
        raise Exception("2025 - 2026 pos dataframe is empty!")
    _df.reset_index(drop=True)
    return _df

def load_sales_data_to_db():
    direct_sales_df = get_direct_sales_df()

    pos_2024_df = get_pos_sales_df(POS_2024_CFG)
    filtered_pos_2024_df = filter_2024_pos_df(pos_2024_df)
    
    pos_2025_to_2026_df = get_pos_sales_df(POS_2025_TO_2026_CFG)
    filtered_pos_2025_to_2026_df = filter_2025_to_2026_pos_df(pos_2025_to_2026_df)

    breakpoint()
# standard library imports
from dotenv import load_dotenv
from pathlib import Path

# Third party imports
import pandas as pd

# Internal Imports
from config.paths import PRICE_LIST_ENV, PRICE_LIST_CFG_YAML
from utils.acumatica_odata import get_acumatica_table
from utils.yaml_loader import load_yaml

def main():

    print(f"Splitting CSVs")

    load_dotenv(PRICE_LIST_ENV)
    cfg: dict = load_yaml(PRICE_LIST_CFG_YAML)

    odata_cfg = cfg.get("odata_cfg", {}) 

    df: pd.DataFrame = get_acumatica_table(
        url=odata_cfg["url"], 
        username=odata_cfg["username"], 
        password=odata_cfg["password"], 
        params=odata_cfg["params"]
    )
    
    # enforce column order
    df = df[odata_cfg["column_order"]]

    branded = _add_brand_column(df=df)

    # hot loop
    _export_partitioned_csv(branded, out_map=cfg["out_map"])

    print(f"Process Complete")

def _add_brand_column(df: pd.DataFrame):
    
    df_copy = df.copy()
    df_copy["brand"] = (df_copy["PriceGroup"] == "NEPTUNE")
    df_copy["brand"] = df_copy["brand"].replace({False: "Peerless-AV", True: "Neptune"})

    return df_copy

def _export_partitioned_csv(
        df: pd.DataFrame,
        out_map: dict[str, str]
    ) -> None | list:

    """
    partition by and export to specified folder
    """
    for brand, partition in df.groupby(by="brand", dropna=True):
        
        root_dir = Path(out_map.get(brand))

        for cust, part in partition.groupby(by="Customer"):
            
            export_path = root_dir / f"{cust}.csv"
            
            part.to_csv(export_path, index=False)


if __name__ == "__main__":
    raise SystemExit(main())


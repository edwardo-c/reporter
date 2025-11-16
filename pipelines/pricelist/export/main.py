# standard library imports
from dotenv import load_dotenv
from pathlib import Path
import logging

# Third party imports
import pandas as pd

# Internal Imports
from config.paths import PRICE_LIST_ENV, PRICE_LIST_CFG_YAML
from utils.acumatica_odata import get_acumatica_table
from utils.yaml_loader import load_yaml
from data_toolkit.cleaners.data_cleaner import DataCleaner
from data_toolkit.clients.acumatica import AcumaticaClient

logger = logging.basicConfig(level=logging.INFO)

def main():

    print(f"Exporting data for Price List Process")

    load_dotenv(PRICE_LIST_ENV)
    cfg: dict = load_yaml(PRICE_LIST_CFG_YAML)

    data_cfg = cfg.get("data_cfg", {})
    eol_cfg = data_cfg["eol"]
    master_pricing_cfg = data_cfg["master_pricing"]
    
    with AcumaticaClient(**cfg["acu_auth"]) as ac:
        
        eol_df = ac.odata(url=eol_cfg["url"], params=eol_cfg["params"], df=True)
        
        master_pricing_df = ac.odata(
            url=master_pricing_cfg["url"], 
            params=master_pricing_cfg["params"], 
            df=True
        )

    cleaned_eol = DataCleaner(**eol_cfg["cleaner_cfg"]).clean(eol_df)

    cleaned_master_pricing_df = DataCleaner(
        **master_pricing_cfg["cleaner_cfg"]
        ).clean(master_pricing_df)

    branded = _add_brand_column(df=cleaned_master_pricing_df)

    # hot loop
    cleaned_eol.to_csv(eol_cfg["out"], index=False)
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


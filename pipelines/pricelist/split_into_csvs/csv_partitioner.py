"""Primary runner for CSV brand seperation and export"""
import pandas as pd

import numpy as np

from pathlib import Path

def run(df: pd.DataFrame, out_map: dict[str, Path]):
    
    branded = _add_brand_column(df)

    _export_partitioned_csv(branded, out_map)

def _add_brand_column(df: pd.DataFrame):
    
    df_copy = df.copy()
    df_copy["brand"] = (df_copy["Price Group"] == "NEPTUNE")
    df_copy["brand"] = df_copy["brand"].replace({False: "Peerless-AV", True: "Neptune"})

    return df_copy


def _export_partitioned_csv(
        df: pd.DataFrame,
        brand_dir_map: dict[str, Path]
    ) -> None | list:

    """
    partition by and export to specified folder
    """
    for brand, partition in df.groupby(by="brand", dropna=True):
        
        root_dir = Path(brand_dir_map.get(brand))

        for cust, part in partition.groupby(by="Customer"):
            
            export_path = root_dir / f"{cust}.csv"
            
            part.to_csv(export_path, index=False)

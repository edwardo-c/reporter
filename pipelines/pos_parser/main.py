from pathlib import Path
import pandas as pd
from utils.yaml_loader import load_yaml
from config.paths import POS_PARSER_CFG, POS_PARSER_ENV
from pipelines.pos_parser.readers.factory import get_reader
from data_toolkit.cleaners.data_cleaner import DataCleaner
from data_toolkit.cleaners.adapters import build_cleaner_cfg
from schemas.pos_schema import PosSchemaMapping, POS_SCHEMA_DEF
from data_toolkit.clients.acumatica import AcumaticaClient
import os
from dotenv import load_dotenv
from pipelines.pos_parser.enrichment.enricher import Enricher

import logging

logging.basicConfig(level=logging.INFO)

"""
SMELLS:
what if a sheet name or index changes?
"""

PERIOD_DATE = "10/31/2025"


def main():
    
    # ================ Resources =================
    load_dotenv(POS_PARSER_ENV)

    global_cfg = load_yaml(POS_PARSER_CFG)
    enricher_cfg = global_cfg["enricher"]

    files = list(Path(r"H:\Pro AV and Sales Operations\Sales Reports\POS Reports\Monthly POS Loads to Dan\October 2025").glob("*"))

    dfs = []

    for file_cfg in global_cfg["files_cfg"]:

        file_id = file_cfg["file_id"].casefold()

        logging.debug(f"parsing {file_id}")

        path = next((file for file in files if file_id in file.stem.casefold()), None)

        # ================ Data Collection =================

        reader = get_reader(kind=file_cfg["reader"])
        
        reader_cfg = file_cfg.get("reader_cfg", None)

        if reader_cfg is None:
            df = reader.df(path)
        else:
            df = reader.df(file_path=path, cfg=reader_cfg)

        # ================ Data Cleaning =================

        schema_mapping = PosSchemaMapping(**file_cfg["CanonicalSchema"])
        
        cleaner_cfg = build_cleaner_cfg(POS_SCHEMA_DEF, schema_mapping)
        cleaner_cfg.src_id = file_cfg["src_id"]
        cleaner_cfg.src_col_name = file_cfg["src_col_name"]
        cleaner_cfg.col_order = [cleaner_cfg.src_col_name] + cleaner_cfg.col_order

        cleaner = DataCleaner(cleaner_cfg)

        df_clean = cleaner.clean(df)

        dfs.append(df_clean)

    stacked = pd.concat(dfs)

    # ================ Enrichment =================

    # Period date, credits, drop columns, category
    raw_cats = AcumaticaClient(
        username = enricher_cfg["categories"]["auth"]["username"], 
        password = enricher_cfg["categories"]["auth"]["password"]
        ).odata(
            enricher_cfg["categories"]["url"], 
            params=enricher_cfg["categories"]["params"]
    )

    clean_cats = {r["InventoryID"] : r["Category"] for r in raw_cats}
    
    category_cfg = enricher_cfg["categories"]["cfg"]
    category_cfg["mapping"] = clean_cats

    # TODO: create credit_cfg and function in Enricher

    enriched_df = Enricher(
        period_date=PERIOD_DATE,
        category_cfg=category_cfg,
        credit_cfg=None
    ).apply(stacked)

    enriched_df.to_csv(r"C:\Users\eddiec11us\Desktop\pos.csv", index=False)

"""
phase two:
    description if available?
    cross references
"""

if __name__ == "__main__":
    raise SystemExit(main())
from dotenv import load_dotenv
from pathlib import Path
import logging

import duckdb
import pandas as pd

from config.paths import POS_PARSER_CFG, POS_PARSER_ENV
from data_toolkit.clients.acumatica import AcumaticaClient
from data_toolkit.cleaners.data_cleaner import DataCleaner
from data_toolkit.cleaners.adapters import build_cleaner_cfg
from pipelines.pos_parser.enrichment.enricher import Enricher
from pipelines.pos_parser.normalizer.sales_normalizer import normalize_sales
from pipelines.pos_parser.readers.factory import get_reader
from schemas.pos_schema import PosSchemaMapping, POS_SCHEMA_DEF
from utils.yaml_loader import load_yaml

logging.basicConfig(level=logging.DEBUG)

"""
SMELLS:
what if a sheet name or index changes?

!!Out file is not dynamically updated!!

"""

PERIOD_DATE = "03/31/2026"
STRICT_CATEGORIES = True

def main():
    
    # ================ Resources =================
    load_dotenv(POS_PARSER_ENV)

    global_cfg = load_yaml(POS_PARSER_CFG)
    enricher_cfg = global_cfg["enricher"]
    files = list(Path(global_cfg["pos_dir"]).glob("*"))

    dfs = []

    for file_cfg in global_cfg["files_cfg"]:

        file_id = file_cfg["file_id"].casefold()

        logging.debug(f"parsing {file_cfg['src_id']}")

        path = next((file for file in files if file_id in file.stem.casefold()), None)

        if path == None:
            raise ValueError(f"{file_cfg['src_id']} file not found")

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

        df_clean = DataCleaner(cleaner_cfg).clean(df)

        df_norm = normalize_sales(df_clean, return_id=file_cfg["return_id"])

        dfs.append(df_norm)

    stacked = pd.concat(dfs)

    # ================ Enrichment =================
    # Period date, credits, drop columns, category

    client = AcumaticaClient(**enricher_cfg["categories"]["auth"])

    raw_cats = client.odata(
        url=enricher_cfg["categories"]["url"], 
        params=enricher_cfg["categories"]["params"]
    )

    clean_cats = {r["InventoryID"].strip() : r["Category"].strip() for r in raw_cats}

    additional_cats_df = pd.read_csv(enricher_cfg["categories"]["additional"]["file_path"])
    
    add_cats = additional_cats_df.set_index("InventoryID").to_dict()['Category']

    clean_cats.update(add_cats)

    curr_parts = set(
        s for s in stacked['PiiPartNumber'] 
        if pd.notna(s) and s != ""
    )

    non_categorized_parts = curr_parts.difference(clean_cats.keys())

    if non_categorized_parts:
        missing_parts_df = pd.DataFrame(data=non_categorized_parts, columns=["InventoryID"])
        add_cats_file_path = enricher_cfg['categories']['additional']['file_path']
        temp_cats_df = pd.read_csv(add_cats_file_path)
        cats_out = pd.concat([temp_cats_df, missing_parts_df])
        cats_out.to_csv(add_cats_file_path, index=False)
        
        if STRICT_CATEGORIES:
            raise LookupError(f"missing parts in additional_categories.csv: {len(missing_parts_df)} added")

    category_cfg = enricher_cfg["categories"]["cfg"]

    category_cfg["mapping"] = clean_cats

    enriched_df = Enricher(
        period_date=PERIOD_DATE,
        category_cfg=category_cfg,
        credit_cfg=enricher_cfg["credit_rules"]
    ).apply(stacked)

    # store to persistent table

    db = duckdb.connect(global_cfg["pos_sales_db"])
    db.sql("CREATE OR REPLACE TABLE pos_sales AS SELECT * FROM enriched_df")

    enriched_df.to_csv(r"C:\Users\eddiec11us\Desktop\March_2026_POS.csv", index=False)

if __name__ == "__main__":
    raise SystemExit(main())


"""
- dtype specification for zips at reader (yagni?)

- check credit outputs

5. 
using soldtoname where bill to state is not blank ONLY if it is a 1:1
or return blank? this might be better and just let cm make the call

=====
phase three:
    cross references
    sales person
    apply rules to files recursively
====
"""
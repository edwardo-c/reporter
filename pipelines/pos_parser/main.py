from pathlib import Path
import pandas as pd
from utils.yaml_loader import load_yaml
from config.paths import POS_PARSER_CFG
from pipelines.pos_parser.readers.factory import get_reader
from data_toolkit.cleaners.data_cleaner import DataCleaner
from data_toolkit.cleaners.adapters import build_cleaner_cfg
from schemas.pos_schema import PosSchemaMapping, POS_SCHEMA_DEF

import logging

logging.basicConfig(level=logging.DEBUG)

"""
SMELLS:
what if a sheet name or index changes?
"""

def main():
    
    # ================ Resources =================

    cfg = load_yaml(POS_PARSER_CFG)

    files = list(Path(r"H:\Pro AV and Sales Operations\Sales Reports\POS Reports\Monthly POS Loads to Dan\October 2025").glob("*"))

    dfs = []

    for cfg in cfg["files_cfg"]:

        file_id = cfg["file_id"].casefold()

        logging.debug(f"parsing {file_id}")

        path = next((file for file in files if file_id in file.stem.casefold()), None)

        # ================ Data Collection =================

        reader = get_reader(kind=cfg["reader"])
        
        reader_cfg = cfg.get("reader_cfg", None)

        if reader_cfg is None:
            df = reader.df(path)
        else:
            df = reader.df(file_path=path, cfg=reader_cfg)

        # ================ Data Cleaning =================

        schema_mapping = PosSchemaMapping(**cfg["CanonicalSchema"])
        
        cleaner_cfg = build_cleaner_cfg(POS_SCHEMA_DEF, schema_mapping)

        cleaner = DataCleaner(cleaner_cfg)

        df_clean = cleaner.clean(df)

        dfs.append(df_clean)

    stacked = pd.concat(dfs)
    breakpoint()

    stacked.to_csv()

    # # export data
    # breakpoint()

    # categories should be straight from acumatica


"""
ADI and petra are auto assigned to earl for credit
Almo 
Almo exceptions, then buyers, bill to state
may not give bill to, if so then default to ship to
also account for 

phase two:
    description if available?
    cross references
    salesperson name to cleaner_cfg
"""


if __name__ == "__main__":
    raise SystemExit(main())
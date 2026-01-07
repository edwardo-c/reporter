from pathlib import Path

import pandas as pd

from utils.yaml_loader import load_yaml
from dotenv import load_dotenv
from config.paths import POS_XREF_ENV_VARS, POS_XREF_CFG
from pipelines.pos_xref.xref import PosXref


load_dotenv(dotenv_path=Path(POS_XREF_ENV_VARS))

def main():

    """
    pos_xref pipeline - customer resolution engine
    compares incoming data against a master data set
    the master data set is a combination of those already under review and
    those already matched to a parent

    TODO: 
    - compile master_data_set, currently only reads single file
    - append latest data to outgoing path
    """

    cfg = load_yaml(POS_XREF_CFG)

    compare_cfg = cfg["compare"]
    compare_df = pd.read_csv(**compare_cfg["read"])

    compare_against_cfg = cfg["compare_against"]
    compare_against_df = pd.read_csv(**compare_against_cfg["read"])

    join_columns = {"SoldToName": "Child"}

    px: PosXref = PosXref(
        left=compare_df, 
        right=compare_against_df,
        join_columns=join_columns
        outgoing_path
    )

if __name__ == "__main__":
    main()
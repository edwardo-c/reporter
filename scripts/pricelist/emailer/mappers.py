import pandas as pd

from data_toolkit.attachments.mapper import AttchmentMap
from data_toolkit.arrangers.df_to_dict_list import get_mapping
from scripts.pricelist.emailer import config

def build_contacts_map(
        contacts_df: pd.DataFrame,
        key_col: str,
        value_col: str
    ) -> dict[str, list[str]]:
    """
    thin wrapper for converting contacts dataframe to map
    """
    mapping = get_mapping(contacts_df, key_col, value_col)
    return mapping

def build_attachment_map(
        src_dir, 
        glob_pattern: str = config.GLOB_PATTERN, 
        re_pattern: str = config.ACU_ID_RE
    ) -> AttchmentMap:
    
    return AttchmentMap(
        src_dir=src_dir,
        glob_pattern=glob_pattern,
        re_pattern=re_pattern
    )


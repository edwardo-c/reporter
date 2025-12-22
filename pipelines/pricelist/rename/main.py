"""Copy and rename files with safe file naming convention"""
from pathlib import Path
import re
from shutil import copy2
from dotenv import load_dotenv

import pandas as pd

from utils.yaml_loader import load_yaml
from config.paths import PRICE_LIST_ENV, PRICE_LIST_RENAME_CFG

PROD = False

def main():

    load_dotenv(PRICE_LIST_ENV)

    cfg = load_yaml(PRICE_LIST_RENAME_CFG)
    
    args = cfg.get("args", None)
    if not args:
        raise ValueError("missing args to read rename map worksheet, did YAML load?")
    
    rename_df = pd.read_excel(**args)
    id_newname_map: dict = rename_df.set_index("Customer Account Number").to_dict()['Price List Name']

    ids_to_move = set(id_newname_map.keys())

    brand_dir_map: dict = cfg["brand_dir_map"]
    
    dst_dir = Path(cfg["dst_dir"])
    
    for brand, files_dir in brand_dir_map.items():
        
        brand_files = Path(files_dir).glob("*.xlsx")
        
        for src_path in brand_files:
            
            acct_id = _extract_acct_num(src_path)
            
            if (acct_id and acct_id in ids_to_move):
                
                file_name = Path(src_path).stem
                
                dst_name = _gen_dst_name(
                    extract_from_str=file_name,
                    brand=brand,
                    acct_id=acct_id,
                )
                
                dst_path = dst_dir / dst_name
                
                if PROD:
                    copy2(src=src_path, dst=dst_path)    
                else:
                    breakpoint()

def _gen_dst_name(
        extract_from_str: str,
        brand: str,
        acct_id: str,
        year: str | int | None = None,
        acct_name: str | None = None,
    ):
    """
    applies naming nomenclature and appends .xlsx
    # [Year] [Brand] [Cust Name] ([Account Number]) Price List - [Date, MMDDYY]
    """
    
    eff_date_pattern = r"\b[0-9]{2}\.[0-9]{2}\b"

    if not year:
        yr_pattern = r"\b20[0-9]{2}\b"
        year_re = re.search(yr_pattern, extract_from_str)
        year = str(year_re.group(0))
    
    elif isinstance(year, int):
        year = str(year)
    
    year_sfx = year[2:]

    eff_date_sfx_re = re.search(eff_date_pattern, extract_from_str)
    eff_date_sfx = eff_date_sfx_re.group(0).replace('.','')
    eff_date = f"{eff_date_sfx}{year_sfx}"

    if not acct_name:
        acct_name_pattern = r"[A-Za-z0-9]{1,3}[0-9]{6}\s-\s(.*)"
        acct_name = re.search(acct_name_pattern, extract_from_str)
        acct_name = acct_name.group(1)

    safe_acct = _safe_filename(acct_name)

    result = (
        f"{year} {brand} {safe_acct} ({acct_id}) "
        f"Price List - {eff_date}.xlsx"
    )

    return result

def _extract_acct_num(s: Path | str) -> str | None:
    pattern = r"[A-Za-z0-9]{1,3}[0-9]{6}"
    m = re.search(pattern, str(s))
    return str(m[0]) if m else None

def _safe_filename(s: str) -> str:
    """Make a string safe for Windows filenames and format to Proper Case"""
    # Normalize spacing and capitalization
    s = s.strip()

    # Replace forbidden characters
    forbidden = r'\/:*?"<>|'
    for ch in forbidden:
        s = s.replace(ch, "_")

    # Strip trailing spaces or dots (illegal in Windows)
    return s.rstrip(" .")

if __name__ == "__main__":
    main()

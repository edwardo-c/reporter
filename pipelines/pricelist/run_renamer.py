"""Copy and rename files with seperate file convention"""

from pathlib import Path
from typing import Iterable, Tuple

from dotenv import load_dotenv
from config.paths import PRICE_LIST_ENV
import os
import re
import requests
import pandas as pd


def main():
    load_dotenv(PRICE_LIST_ENV)
    
    accts = _get_src_IDs()

    files_to_move = _gather_files(
        {"Peerless-AV": Path(os.getenv("PAV_ATTACHMENTS")),
         "Neptune": Path(os.getenv("NEP_ATTACHMENTS"))}, accts)
    
    rename_map = _rename_map(files_to_move)

    breakpoint()


def _move_to_dst(conversion_map: Iterable[Tuple[Path, Path]]):
    """Copies files per (src, dst) pairs"""
    ...

def _rename_map(files_to_move: dict[str, Path]):
    """files_to_move 
    {BrandName: [Path to be moved],}
    """
    def _gen_dst(s: str, brand: str):
        yr = re.search(yr_pattern, s)
        eff_date = re.search(eff_date_pattern, s)
        acct_name = re.search(acct_name_pattern, s)
        return f"{yr.group(0)} {brand} {acct_name.group(1)} Price List - {eff_date.group(0).replace(".","")}{yr.group(0)[2:]}"

    yr_pattern = r"\b20[0-9]{2}\b"
    eff_date_pattern = r"\b[0-9]{2}\.[0-9]{2}\b"
    acct_name_pattern = r"[A-Za-z0-9]{1,3}[0-9]{6}\s-\s(.*)"
    
    """creates a list of Tuples (src, dst)""" 
    result = []
    
    for brand, files in files_to_move.items():
        for src in files:
            dst = src.parent / _gen_dst(src.stem, brand)
            result.append((src, dst))
    
    return result


def _gather_files(brand_dir_map: dict[str, Path], valid_ids: set):
    
    def _extract_acct_num(s: Path | str) -> str | None:
            pattern = r"[A-Za-z0-9]{1,3}[0-9]{6}"
            m = re.search(pattern, str(s))
            return str(m[0]) if m else None
    
    return {
        brand: [f for f in Path(dir).glob("*.xlsx") 
                if _extract_acct_num(str(f)) in valid_ids]
        for brand, dir in brand_dir_map.items()
    }


def _get_src_IDs():
    """pulls customer id data for en directly from Acu"""
    url = os.getenv("CUSTOMERS_FEED")
    username = os.getenv("ACU_USERNAME")
    password = os.getenv("ACU_PW")
    
    params = {
        "$select": "CustomerID",
        "$filter": "AccountOwner eq 'EN6682'",
        "$format": "json"
    }
    
    resp = requests.get(url, auth=(username, password), params=params)
    resp.raise_for_status()

    data = resp.json().get("value", [])
    return {str(row["CustomerID"]).strip() for row in data}

if __name__ == "__main__":
    main()
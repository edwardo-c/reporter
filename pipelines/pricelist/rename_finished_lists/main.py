"""Copy and rename files with safe file naming convention"""

from pathlib import Path
from typing import Iterable, Tuple
from dotenv import load_dotenv
from config.paths import PRICE_LIST_ENV
import os
import re
import requests
import pandas as pd
from shutil import copy2


def main():
    load_dotenv(PRICE_LIST_ENV)

    accts = _get_src_IDs()

    files_to_move = _gather_files(
        {"Peerless-AV": Path(os.getenv("PAV_FINISHED_LISTS")),
         "Neptune": Path(os.getenv("NEP_FINISHED_LISTS"))}, accts
    )

    rename_map = _rename_map(files_to_move, Path(os.getenv("EN_DST")))

    _move_to_dst(rename_map)


def _move_to_dst(conversion_maps: Iterable[Tuple[Path, Path]]):
    """Copies files per (src, dst) pairs"""
    for src, dst in conversion_maps:
        copy2(src=src, dst=dst)


def _safe_filename(s: str) -> str:
    """Make a string safe for Windows filenames and format to Proper Case"""
    # Normalize spacing and capitalization
    s = s.strip().title()

    # Replace forbidden characters
    forbidden = r'\/:*?"<>|'
    for ch in forbidden:
        s = s.replace(ch, "_")

    # Strip trailing spaces or dots (illegal in Windows)
    return s.rstrip(" .")


def _rename_map(files_to_move: dict[str, list[Path]], target_dir: Path):
    """files_to_move {BrandName: [Path to be moved],}"""

    def _gen_dst(s: str, brand: str):
        yr = re.search(yr_pattern, s)
        eff_date = re.search(eff_date_pattern, s)
        acct_name = re.search(acct_name_pattern, s)

        safe_acct = _safe_filename(acct_name.group(1))
        return (
            f"{yr.group(0)} {brand} {safe_acct} "
            f"Price List - {eff_date.group(0).replace('.','')}{yr.group(0)[2:]}.xlsx"
        )

    yr_pattern = r"\b20[0-9]{2}\b"
    eff_date_pattern = r"\b[0-9]{2}\.[0-9]{2}\b"
    acct_name_pattern = r"[A-Za-z0-9]{1,3}[0-9]{6}\s-\s(.*)"

    result = []

    for brand, files in files_to_move.items():
        for src in files:
            dst = target_dir / _gen_dst(src.stem, brand)
            result.append((src, dst))

    return result


def _gather_files(brand_dir_map: dict[str, Path], valid_ids: set[str]):
    def _extract_acct_num(s: Path | str) -> str | None:
        pattern = r"[A-Za-z0-9]{1,3}[0-9]{6}"
        m = re.search(pattern, str(s))
        return str(m[0]) if m else None

    return {
        brand: [
            f
            for f in Path(dir).glob("*.xlsx")
            if _extract_acct_num(str(f)) in valid_ids
        ]
        for brand, dir in brand_dir_map.items()
    }


def _get_src_IDs() -> set[str]:
    """pulls customer id data for EN directly from Acu"""
    url = os.getenv("CUSTOMERS_FEED")
    username = os.getenv("ACU_USERNAME")
    password = os.getenv("ACU_PW")

    params = {
        "$select": "CustomerID",
        "$filter": "AccountOwner eq 'EN6682'",
        "$format": "json",
    }

    resp = requests.get(url, auth=(username, password), params=params)
    resp.raise_for_status()
    data = resp.json().get("value", [])
    return {str(row["CustomerID"]).strip() for row in data}


if __name__ == "__main__":
    main()

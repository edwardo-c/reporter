from dataclasses import dataclass
from typing import Tuple, Dict, Optional

from data_toolkit.cleaners.data_cleaner import CleanerCfg


@dataclass(frozen=True)
class CanonicalSchemaDef:
    str_fields: Tuple[str, ...]
    float_fields: Tuple[str, ...]
    date_fields: Tuple[str, ...]
    zipcode_fields: Tuple[str, ...]


def build_cleaner_cfg(schema_def: CanonicalSchemaDef, mapping) -> CleanerCfg:
    """
    Generic adapter: schema_def + mapping -> CleanerCfg.

    `mapping` is any object with .as_dict() -> dict[canonical_name, source_col_or_None].
    """
    m: Dict[str, Optional[str]] = mapping.as_dict()
    
    available = {canon: src for canon, src in m.items() if src is not None}

    cfg = CleanerCfg()

    # source_col -> canonical_name
    cfg.rename_map = {src: canon for canon, src in available.items()}

    # canonical order
    cfg.keep_cols = list(available.keys())
    cfg.col_order = list(available.keys())

    cfg.str_cols = [canon for canon in schema_def.str_fields if canon in available]
    cfg.float_cols = [canon for canon in schema_def.float_fields if canon in available]
    cfg.date_cols = [canon for canon in schema_def.date_fields if canon in available]
    cfg.zipcode_cols = [canon for canon in schema_def.zipcode_fields if canon in available]

    return cfg

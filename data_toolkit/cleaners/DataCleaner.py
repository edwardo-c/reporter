import pandas as pd
import numpy as np
import re

from dataclasses import dataclass, field

@dataclass
class CleanerCfg:
    keep_cols: list[str] | str = 'all'
    str_cols: list[str] | str
    numeric_cols: list[str] = field(default_factory=list)
    float_cols: list[str] = field(default_factory=list)
    date_cols: list[str] = field(default_factory=list)
    rename_map: dict[str, str] = field(default_factory=dict)
    zipcode_cols: dict[str, str] = field(default_factory=dict)

    def __post_init__(self):
        kc = self.keep_cols
        if not (kc == "all" or (isinstance(kc, list) and all(isinstance(c, str) for c in kc))):
            raise TypeError("keep_cols must be 'all' or list[str]")
        
        sc = self.str_cols
        if isinstance(sc, str):
            self.str_cols = [sc]
        elif sc is None:
            self.str_cols = []

class DataCleaner():
    """
    zipcode_cols: {'dst_col', 'src_col'} cleans us and ca zip codes, returning only first 5 for us and complete for ca
    """
    def __init__(
        self,
        cfg: CleanerCfg | None = None,
        *,
        keep_cols: list[str] | str | None = None,
        str_cols: list[str] | None = None,
        float_cols: list[str] | None = None,
        date_cols: list[str] | None = None,
        zipcode_cols: dict[str, str] | None = None,
        rename_map: dict[str, str] | None = None,
    ):
        if cfg is None:
            cfg = CleanerCfg(
                keep_cols = keep_cols if keep_cols is not None else "all",
                str_cols = str_cols or [],
                float_cols = float_cols or [],
                date_cols = date_cols or [],
                zipcode_cols = zipcode_cols or {},
                rename_map = rename_map or {},
            )
        self.cfg = cfg
    
    def _coerce_data_types(self, df: pd.DataFrame):

        assign = {}

        if self.cfg.str_cols:
            for str_col in self.cfg.str_cols:
                assign[str_col] = df[str_col].astype("string").str.strip()
        
        if self.cfg.float_cols:
            for float_col in self.cfg.float_cols:
                assign[float_col] = pd.to_numeric(df[float_col], errors="coerce").round(2)
        
        if self.cfg.date_cols:
            for date_col in self.cfg.date_cols:
                assign[date_col] = pd.to_datetime(df[date_col], errors="coerce", format="%Y-%m-%d")

        return df.assign(**assign)
    
    def add_postal(self, df: pd.DataFrame) -> pd.DataFrame:
        US_RE = r'^\s*(\d{5})(?:[-\s]?(\d{4}))?\s*$'
        CA_RE = r'^\s*([ABCEGHJ-NPRSTVXY]\d[ABCEGHJ-NPRSTV-Z])(\d[ABCEGHJ-NPRSTV-Z]\d)\s*$'

        assigns: dict[str, pd.Series] = {}
        drops: list[str] = []

        for dst_col, src_col in self.cfg.zipcode_cols.items():
            s = df[src_col].astype("string").str.upper().str.strip()

            us = s.str.extract(US_RE)
            ca = s.str.replace(" ", "", regex=False).str.extract(CA_RE)

            primary = pd.Series(
                np.where(
                    us[0].notna(), us[0],
                    np.where(ca[0].notna(), ca[0].str.cat(ca[1], sep=" "), pd.NA)
                ),
                index=df.index,
                name=dst_col,
            )

            assigns[dst_col] = primary
            drops.append(src_col)

        return (
            df.assign(**assigns)
            .drop(columns=[c for c in drops if c in df.columns], errors="ignore")
        )

    def _columns_exist(self, existing_cols: set) -> None:
        cols_to_check = (self.cfg.str_cols, self.cfg.float_cols, self.cfg.date_cols, self.cfg.zipcode_cols.values())
        for grp in cols_to_check:
            if not grp:
                continue
            missing = [c for c in grp if c not in existing_cols]
            if missing: 
                raise KeyError(f"column(s): {missing} missing from df - {existing_cols}")

    def _column_manager(self, df: pd.DataFrame):
        
        if self.cfg.rename_map:    
            df = df.rename(columns=self.cfg.rename_map)
            
        if isinstance(self.cfg.keep_cols, list):
            return df[self.cfg.keep_cols]
        elif isinstance(self.cfg.keep_cols, str) and self.cfg.keep_cols == 'all':
            return df
        else:
            raise KeyError(f"invalid self.cfg.keep_cols; must be 'all' or list of ['cols', 'to', 'keep'] ")
        

    def clean(self, df: pd.DataFrame):
        self._columns_exist(set(df.columns))
        df = self._coerce_data_types(df)
        df = self.add_postal(df)
        df = self._column_manager(df)

        return df
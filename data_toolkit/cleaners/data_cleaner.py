import pandas as pd
import numpy as np
import re

from dataclasses import dataclass, field

@dataclass
class CleanerCfg:
    str_cols: list[str] = field(default_factory=list)
    keep_cols: list[str] = field(default_factory=list)
    col_order: list[str] = field(default_factory=list)
    float_cols: list[str] = field(default_factory=list)
    date_cols: list[str] = field(default_factory=list)
    zipcode_cols: list[str] = field(default_factory=list)
    rename_map: dict[str, str] = field(default_factory=dict)

class DataCleaner():
    """clean data based off CleanerCfg"""
    def __init__(
        self,
        cfg: CleanerCfg | None = None,
        *,
        keep_cols: list[str] | None = None,
        str_cols: list[str] | None = None,
        col_order: list[str] | None = None,
        float_cols: list[str] | None = None,
        date_cols: list[str] | None = None,
        zipcode_cols: list[str] | None = None,
        rename_map: dict[str, str] | None = None,
    ):

        if cfg is None:
            cfg = CleanerCfg(
                str_cols = str_cols or [],
                keep_cols = keep_cols or [],
                col_order = col_order or [],
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

        for col in self.cfg.zipcode_cols:
            s = df[col].astype("string").str.upper().str.strip()

            us = s.str.extract(US_RE)
            ca = s.str.replace(" ", "", regex=False).str.extract(CA_RE)

            primary = pd.Series(
                np.where(
                    us[0].notna(), us[0],
                    np.where(ca[0].notna(), ca[0].str.cat(ca[1], sep=" "), pd.NA)
                ),
                index=df.index,
                name=col,
            )

            assigns[col] = primary

        return df.assign(**assigns)


    def _columns_exist(self, existing_cols: set) -> None:
        cols_to_check_groups = (
            self.cfg.str_cols,
            self.cfg.float_cols,
            self.cfg.date_cols,
            self.cfg.zipcode_cols,
            self.cfg.keep_cols,
            self.cfg.col_order,
        )

        for grp in cols_to_check_groups:
            if not grp:
                continue
            missing = [c for c in grp if c not in existing_cols]
            if missing:
                raise KeyError(f"column(s): {missing} missing from df - {existing_cols}")


    def _column_rename(self, df: pd.DataFrame) -> pd.DataFrame:
        if self.cfg.rename_map:    
            df = df.rename(columns=self.cfg.rename_map)
        return df

    def _keep_cols(self, df: pd.DataFrame) -> pd.DataFrame:
        if self.cfg.keep_cols:
            df = df[self.cfg.keep_cols]
        return df

    def _column_order(self, df: pd.DataFrame) -> pd.DataFrame:
        if self.cfg.col_order:
            df = df[self.cfg.col_order]
        return df

    def clean(self, df: pd.DataFrame) -> pd.DataFrame:
        
        df = self._column_rename(df)
        self._columns_exist(set(df.columns))
        df = self._coerce_data_types(df)
        df = self.add_postal(df)
        df = self._keep_cols(df)
        df = self._column_order(df)

        return df

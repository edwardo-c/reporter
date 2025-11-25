import pandas as pd
from datetime import datetime


class Enricher:
    def __init__(
        self,
        period_date: str | datetime,
        category_cfg: dict,
        credit_cfg: dict,
    ):
        self.period_date = self._parse_period_date(period_date)
        self.category_cfg = self._validate_cat_cfg(category_cfg)
        self.credit_cfg = credit_cfg

    # === PERIOD DATE ======================================================

    def _parse_period_date(self, value: str | datetime | None):
        if value is None:
            return None
        return pd.to_datetime(value, errors="coerce")

    def add_period_date(self, df: pd.DataFrame) -> pd.DataFrame:
        if self.period_date is None:
            raise ValueError("Period Date is required!")
        return df.assign(PeriodDate=self.period_date)

    # === CATEGORY LOGIC ===================================================

    def _validate_cat_cfg(self, cfg: dict):
        left = cfg.get("left", None)
        right = cfg.get("right", None)
        cat_mapping = cfg.get("mapping", None)

        if not all([left, right, cat_mapping]):
            raise ValueError("invalid categories config")

        # normalize mapping to uppercase/stripped
        cfg["mapping"] = {
            k.strip().upper(): v.strip().upper()
            for k, v in cat_mapping.items()
        }

        return cfg

    def add_category(self, df: pd.DataFrame) -> pd.DataFrame:
        left = self.category_cfg["left"]
        right = self.category_cfg["right"]
        mapping = self.category_cfg["mapping"]

        lookup_key = df[left].astype("string").str.strip().str.upper()
        df[right] = lookup_key.map(mapping)
        return df

    # === CREDIT ORCHESTRATION ============================================

    def apply_credit(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Orchestrates all credit rules in self.credit_cfg["rules"].

        - Supports:
            kind="mapping"   → simple 1:1 mapping (e.g. State → SalesRep)
            kind="zip_range" → State + ZipMin/ZipMax based mapping
        - Earlier rules have precedence: once `out` is filled, later rules
          only fill remaining NaNs.
        """
        out = "SalesRep"
        df = df.copy()

        # Ensure output column exists and can hold strings
        if out not in df.columns:
            df[out] = pd.Series([None] * len(df), dtype="object")
        else:
            df[out] = df[out].astype("object")

        for rule in self.credit_cfg:
            kind = rule.get("kind", "mapping")

            if kind == "mapping":
                # mapping may be passed directly or via map_args → _load_mapping()
                mapping = rule.get("mapping")
                if mapping is None and "map_args" in rule:
                    mapping = self._load_mapping(**rule["map_args"])

                self._apply_mapping_rule(
                    df=df,
                    out=out,
                    left=rule["left"],
                    mapping=mapping,
                )

            elif kind == "zip_range":
                rules_df = self._load_zip_rules(**rule["range_args"])

                self._apply_zip_range_rule(
                    df=df,
                    out=out,
                    rules_df=rules_df,
                    state_col=rule.get("state_col", "State"),
                    zip_col=rule.get("zip_col", "Zip"),
                )

            else:
                raise ValueError(f"Unknown credit rule kind: {kind!r}")

        return df

    def drop_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        # placeholder for later
        return df

    # === HELPERS: LOADING CONFIG TABLES ==================================

    def _load_mapping(
        self,
        path,
        sheet,
        usecols,
        skiprows: int = 0,
        nrows: int | None = None,
    ) -> dict:
        """
        Read a 2-column mapping table from an Excel sheet and return {key: value}.

        - path: Excel file path
        - sheet: sheet name (e.g. "Config")
        - usecols: list of integer column positions, e.g. [0, 1] or [3, 4]
        - skiprows: number of rows to skip before the header (Excel row 3 -> skiprows=2)
        - nrows: optional row limit
        """
        df = pd.read_excel(
            path,
            sheet_name=sheet,
            usecols=usecols,
            skiprows=skiprows,
            nrows=nrows,
        )

        # We know this is a 2-column mapping table — normalize names
        if df.shape[1] != 2:
            raise ValueError(f"Expected 2 columns for mapping, got {df.shape[1]}")

        df.columns = ["key", "value"]

        # Drop empty key rows (avoids {nan: nan})
        df = df.dropna(subset=["key"])

        return df.set_index("key")["value"].to_dict()

    def _load_zip_rules(
        self,
        path,
        sheet,
        usecols,
        skiprows: int = 0,
        nrows: int | None = None,
    ) -> pd.DataFrame:
        """
        Load a 4-column zip rules table:
            State, ZipMin, ZipMax, SalesRep

        Drops rows without ZipMin/ZipMax so only true range rules remain.
        """
        df = pd.read_excel(
            path,
            sheet_name=sheet,
            usecols=usecols,
            skiprows=skiprows,
            nrows=nrows,
        )

        if df.shape[1] != 4:
            raise ValueError(f"Expected 4 columns for zip rules, got {df.shape[1]}")

        df.columns = ["State", "ZipMin", "ZipMax", "SalesRep"]

        # Drop rows that are NOT true zip rules
        df = df.dropna(subset=["ZipMin", "ZipMax"])

        # Ensure numeric
        df["ZipMin"] = pd.to_numeric(df["ZipMin"], errors="coerce")
        df["ZipMax"] = pd.to_numeric(df["ZipMax"], errors="coerce")

        return df

    # === HELPERS: APPLYING CREDIT RULES ==================================

    def _apply_mapping_rule(
        self,
        df: pd.DataFrame,
        out: str,
        left: str,
        mapping: dict,
    ) -> None:
        """
        Simple 1:1 mapping: if df[left] == key → mapping[key] into df[out],
        but only where df[out] is still NaN (earlier rules win).
        """
        mapped = df[left].map(mapping)
        mask = df[out].isna() & mapped.notna()
        df.loc[mask, out] = mapped[mask]

    def _apply_zip_range_rule(
        self,
        df: pd.DataFrame,
        out: str,
        rules_df: pd.DataFrame,
        state_col: str = "State",
        zip_col: str = "Zip",
    ) -> None:
        """
        Zip-based credit:
            if df[state_col] == rule.State AND
               df[zip_col] between [ZipMin, ZipMax] → SalesRep

        Only fills rows where df[out] is still NaN (earlier rules win).
        """
        # ensure Zip is numeric
        df[zip_col] = pd.to_numeric(df[zip_col], errors="coerce")

        for _, r in rules_df.iterrows():
            state = r["State"]
            zmin = r["ZipMin"]
            zmax = r["ZipMax"]
            rep = r["SalesRep"]

            candidates = (
                (df[state_col] == state) &
                df[zip_col].between(zmin, zmax, inclusive="both")
            )

            mask = df[out].isna() & candidates
            df.loc[mask, out] = rep

    # === PIPELINE ENTRYPOINT =============================================

    def apply(self, df: pd.DataFrame) -> pd.DataFrame:
        df = self.add_period_date(df)
        df = self.add_category(df)
        df = self.apply_credit(df)
        df = self.drop_columns(df)
        return df

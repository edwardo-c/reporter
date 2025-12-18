import pandas as pd
from datetime import datetime
import numpy as np

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
        rep_out = "SalesRep"
        rule_out = "SalesRepAssignedRule"

        df = df.copy()

        # Ensure output columns exists and can hold strings
        for c in (rep_out, rule_out):
            if c not in df.columns:
                df[c] = pd.Series([None] * len(df), dtype="object")
            else:
                df[c] = df[c].astype("object")

        for rule in self.credit_cfg:
            kind = rule.get("kind", "mapping")

            if kind == "mapping":
                # mapping may be passed directly or via map_args → _load_mapping()
                mapping = rule.get("mapping")
                if mapping is None and "map_args" in rule:
                    mapping = self._load_mapping(**rule["map_args"])

                self._apply_mapping_rule(
                    df=df,
                    credit_rep_out=rep_out,
                    left=rule["left"],
                    mapping=mapping,
                    credit_rule_out=rule_out,
                    credit_rule_id=rule["rule_id"]
                )

            elif kind == "zip_range":
                
                rules_df = pd.DataFrame.from_dict(rule["data_dict"])

                # deprecated since the table's objective was changed
                # rules_df = self._load_zip_rules(**rule["range_args"])

                self._apply_zip_range_rule(
                    df=df,
                    credit_rep_out=rep_out,
                    rules_df=rules_df,
                    state_col=rule.get("state_col", "State"),
                    zip_col=rule.get("zip_col", "Zip"),
                    credit_rule_out=rule_out,
                    credit_rule_id=rule["rule_id"]
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
        filter_col = None,
        filter_val = None,
        key_col_name = None,
        val_col_name = None,
    ) -> dict:
        """
        Read a 2-column mapping table from an Excel sheet and return {key: value}.

        - path: Excel file path
        - sheet: sheet name (e.g. "Config")
        - usecols: list of integer column positions, e.g. [3, 4] or range of columns, e.g "A:E"
        - skiprows: number of rows to skip before the header (Excel row 3 -> skiprows=2)
        - nrows: optional row limit
        - filter_col: filter table by this column
        - filter_val: filter filter_col by this val
        - key_col_name: specify a key col when loading an entire table
        - val_col_name: specify a val col when loading an entire table
        """

        df = pd.read_excel(
                path,
                sheet_name=sheet,
                usecols=usecols,
                skiprows=skiprows,
                nrows=nrows,
            )

        # if filtering and k: v designation exists
        if all([filter_col, filter_val, key_col_name, val_col_name]):
            df = df[df[filter_col] == filter_val]
            df = df[[key_col_name, val_col_name]]

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
        credit_rep_out: str,
        left: str,
        mapping: dict,
        credit_rule_id: str,
        credit_rule_out: str = "SalesRepAssignedRule",
    ) -> None:
        """
        Simple 1:1 mapping: if df[left] == key → mapping[key] into df[out],
        but only where df[out] is still NaN (earlier rules win).
        """
        normalized_map = {k.casefold(): v for k, v in mapping.items()}

        mapped = df[left].str.casefold().map(normalized_map)
        mask = df[credit_rep_out].isna() & mapped.notna()
        df.loc[mask, credit_rep_out] = mapped[mask]
        df.loc[mask, credit_rule_out] = credit_rule_id


    def _apply_zip_range_rule(
        self,
        df: pd.DataFrame,
        credit_rep_out: str,
        rules_df: pd.DataFrame,
        credit_rule_id: str,
        state_col: str = "State",
        zip_col: str = "Zip",
        credit_rule_out: str = "SalesRepAssignedRule"
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

            mask = df[credit_rep_out].isna() & candidates
            df.loc[mask, credit_rep_out] = rep
            df.loc[mask, credit_rule_out] = credit_rule_id
        
        return df

    # === HELPERs: STATE ENRICHMENT =========================================

    def enrich_zips(
        self,
        df: pd.DataFrame,
        state_col_name: str = "BillToCustomerState",
        zip_col_name: str = "BillToCustomerZip",
    ) -> pd.DataFrame:

        _df = df.copy()
        _df["_orig_zip"] = _df[zip_col_name]

        # numeric zip for interval lookup (Canadian postal codes -> NaN)
        _df[zip_col_name] = pd.to_numeric(_df[zip_col_name], errors="coerce")

        candidates = _df[state_col_name].isna() & _df[zip_col_name].notna()
        if not candidates.any():
            _df[zip_col_name] = _df["_orig_zip"]
            return _df.drop(columns=["_orig_zip"])

        labels, zip_intervals = self._state_zip_interval_index()
        labels = np.asarray(labels, dtype=object)

        # --- LOOKUP ONLY ON CANDIDATES ---
        z = _df.loc[candidates, zip_col_name].astype("int64").to_numpy()
        idx_positions = zip_intervals.get_indexer(z)  # length == candidates.sum()

        valid = idx_positions != -1

        mapped = np.full(idx_positions.shape[0], pd.NA, dtype=object)
        mapped[valid] = labels[idx_positions[valid]]

        # assign back only to candidate rows (lengths now match by construction)
        _df.loc[candidates, state_col_name] = mapped

        # restore original zip codes (re-introduce Canadian codes)
        _df[zip_col_name] = _df["_orig_zip"]

        return _df.drop(columns=["_orig_zip"])

    @staticmethod
    def _state_zip_interval_index():
        """
        returns state keys (array) and interval index of zip codes.
        State -> (range_start, range_end)
        used for vectorized lookup of state with valid zip within range
        """

        zip_states_df = pd.DataFrame(
            [
                ("AL", 35000, 36999),
                ("AK", 99500, 99999),
                ("AZ", 85000, 86999),
                ("AR", 71600, 72999),
                ("CA", 90000, 96699),
                ("CO", 80000, 81699),
                ("CT",  6000,  6999),  # 06000–06999
                ("DE", 19700, 19999),
                ("FL", 32000, 34999),
                ("GA", 30000, 31999),
                ("HI", 96700, 96999),
                ("ID", 83200, 83899),
                ("IL", 60000, 62999),
                ("IN", 46000, 47999),
                ("IA", 50000, 52899),
                ("KS", 66000, 67999),
                ("KY", 40000, 42799),
                ("LA", 70000, 71499),
                ("ME",  3900,  4999),  # 03900–04999
                ("MD", 20600, 21999),
                ("MA",  1000,  2799),  # 01000–02799
                ("MI", 48000, 49999),
                ("MN", 55000, 56799),
                ("MS", 38600, 39799),
                ("MO", 63000, 65899),
                ("MT", 59000, 59999),
                ("NE", 68000, 69399),
                ("NV", 88900, 89899),
                ("NH",  3000,  3899),  # 03000–03899
                ("NJ",  7000,  8999),  # 07000–08999
                ("NM", 87000, 88499),
                ("NY", 10000, 14999),
                ("NC", 27000, 28999),
                ("ND", 58000, 58899),
                ("OH", 43000, 45899),
                ("OK", 73000, 74999),
                ("OR", 97000, 97999),
                ("PA", 15000, 19699),
                ("RI",  2800,  2999),  # 02800–02999
                ("SC", 29000, 29999),
                ("SD", 57000, 57799),
                ("TN", 37000, 38599),
                ("TX", 75000, 79999),
                ("TX", 88500, 88599),
                ("UT", 84000, 84799),
                ("VT",  5000,  5999),  # 05000–05999
                ("WA", 98000, 99499),
                ("WV", 24700, 26899),
                ("WI", 53000, 54999),
                ("WY", 82000, 83199),
                ("VA", 20100, 20199),
                ("VA", 22000, 24699),
                ("DC", 20000, 20099),
                ("DC", 20200, 20599),             
                ("PR",   600,   999),  # 00600–00999
            ],
            columns=["state", "range_start", "range_end"],
        )

        key = zip_states_df["state"].to_numpy()
        left = zip_states_df["range_start"]
        right = zip_states_df["range_end"]
        ii = pd.IntervalIndex.from_arrays(left, right, "both")

        return key, ii

    # === PIPELINE ENTRYPOINT =============================================

    def apply(self, df: pd.DataFrame) -> pd.DataFrame:
        df = self.add_period_date(df)
        df = self.add_category(df)
        df = self.enrich_zips(df)
        df = self.apply_credit(df)
        df = self.drop_columns(df)
        return df

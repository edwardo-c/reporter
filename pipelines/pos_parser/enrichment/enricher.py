import pandas as pd
from datetime import datetime

class Enricher:
    def __init__(
            self, 
            period_date: str | datetime, 
            category_cfg: dict,
            credit_cfg
        ):
        
        self.period_date = self._parse_period_date(period_date)
        self.category_cfg = self._validate_cat_cfg(category_cfg)
        self.credit_cfg = credit_cfg

    def _parse_period_date(self, value: str | datetime | None):
        if value is None:
            return None
        return pd.to_datetime(value, errors="coerce")
    
    def _validate_cat_cfg(self, cfg: dict):
        left = cfg.get("left", None)
        right = cfg.get("right", None)
        cat_mapping = cfg.get("mapping", None)

        if not all([left, right, cat_mapping]):
            raise ValueError(f"invalid categories config")
        
        cfg["mapping"] = {k.strip().upper(): v.strip().upper() for k, v in cat_mapping.items()}

        return cfg

    def add_period_date(self, df: pd.DataFrame):
        if self.period_date is None:
            raise ValueError(f"Period Date is required!")
        
        return df.assign(PeriodDate=self.period_date)

    def add_category(self, df: pd.DataFrame) -> pd.DataFrame:
        left = self.category_cfg["left"]
        right = self.category_cfg["right"]
        mapping = self.category_cfg["mapping"]
        lookup_key = df[left].astype("string").str.strip().str.upper()

        df[right] = lookup_key.map(mapping)

        return df

    def add_credit(self, df):
        """
        ADI and petra are auto assigned to earl for credit
        Almo 
        Almo exceptions, then buyers, bill to state
        may not give bill to, if so then default to ship to
        """
        
        return df

    def drop_columns(self, df):
        return df

    def apply(self, df: pd.DataFrame) -> pd.DataFrame:
        df = self.add_period_date(df)
        df = self.add_category(df)
        df = self.add_credit(df)
        df = self.drop_columns(df)

        return df
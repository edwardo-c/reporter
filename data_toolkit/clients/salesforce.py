"""simple_salesforce wrapper to validate authentication early (fail-fast)"""

from dataclasses import dataclass, field
from typing import Optional
from simple_salesforce import Salesforce
import pandas as pd

@dataclass
class SFClient:
    username: str
    password: str = field(repr=False)
    security_token: str = field(repr=False)
    domain: str = "login"
    validate_at_init: bool = True

    sf: Optional[Salesforce] = field(default=None, init=False, repr=False)

    def __post_init__(self):
        if self.validate_at_init:
            self.connect()

    def connect(self) -> None:
        try:
            self.sf = Salesforce(
                username=self.username,
                password=self.password,
                security_token=self.security_token,
                domain=self.domain
            )
        except Exception as exc:
            raise ConnectionError(
                "Unable to connect to Salesforce — check credentials, token, domain, or IP allowlist."
            ) from exc

    def _ensure_connected(self) -> Salesforce:
        if self.sf is None:
            self.connect()
        return self.sf

    def query(self, soql: str) -> pd.DataFrame:
        sf = self._ensure_connected()
        result = sf.query_all(soql)
        records = result.get("records", [])
        if not records:
            return pd.DataFrame()

        df = pd.json_normalize(records)

        return df.drop(columns=[c for c in list(df.columns) if 'attributes.' in c], errors="ignore")

    def log_task(self, params: dict):
        result = self.sf.Task.create(params)
from simple_salesforce import Salesforce
import pandas as pd
from dataclasses import dataclass

@dataclass
class SFCred:
    username: str
    password: str
    token: str

class SFClient:
    def __init__(
            self, 
            username: str | None = None,
            password: str | None = None,
            security_token: str | None = None,
            sf: Salesforce | None = None
        ):
        
        self._login_args = (username, password, security_token)
        self._sf = sf

        if self._sf is None:
            self._connect()
        else:
            self._sf = sf

    def _connect(self):
        if self._sf is None:
            u, p, t = self._login_args
            self._sf = Salesforce(username=u, password=p, security_token=t)
            self._login_args = (None, None, None)

    def __enter__(self):
        self._connect()
        return self

    def __exit__(self, exc_type, exc, tb):
        self._sf = None
    
    def query(self, soql: str, df: bool = True) -> pd.DataFrame | dict:
        res = self._sf.query_all(soql)
        records = res["records"]
        if df:
            return pd.DataFrame(records).drop(columns=["attributes"], errors="ignore")
        else:
            return records


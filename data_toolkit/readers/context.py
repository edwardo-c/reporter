from simple_salesforce import Salesforce
import requests
from dataclasses import dataclass

class ReaderContext:
    def __init__(
            self, 
            sf: Salesforce | None = None,
            acu: requests.Session | None = None):
        self.sf = sf
        self.acu = acu

@dataclass(frozen=True)
class SFCred:
    username: str
    password: str
    token: str

@dataclass(frozen=True)
class AcuCred:
    username: str
    password: str
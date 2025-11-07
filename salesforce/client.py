from dataclasses import dataclass, field
from typing import Optional
from simple_salesforce import Salesforce
import pandas as pd

@dataclass
class Credentials:
    username: str
    password: str = field(repr=False)
    security_token: str | None = field(repr=False)

class SFClient_Refactor:
    def __init__(
            self, 
            username: str | None = None, 
            password: str  | None  = None, 
            security_token: str  | None  = None,
            credentials: Credentials | None  = None,
        ):

        if not credentials:
            c = Credentials(
                username=username,
                password=password,
                security_token=security_token)

        self.sf = Salesforce(username=credentials.username)

    def upload_part(
            self, 
            part_params: dict,
            msrp_params: dict | None = None,
            price_lvl_params: dict | None = None
            ) -> bool:
        
        result = self.sf.Product2.create(part_params)

        if not result["success"]:
            return False
        
        id = result["id"]

        #TODO: upload msrp

        #TODO: upload price levels
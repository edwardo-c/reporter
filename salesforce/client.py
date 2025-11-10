from simple_salesforce import Salesforce
from salesforce.objects.msrp_entry import MSRPEntry
import pandas as pd

class SFClient:
    def __init__(
            self, 
            username: str | None = None,
            password: str | None = None,
            security_token: str | None = None,
            sf: Salesforce | None = None
        ):
        
        self._sf = sf
        self._login_args = (username, password, security_token)

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

    def upload_part(
            self, 
            part_params: dict,
            msrp: float,
            price_lvl_params: dict | None = None
            ) -> bool:

        part = self._sf.Product2.create(part_params)

        if not part["success"]:
            return False
        
        id = part["id"]

        self._sf.PricebookEntry.create(MSRPEntry(price=msrp, id=id).params)
    
        #TODO: upload price levels

    def _new_object(sf_obj: object, params: dict):
        return sf_obj.create(params)